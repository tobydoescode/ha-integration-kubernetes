# HA Kubernetes Integration

Home Assistant custom integration (HACS-compatible) that exposes Kubernetes Deployments and StatefulSets as HA devices.

## Commands

- `task sync` — install dependencies (uv)
- `task lint` — run ruff linter + format check
- `task lint:fix` — auto-fix lint/format issues
- `task test` — run pytest

## Architecture

- **Config flow** (`config_flow.py`): 2-step setup (paste kubeconfig, then set namespaces/label selector/interval). Options flow for post-setup changes triggers integration reload.
- **Coordinator** (`coordinator.py`): `DataUpdateCoordinator` subclass. Polls k8s API via `AppsV1Api` and `CoreV1Api` (for pod-level data). All k8s client calls are synchronous (urllib3) and must run via `hass.async_add_executor_job()`.
- **Entity base** (`entity.py`): Each Deployment/StatefulSet is an HA device. Entities attach via shared `device_info` identifiers.
- **Platforms**:
  - `sensor.py` — ready pods, desired replicas, available pods (Deployment only), container image, last restart time, pod restart count, last restart reason
  - `button.py` — rollout restart (patches pod template annotation)
  - `number.py` — replica count (0-50, patches scale subresource)

## Key conventions

- Label selector `homeassistant.io/managed=true` controls resource discovery (opt-in)
- Kubeconfig must use embedded cert data (`*-data` keys), not file path references
- Entity unique IDs include `entry.entry_id` to support multiple clusters
- Polling default: 30s, configurable 10-600s
- Tests mock `kubernetes.config.new_client_from_config_dict` and `kubernetes.client.AppsV1Api` directly (coordinator uses lazy imports)
- Tests use `coordinator.async_refresh()` not `async_config_entry_first_refresh()` (avoids config entry state checks)
