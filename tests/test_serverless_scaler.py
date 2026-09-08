import unittest

from src.serverless_scaler import ServerlessScaler


class ServerlessScalerTests(unittest.TestCase):
    def test_keeps_one_container_for_light_traffic(self):
        snapshot = ServerlessScaler().evaluate(100)

        self.assertEqual(snapshot.instances, 1)
        self.assertEqual(snapshot.status, "Running")
        self.assertEqual(snapshot.action, "No capacity change")

    def test_scales_up_at_capacity_boundary(self):
        scaler = ServerlessScaler()
        scaler.evaluate(100)

        snapshot = scaler.evaluate(2_500)

        self.assertEqual(snapshot.instances, 3)
        self.assertEqual(snapshot.status, "Scaling Up")
        self.assertIn("Launch containers", snapshot.action)

    def test_scales_down_when_traffic_falls(self):
        scaler = ServerlessScaler()
        scaler.evaluate(2_500)

        snapshot = scaler.evaluate(500)

        self.assertEqual(snapshot.instances, 1)
        self.assertEqual(snapshot.status, "Scaling Down")

    def test_rejects_negative_traffic(self):
        with self.assertRaises(ValueError):
            ServerlessScaler().evaluate(-1)


if __name__ == "__main__":
    unittest.main()