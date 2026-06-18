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

Then deploy pods and CRDs
```bash
flux install

# verify install
kubectl get crds | grep toolkit
kubectl get pods -n flux-system
```

## Bootstrap Flux
```bash
export GITHUB_USER="YOUR_GITHUB_USER"
export GITHUB_REPO="infra-gitops"

flux check --pre

flux bootstrap github \
  --owner=$GITHUB_USER \
  --repository=$GITHUB_REPO \
  --branch=main \
  --path=clusters/docker-desktop \
  --personal
```
Paste your PAT when prompted.

## Flux Commands

Observe all your resources:
```bash
flux get all -A

# or continuously watch

flux get all -A --watch
```

Independent Resources:
```bash
flux get sources all

flux get kustomizations # shorthand ks

flux get helmreleases # shorthand hr
```

Reconcile commands:
```bash
flux reconcile kustomization arc-controller --with-source -n flux-system
flux reconcile kustomization arc-runners --with-source -n flux-system
```