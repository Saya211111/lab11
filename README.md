# Lab 11 GitHub Simulation

This project converts the original Lab 11 idea from GitLab + Cisco routers into:

- GitHub Actions instead of GitLab CI
- Python code instead of Cisco/CML routers
- CSV source of truth instead of manual configuration
- JSON files as simulated router running configuration

## Goal

When `interfaces.csv` changes, the pipeline runs `deploy_interfaces.py`.
The script reads the desired interface state and updates simulated routers under `simulated_devices/`.

## Run Locally

```powershell
python deploy_interfaces.py
python validate_interfaces.py
```

If your Windows `python` command points to the Microsoft Store, use the bundled runtime:

```powershell
& 'C:\Users\ihsan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' deploy_interfaces.py
& 'C:\Users\ihsan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' validate_interfaces.py
```

## GitHub Actions

Push this folder to a GitHub repository. The workflow in `.github/workflows/deploy-interfaces.yml` will run on every push or pull request.

## Lab 11 Mapping

| Original Lab 11 | This Simulation |
| --- | --- |
| GitLab project | GitHub repository |
| `.gitlab-ci.yml` | `.github/workflows/deploy-interfaces.yml` |
| GitLab Runner | GitHub Actions runner |
| Cisco IOS XE routers | JSON files in `simulated_devices/` |
| Ansible playbook | Python deployment script |
| `interfaces.csv` source of truth | Same concept, still CSV |
