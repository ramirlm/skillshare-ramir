#!/usr/bin/env python3
import json, pathlib, datetime

snap = pathlib.Path(__file__).resolve().parent
# default snapshot dir
import sys
out_dir = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('/tmp/avaliadora-workspace-snapshot')

cron_path = out_dir / 'cron-jobs.json'
status_path = out_dir / 'openclaw-status.json'

cron = {}
status = {}
try:
    cron = json.loads(cron_path.read_text())
except Exception:
    cron = {}
try:
    status = json.loads(status_path.read_text())
except Exception:
    status = {}

lines=[]
lines.append(f"# Avaliadora Workspace — Snapshot Report")
lines.append("")
lines.append(f"GeneratedAt: {datetime.datetime.now(datetime.timezone.utc).isoformat()}")
lines.append("")

# Cron summary
jobs = cron.get('jobs', []) if isinstance(cron, dict) else []
err = []
ok = 0
for j in jobs:
    st = (j.get('state') or {})
    lastStatus = st.get('lastStatus')
    if lastStatus == 'ok':
        ok += 1
    if lastStatus in ('error','skipped') and st.get('lastError'):
        err.append({
            'name': j.get('name'),
            'id': j.get('id'),
            'enabled': j.get('enabled'),
            'lastStatus': lastStatus,
            'lastError': st.get('lastError'),
            'consecutiveErrors': st.get('consecutiveErrors', 0),
            'lastRunAtMs': st.get('lastRunAtMs'),
            'nextRunAtMs': st.get('nextRunAtMs'),
            'delivery': j.get('delivery'),
        })

lines.append("## Cron jobs")
lines.append(f"- total: {len(jobs)}")
lines.append(f"- lastStatus ok: {ok}")
lines.append(f"- with errors: {len(err)}")
lines.append("")

if err:
    lines.append("### Errors (top)")
    for e in sorted(err, key=lambda x: (-(x.get('consecutiveErrors') or 0), x.get('name') or ''))[:20]:
        lines.append(f"- **{e['name']}** (enabled={e['enabled']}, consecutiveErrors={e['consecutiveErrors']}): {e['lastError']}")

# Vault-path grep
gv = (out_dir / 'grep-vault-paths.txt')
lines.append("")
lines.append("## Vault path footguns")
if gv.exists():
    txt = gv.read_text(errors='ignore').strip()
    if txt:
        lines.append("Found occurrences of '~/vault' or '/vault' in configs/scripts. Review file list in snapshot:")
        lines.append(f"- {gv}")
    else:
        lines.append("No occurrences found in scanned directories.")
else:
    lines.append("[UNVERIFIED] grep output missing")

print("\n".join(lines))