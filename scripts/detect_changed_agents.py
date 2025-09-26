#!/usr/bin/env python3
import argparse, json, os, subprocess, sys
p = argparse.ArgumentParser()
p.add_argument("--event", required=True)
p.add_argument("--base")
p.add_argument("--before")
p.add_argument("--head", required=True)
p.add_argument("--out", default=None)
a = p.parse_args()

def sh(cmd):
    return subprocess.check_output(cmd, text=True).strip()

# Ensure full history for comparisons
subprocess.run(["git","fetch","--quiet","--prune","--unshallow"], check=False)

base = None
if a.event == "pull_request" and a.base:
    base = a.base
elif a.before:
    base = a.before
else:
    # fallback: merge-base with origin/main
    try:
        sh(["git","fetch","--quiet","origin","+refs/heads/*:refs/remotes/origin/*"])
        base = sh(["git","merge-base","origin/main", a.head])
    except Exception:
        base = a.head + "^"

files = sh(["git","diff","--name-only", f"{base}..{a.head}"]).splitlines()
agents = set()
for f in files:
    parts = f.split("/")
    if len(parts) >= 2 and parts[0] == "agents":
        agents.add(parts[1])

# Only keep directories that look like agents (have Dockerfile)
keepers = []
for ag in sorted(agents):
    if os.path.exists(os.path.join("agents", ag, "Dockerfile")):
        keepers.append(ag)

out = json.dumps(keepers)
# For job->job output
if a.out:
    with open(a.out, "a") as fh:
        fh.write(f"agents={out}\n")
else:
    print(out)
