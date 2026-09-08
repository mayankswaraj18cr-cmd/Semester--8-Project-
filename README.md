# Serverless Container Deployment Platform

A browser-based interactive concept demo for deploying and autoscaling containerized workloads on a serverless platform.

## Overview

This project presents a compact dashboard for exploring serverless container deployment. It demonstrates deployment status, resource scaling, architecture flow, runtime specifications, and activity logs in a single self-contained HTML page.

The repository also includes a dependency-free Python implementation of the autoscaling model shown in the dashboard. The Python module is intentionally small and easy to extend into a REST API, worker service, or cloud deployment controller.

## Features

- Interactive deployment simulation with live status and activity updates
- Adjustable container scaling controls and resource metrics
- Architecture overview and runtime specification panels
- Python autoscaling model with a command-line interface
- Unit tests for scale-up, scale-down, validation, and steady-state behavior
- Supporting research paper and presentation materials

## Project Structure

```
.
├── serverless_deployment_platform.html  # Interactive platform dashboard demo
├── src/
│   └── serverless_scaler.py              # Python autoscaling model and CLI
├── tests/
│   └── test_serverless_scaler.py         # Python unit tests
├── docs/
│   ├── Serverless_Platform_Research_Paper.pdf  # Research and problem framing
│   └── Serverless_Platform_Presentation.pptx   # Project presentation
├── assets/                               # Images and diagrams
├── LICENSE
└── README.md
```

## Getting Started

```bash
git clone https://github.com/mayankswaraj18cr-cmd/Semester--8-Project-.git
cd Semester--8-Project-
```

Open `serverless_deployment_platform.html` in a modern browser to view the demo. It has no build step or external dependencies.

### Run the Python model

Python 3.10 or newer is recommended. The model uses only the Python standard library, so no package installation is required.

```bash
python3 src/serverless_scaler.py --users 2500
```

The command prints a JSON deployment snapshot:

```json
{
	"users": 2500,
	"instances": 3,
	"cpu_percent": 79,
	"response_ms": 70,
	"status": "Scaling Up",
	"action": "Launch containers 2 through 3"
}
```

### Run the tests

```bash
python3 -m unittest discover -s tests -v
```

## Autoscaling Model

The model assumes that one container can serve up to 1,000 concurrent users. For every traffic measurement it:

1. Calculates the required capacity with `max(1, ceil(users / 1000))`.
2. Estimates CPU utilization from the traffic assigned to each active container.
3. Estimates response time when CPU utilization passes 80 percent.
4. Compares the required capacity with the previous state and reports a scale-up, scale-down, or steady-state action.

This is a simulation for academic demonstration. It does not create Docker containers, call AWS or GCP APIs, or persist metrics.

## Python API Example

```python
from src.serverless_scaler import ServerlessScaler

scaler = ServerlessScaler(users_per_container=1000)
snapshot = scaler.evaluate(2500)
print(snapshot.instances)  # 3
print(snapshot.status)     # Scaling Up
```

`ServerlessScaler.evaluate()` returns a `DeploymentSnapshot` dataclass containing the traffic level, instance count, CPU estimate, response-time estimate, current status, and recommended action.

## Development Notes

- Keep the scaling rules deterministic so the model is easy to test and compare with the dashboard.
- Extend `DeploymentSnapshot` when adding metrics that should be exposed by a future API.
- Keep cloud-provider integrations outside the core scaler so the calculation remains portable.
- Add tests before changing capacity thresholds or metric formulas.

## Documentation

- [Research Paper](docs/Serverless_Platform_Research_Paper.pdf) - background and problem framing
- [Presentation](docs/Serverless_Platform_Presentation.pptx) - project overview and findings

## Roadmap

- [ ] Connect the dashboard to a real deployment API
- [ ] Add persistent workload and metrics data

## License

MIT - see [LICENSE](LICENSE)

## Contact

Mayank Swaraj - [mayankswaraj18cr@gmail.com](mailto:mayankswaraj18cr@gmail.com)