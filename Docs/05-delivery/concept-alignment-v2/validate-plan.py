"""Validate the documentation execution plan; does not run or modify product code."""
from __future__ import annotations
import hashlib
import json
import re
import subprocess
from pathlib import Path

PACK = Path(__file__).resolve().parent
ROOT = PACK.parents[2]
REPOS = {'ROOT': ROOT, 'PUBLIC': ROOT/'Front-End/public-site',
         'ADMIN': ROOT/'Front-End/admin-panel', 'BACKEND': ROOT/'Back-End'}

def main():
    data = json.loads((PACK/'execution-tasks.json').read_text(encoding='utf-8'))
    tasks = data['tasks']; by_id = {t['id']: t for t in tasks}
    assert len(tasks) == len(by_id), 'duplicate ID'
    ancestors = {}; visiting = set()
    def visit(n):
        assert n in by_id, f'missing dependency {n}'
        if n in ancestors: return ancestors[n]
        assert n not in visiting, f'cycle at {n}'
        visiting.add(n); result = set()
        for d in by_id[n]['depends_on']: result |= {d} | visit(d)
        visiting.remove(n); ancestors[n] = result
        return result
    for n in by_id: visit(n)
    path_count = 0; overlap_count = 0; writers = {}
    for t in tasks:
        assert t['repository'] in REPOS
        assert t['status'] in {'DOC_COMPLETE', 'NOT_STARTED', 'REVISE', 'IMPLEMENTED_UNREVIEWED', 'BLOCKED', 'ACCEPTED_LOCAL'}
        if t['status'] in {'IMPLEMENTED_UNREVIEWED', 'REVISE', 'BLOCKED', 'ACCEPTED_LOCAL'}:
            # Implemented + locally tested, but uncommitted and not
            # owner-reviewed/accepted/published. Must cite the evidence report
            # and must NOT be treated as a satisfied dependency (see EXECUTION.md).
            assert isinstance(t.get('review_note'), str) and t['review_note'].strip(), (t['id'], 'review_note')
            assert (PACK/t['review_note']).is_file(), (t['id'], 'missing review evidence')
        assert t['active'] is True
        assert t['allowlist'] and len(t['allowlist']) == len(set(t['allowlist']))
        packet = PACK/t['packet']; assert packet.is_file(), packet
        text = packet.read_text(encoding='utf-8')
        assert t['stop_marker'] in text, (t['id'], 'stop marker')
        repo = REPOS[t['repository']].resolve()
        for rel in t['allowlist']:
            p = (repo/rel).resolve()
            assert p.is_relative_to(repo), (t['id'], 'path escape', rel)
            if t['repository'] == 'ROOT':
                assert not any(p.is_relative_to(REPOS[x]) for x in ('PUBLIC','ADMIN','BACKEND'))
            assert rel in text, (t['id'], 'packet/JSON allowlist mismatch', rel)
            assert p.exists() or rel in t['proposed_new_files'], (t['id'], 'unlabelled new path', rel)
            path_count += 1
            if t['status'] != 'DOC_COMPLETE': writers.setdefault((t['repository'],rel),[]).append(t['id'])
        for dependency in t.get('file_serialization_dependencies',[]):
            assert dependency in t['depends_on']
    for key, ids in writers.items():
        for i,a in enumerate(ids):
            for b in ids[i+1:]:
                overlap_count += 1
                assert a in ancestors[b] or b in ancestors[a], ('unordered write conflict', key,a,b)
    ca = json.loads((PACK/'tasks.json').read_text(encoding='utf-8'))
    for t in ca['tasks']:
        if t['id'] in data['superseded_aliases']:
            assert not t['active'] and t['status']=='SUPERSEDED'
            assert t['id'] not in by_id
            assert t['replacement_ids']==data['superseded_aliases'][t['id']]
            for n in t['replacement_ids']: assert n in by_id
        else:
            assert t['depends_on']==by_id[t['id']]['depends_on'], ('CA mirror mismatch',t['id'])
            assert t['status']==by_id[t['id']]['status'], ('CA status mismatch',t['id'])
    accepted = json.loads((PACK/'reviews/ACCEPTED-LOCAL-2026-09-06.json').read_text(encoding='utf-8'))['packets']
    satisfied = {'DOC_COMPLETE', 'ACCEPTED_LOCAL'}
    for t in tasks:
        if t['status'] != 'ACCEPTED_LOCAL': continue
        assert all(by_id[d]['status'] in satisfied for d in t['depends_on']), (t['id'], 'unaccepted dependency')
        evidence = accepted[t['id']]
        assert evidence['repository'] == t['repository']
        repo = REPOS[t['repository']]
        assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'], text=True).strip() == evidence['head']
        assert set(evidence['files']) == set(t['allowlist']), (t['id'], 'acceptance coverage')
        for path, expected in evidence['files'].items():
            assert hashlib.sha256((repo/path).read_bytes()).hexdigest() == expected, (t['id'], 'accepted snapshot drift', path)
    ready = [t for t in tasks if t['status'] not in satisfied and all(by_id[d]['status'] in satisfied for d in t['depends_on'])]
    source=json.loads((PACK/'SOURCE-INVENTORY.json').read_text(encoding='utf-8'))
    source_drift = []
    for item in source['sources']:
        actual = hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()
        if actual != item['sha256']:
            source_drift.append({'path': item['path'], 'baseline': item['sha256'], 'current': actual})
    assert len(re.findall(r'^### F\d\d', (PACK/'PRODUCT-SPEC.md').read_text(encoding='utf-8'),re.M))==15
    # New/rewritten documentation links only; old historical body links aren't
    # silently promoted into a current acceptance claim.
    docs=list(PACK.glob('product-packets/*.md'))+[PACK/n for n in ['EXECUTION.md','README.md','PRODUCT-TASKS.md','PACKETS.md','COVERAGE.md','PRODUCT-SPEC.md','CMS-SPEC.md','TOOLING.md','RECONCILIATION.md']]
    links=0
    for f in docs:
        assert f.exists(), f
        for target in re.findall(r'\]\(([^)]+)\)',f.read_text(encoding='utf-8')):
            if target.startswith(('http:','https:','#')):continue
            path=target.split('#')[0]
            assert (f.parent/path).exists(), ('broken link',f.name,target)
            links+=1
    git_checks={}
    for name,repo in REPOS.items():
        r=subprocess.run(['git','-C',str(repo),'-c','core.safecrlf=false','diff','--check'],capture_output=True,text=True)
        assert r.returncode==0,(name,r.stdout,r.stderr)
        tracked=subprocess.check_output(['git','-C',str(repo),'diff','--name-only'],text=True,stderr=subprocess.DEVNULL).splitlines()
        untracked = subprocess.check_output(['git','-C',str(repo),'ls-files','--others','--exclude-standard'],text=True).splitlines() if name != 'ROOT' else []
        runtime_paths = [p for p in tracked + untracked if not p.endswith('.md') and '__pycache__/' not in p]
        if name!='ROOT':
            # Packets under active rework own their allowlisted runtime files,
            # whether review-flagged (REVISE) or implemented-but-unreviewed
            # (IMPLEMENTED_UNREVIEWED: code + local checks, uncommitted, not
            # owner-accepted). Anything else is an unassigned product change.
            active_paths = {p for t in tasks if t['repository']==name and t['status'] in {'REVISE', 'IMPLEMENTED_UNREVIEWED', 'ACCEPTED_LOCAL'} for p in t['allowlist']}
            assert all(p in active_paths for p in runtime_paths),(name,'unassigned product change',runtime_paths)
        else:
            # ROOT owns docs/governance plus the staging runner topology through
            # its active packets (same active-rework rule as the other repos).
            root_active = {p for t in tasks if t['repository']=='ROOT' and t['status'] in {'REVISE', 'IMPLEMENTED_UNREVIEWED', 'ACCEPTED_LOCAL'} for p in t['allowlist']}
            assert all(p.startswith('Docs/') or p in {'AGENTS.md','PROJECT-MANIFEST.md'} or p in root_active for p in tracked), ('root runtime modified',tracked)
        git_checks[name]={'diff_check':'PASS','tracked_changed_files':len(tracked),'packet_runtime_changes_present':bool(runtime_paths) if name!='ROOT' else False}
    pending=[t['id'] for t in tasks if t['status']=='REVISE']
    result={'status':'PASS', 'acceptance_status':'OPEN', 'status_counts':{state:sum(t['status']==state for t in tasks) for state in sorted({t['status'] for t in tasks})}, 'ready_for_review':[t['id'] for t in ready if t['status']=='IMPLEMENTED_UNREVIEWED'], 'ready_for_revision':[t['id'] for t in ready if t['status']=='REVISE'], 'ready_to_start':[t['id'] for t in ready if t['status'] in {'NOT_STARTED','BLOCKED'}],'validation_scope':'plan structure only; source drift and revisions are not implementation acceptance','pending_revisions':pending,'source_baseline_drift':source_drift,'task_count':len(tasks),'documentation_complete':sum(t['status']=='DOC_COMPLETE' for t in tasks),'runtime_not_started':sum(t['status']=='NOT_STARTED' for t in tasks),'page_families':15,'retired_CA_aliases':len(data['superseded_aliases']),'allowlist_entries':path_count,'serialized_overlap_pairs':overlap_count,'unchanged_source_hashes':len(source['sources'])-len(source_drift),'checked_local_links':links,'git':git_checks,'runtime_tests_run':False,'publication_acceptance':'OPEN','visual_acceptance':'OPEN'}
    (PACK/'RECONCILIATION-CHECK.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))

if __name__=='__main__': main()
