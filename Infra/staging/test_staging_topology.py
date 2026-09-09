from pathlib import Path
import unittest


STAGING_DIR = Path(__file__).resolve().parent


class StagingTopologyTest(unittest.TestCase):
    def test_compose_publishes_loopback_diagnostics_and_shared_edge_aliases(self) -> None:
        compose = (STAGING_DIR / "docker-compose.stage.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn("https://staging.tahamohamadi.ir", compose)
        self.assertNotIn("https://tahamohamadi.ir}", compose)
        self.assertIn('"127.0.0.1:28001:8000"', compose)
        self.assertIn('"127.0.0.1:23080:8080"', compose)
        self.assertIn('"127.0.0.1:23081:8080"', compose)
        self.assertIn("name: host-edge", compose)
        self.assertIn("taha-stage-cms", compose)
        self.assertIn("taha-stage-web", compose)
        self.assertIn("taha-stage-admin", compose)

    def test_caddy_uses_compose_edge_aliases_and_blocks_internal_api(self) -> None:
        caddy = (STAGING_DIR / "Caddyfile.staging.fragment").read_text(
            encoding="utf-8"
        )

        self.assertIn("# BEGIN TAHA STAGING MANAGED", caddy)
        self.assertIn("# END TAHA STAGING MANAGED", caddy)
        self.assertIn("reverse_proxy taha-stage-cms:8000", caddy)
        self.assertIn("reverse_proxy taha-stage-web:8080", caddy)
        self.assertIn("reverse_proxy taha-stage-admin:8080", caddy)
        self.assertIn('respond "Not Found" 404', caddy)


if __name__ == "__main__":
    unittest.main()
