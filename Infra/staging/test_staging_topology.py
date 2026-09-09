from pathlib import Path
import unittest


STAGING_DIR = Path(__file__).resolve().parent


class StagingTopologyTest(unittest.TestCase):
    def test_compose_publishes_only_isolated_loopback_ingress(self) -> None:
        compose = (STAGING_DIR / "docker-compose.stage.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn("https://staging.tahamohamadi.ir", compose)
        self.assertNotIn("https://tahamohamadi.ir}", compose)
        self.assertIn('"127.0.0.1:18001:8000"', compose)
        self.assertIn('"127.0.0.1:13080:8080"', compose)
        self.assertIn('"127.0.0.1:13081:8080"', compose)

    def test_caddy_uses_the_loopback_ingress_and_blocks_internal_api(self) -> None:
        caddy = (STAGING_DIR / "Caddyfile.staging.fragment").read_text(
            encoding="utf-8"
        )

        self.assertIn("# BEGIN TAHA STAGING MANAGED", caddy)
        self.assertIn("# END TAHA STAGING MANAGED", caddy)
        self.assertIn("reverse_proxy 127.0.0.1:18001", caddy)
        self.assertIn("reverse_proxy 127.0.0.1:13080", caddy)
        self.assertIn("reverse_proxy 127.0.0.1:13081", caddy)
        self.assertIn('respond "Not Found" 404', caddy)
        self.assertNotIn("taha-cms-stage-", caddy)


if __name__ == "__main__":
    unittest.main()
