"""Autoscaling model for the serverless container deployment demo."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from math import ceil


@dataclass(frozen=True)
class DeploymentSnapshot:
    """The deployment state after processing one traffic measurement."""

    users: int
    instances: int
    cpu_percent: int
    response_ms: int
    status: str
    action: str


class ServerlessScaler:
    """Calculate container capacity and simulated runtime metrics."""

    def __init__(self, users_per_container: int = 1_000) -> None:
        if users_per_container < 1:
            raise ValueError("users_per_container must be positive")
        self.users_per_container = users_per_container
        self.current_instances = 1

    def evaluate(self, users: int) -> DeploymentSnapshot:
        """Return the deployment state needed for the supplied user count."""
        if users < 0:
            raise ValueError("users must not be negative")

        required_instances = max(1, ceil(users / self.users_per_container))
        cpu_percent = min(
            96,
            round(
                (users / (required_instances * self.users_per_container)) * 85
            )
            + 8,
        )
        response_ms = round(70 + max(0, cpu_percent - 80) * 6)

        if required_instances > self.current_instances:
            status = "Scaling Up"
            action = (
                f"Launch containers {self.current_instances + 1} through "
                f"{required_instances}"
            )
        elif required_instances < self.current_instances:
            status = "Scaling Down"
            action = f"Terminate idle containers; scale to {required_instances}"
        else:
            status = "Running"
            action = "No capacity change"

        self.current_instances = required_instances
        return DeploymentSnapshot(
            users=users,
            instances=required_instances,
            cpu_percent=cpu_percent,
            response_ms=response_ms,
            status=status,
            action=action,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simulate serverless container autoscaling."
    )
    parser.add_argument(
        "--users",
        type=int,
        default=100,
        help="Concurrent users to evaluate (default: 100).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    snapshot = ServerlessScaler().evaluate(args.users)
    print(json.dumps(asdict(snapshot), indent=2))


if __name__ == "__main__":
    main()