import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const readJson = (name) => JSON.parse(fs.readFileSync(path.join(here, name), "utf8"));
const fail = (message) => { throw new Error(message); };

const tokens = readJson("tokens.json");
const components = readJson("components.json");
const templates = readJson("templates.json");
const assets = readJson("assets.json");
const manifest = readJson("figma-plugin/manifest.json");
const plugin = fs.readFileSync(path.join(here, "figma-plugin/code.js"), "utf8");
const authority = JSON.parse(fs.readFileSync(path.join(root, "AUTHORITY-MANIFEST.json"), "utf8"));
const aliases = JSON.parse(fs.readFileSync(path.join(root, "ALIASES.json"), "utf8"));
const sha256 = (file) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const checksums = fs.readFileSync(path.join(root, "SHA256SUMS.txt"), "utf8").trim().split(/\r?\n/).filter(Boolean);

if (tokens.authority.runtime !== null) fail("Greenfield runtime authority must remain null before scaffold");
if (tokens.authority.contract !== "Docs/04-design/DESIGN-SYSTEM-SPEC.md") fail("Design contract path drifted");
if (tokens.semanticLight.status !== "design-approved") fail("Light token status must be design-approved");
if (tokens.semanticDark.status !== "design-approved") fail("Dark token status must be design-approved");
if (components.components.length !== 24) fail(`Expected 24 components, found ${components.components.length}`);
if (templates.templates.length !== 6) fail(`Expected 6 templates, found ${templates.templates.length}`);
if (templates.prototypePath.length !== 6) fail("Prototype path must contain six bounded steps");
if (manifest.networkAccess.allowedDomains[0] !== "none") fail("Figma plugin must remain offline");
for (const name of ["00 — Foundations & Library", "10 — Templates & Screens", "20 — Prototype & Handoff"]) {
  if (!plugin.includes(name)) fail(`Plugin page missing: ${name}`);
}
if (!plugin.includes('const OWNER = "TFL /"')) fail("Deterministic ownership prefix missing");
for (const asset of assets.assets) {
  const target = path.resolve(root, asset.path);
  if (!fs.existsSync(target)) fail(`Missing asset reference: ${asset.path}`);
}
for (const required of authority.required_files) {
  const target = path.join(root, required);
  if (!fs.existsSync(target)) fail(`Missing authority file: ${required}`);
}
for (const alias of aliases.aliases) {
  const canonical = path.join(root, alias.canonical_path);
  if (!fs.existsSync(canonical)) fail(`Missing alias canonical: ${alias.canonical_path}`);
}
for (const line of checksums) {
  const match = /^([a-f0-9]{64})  (.+)$/.exec(line);
  if (!match) fail(`Invalid SHA256SUMS line: ${line}`);
  const target = path.join(root, match[2]);
  if (!fs.existsSync(target)) fail(`Checksum path missing: ${match[2]}`);
  if (sha256(target) !== match[1]) fail(`Checksum mismatch: ${match[2]}`);
}
const seen = new Map();
for (const file of authority.required_files.filter((value) => value.endsWith(".png"))) {
  const digest = sha256(path.join(root, file));
  if (seen.has(digest)) fail(`Duplicate canonical image hash: ${file} and ${seen.get(digest)}`);
  seen.set(digest, file);
}
if (manifest.networkAccess.allowedDomains[0] !== "none") fail("Figma plugin must remain offline");

console.log(`PASS: ${components.components.length} components, ${templates.templates.length} templates, ${assets.assets.length} asset references, ${authority.required_files.length} required files, ${checksums.length} binary checksums, ${aliases.aliases.length} aliases, offline Figma builder.`);
