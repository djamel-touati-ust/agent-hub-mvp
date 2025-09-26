#!/usr/bin/env python3
"""
Fail CI if any agent is missing README.md or if README lacks required sections.
Rules:
- Every folder under agents/ containing src/ must include README.md
- README must mention both "A2A" and "MCP" (case-insensitive)
- Helpful: ensure JSON-RPC example (message/send) and Claude config path mentioned
"""
import os, sys, re

AGENTS_DIR = "agents"
required_readme_markers = [
    re.compile(r"\bA2A\b", re.I),
    re.compile(r"\bMCP\b", re.I),
]
recommended_markers = [
    re.compile(r"message/send", re.I),
    re.compile(r"claude_desktop_config\.json", re.I),
]

def main():
    errors = 0
    if not os.path.isdir(AGENTS_DIR):
        print(f"[WARN] No '{AGENTS_DIR}' dir found")
        sys.exit(0)

    for name in sorted(os.listdir(AGENTS_DIR)):
        path = os.path.join(AGENTS_DIR, name)
        if not os.path.isdir(path):
            continue
        # Heuristic: treat as agent if it has a src/ folder
        if not os.path.isdir(os.path.join(path, "src")):
            continue

        readme = os.path.join(path, "README.md")
        if not os.path.isfile(readme):
            print(f"[ERROR] {name}: missing README.md")
            errors += 1
            continue

        text = open(readme, "r", encoding="utf-8").read()

        for rx in required_readme_markers:
            if not rx.search(text):
                print(f"[ERROR] {name}: README.md missing required section: {rx.pattern}")
                errors += 1

        # Non-fatal hints (won't fail CI, just prints)
        for rx in recommended_markers:
            if not rx.search(text):
                print(f"[HINT]  {name}: consider adding '{rx.pattern}' to README.md")

    if errors:
        print(f"[FAIL] README checks failed with {errors} error(s).")
        sys.exit(1)
    print("[OK] All agent READMEs present with required sections.")

if __name__ == "__main__":
    main()
