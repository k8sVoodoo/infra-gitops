# Bootstrapping

## Deploy Github Kubernetes Secret manually

If you want to use a secrets manager or SOPS you can do that as well.
```bash
kubectl create secret generic controller-manager \
  -n runners \
  --from-literal=github_token=YOUR_GITHUB_PAT
```

## Flux Install

### Install the CLI
| Operating System | Package Manager         | Command                                             |
| ---------------- | ----------------------- | --------------------------------------------------- |
| macOS            | Homebrew                | `brew install fluxcd/tap/flux`                      |
| Linux            | Official Install Script | `curl -s https://fluxcd.io/install.sh \| sudo bash` |
| Windows          | Chocolatey              | `choco install flux`                                |
| Windows          | Winget                  | `winget install FluxCD.Flux`                        |
| Windows          | Scoop                   | `scoop install flux`                                |


## Bootstrap Flux
```bash
export GITHUB_USER="YOUR_GITHUB_USER"
export GITHUB_REPO="infra-gitops"

flux bootstrap github \
  --owner=$GITHUB_USER \
  --repository=$GITHUB_REPO \
  --branch=main \
  --path=clusters/docker-desktop \
  --personal
```
