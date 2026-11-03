# Almaz topology reference

Last verified from live state and docs pass: 2026-06-06; OS baseline updated from the Machinum Almaz briefing (live check 2026-11-03). Refresh live state before critical operations. Fleet-wide canonical facts live in Machinum on Kvant.

## Host roles

| Host | Address | Role | Keep here |
| --- | --- | --- | --- |
| `almaz` | `10.0.0.200` | Public edge/security/storage/media/GPU/automation host | Caddy, Cloudflared, Authelia, Technitium, wg-easy, media, Immich, n8n, Ollama, SnapRAID/MergerFS, almaz backups |
| `nuc` | `10.0.0.56` | Internal Docker app/data/dashboard host | productivity apps, project apps, dashboards, `ntfy`, local collectors |
| `dozor` | `10.0.0.57` | Central monitoring/alerting host | Prometheus/alerting, Blackbox probes, fallback DNS |
| `volga` | `10.0.0.1` | Router with USB drive treated as remote-ish backup target | router USB restic repositories for nuc and almaz |

Recommended traffic shape:

```text
Internet → Cloudflare Tunnel/Caddy/Authelia on almaz → almaz services or selected nuc-backed routes
```

Do not broadly rebalance services. Prefer host-specific ownership and explicit migration plans.

## Almaz baseline

- Hostname: `almaz`
- OS: Debian 13 (trixie) since 2026-11-03; apt only. Ubuntu 26.04 was deleted the same day and there is no fallback OS.
- Kernel at cutover: `6.12.115+deb13.1-amd64`
- Hardware: ASUS Z170-A desktop/server, x86_64, NVIDIA GeForce GTX 1080
- NVIDIA: driver `580.159.03`, an NVIDIA installer build with DKMS (not an apt package), so kernel updates depend on DKMS rebuilding it
- History: on Ubuntu, kernel `7.0.0-22-generic` caused GTX 1080 `NVRM Xid 79` failures (2026-06-06). That kernel line no longer exists on this host.
- Docker: Docker CE `29.9.2` from the Docker Debian repository (2026-11-03)
- Display/login: `greetd`; Sway/SwayFX/kitty path documented in `terminal-and-desktop.md`

## Storage

- Root: LVM/ext4
- Service SSD: `/mnt/spektr`; `/opt/server` symlink points to `/mnt/spektr/server`
- MergerFS library mount: `/mnt/arkhiv`
- Data disks: `/mnt/kamera1`, `/mnt/kamera2`, `/mnt/kamera3`
- SnapRAID parity: `/mnt/rezerv`
- Extra ext4 mount: `/mnt/impuls`
- SnapRAID config: `/etc/snapraid.conf`

Latest storage audit notes:

- SnapRAID no errors detected.
- 227 updated files pending sync at audit.
- 48% of array not scrubbed.
- 5,079 zero-subsecond timestamp files; run `snapraid touch` before next sync if approved.
- No SnapRAID timer existed at audit.

## Backups

- Primary almaz router backup: `almaz-router-restic-backup.timer`.
- Repo: `sftp:root@10.0.0.1:/tmp/mountd/disk1_part1/almaz-restic`.
- SSH alias `volga` works for the user; root-run script uses equivalent explicit `root@10.0.0.1` and `/home/onnwee/.ssh/id_ed25519`.
- First successful restic snapshot: `57a6929e`, timestamp tag `20260518T201532Z`, source size `68.097 GiB`, stored `33.377 GiB`.
- Borgmatic container still exists but is secondary/untrusted until stale lock and migrated DB entries are cleaned up.

## Current service posture

- Health check script: `/usr/local/sbin/almaz-health-check.sh`.
- Health check timer: `almaz-health-check.timer`.
- Health checks should verify apt/dpkg, failed units, mounts, Docker health, critical containers, NVIDIA, and SnapRAID quick status.
- Kernel/NVIDIA health checks should confirm `uname -r`, that `dkms status` lists the NVIDIA module for that kernel, and that `nvidia-smi` succeeds.
- Critical post-upgrade fix: `wg-easy` needs `/lib/modules:/lib/modules:ro` in compose.

## Active documentation anchors

- Docs root: `/home/onnwee/docs/almaz`
- Host duties: `/home/onnwee/docs/almaz/infrastructure/host-duties.md`
- Storage audit: `/home/onnwee/docs/almaz/infrastructure/storage-audit-2026-05-18.md`
- Backup runbook: `/home/onnwee/docs/almaz/runbooks/backups.md`
- Post-upgrade health: `/home/onnwee/docs/almaz/runbooks/post-upgrade-health.md`
- Maintenance cadence: `/home/onnwee/docs/almaz/runbooks/maintenance-cadence.md`
- Fragile services: `/home/onnwee/docs/almaz/runbooks/fragile-services.md`
- NVIDIA/kernel incident: `/home/onnwee/docs/almaz/journal/2026-06-06.md`
