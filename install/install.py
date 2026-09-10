#!/usr/bin/env python3
"""
Installs the Lithuanian spinnerVerbs list into a Claude Code settings.json.

Usage (interactive):
    python install.py

Usage (non-interactive):
    python install.py --scope global --mode replace
    python install.py --scope project --project-dir /path/to/project --mode append

Merges into any existing settings.json instead of overwriting it, and writes a
".bak" backup of the original file (if one existed) before making changes.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VERBS_FILE = SCRIPT_DIR.parent / "data" / "spinnerVerbs.settings.json"


def load_verbs():
    with open(VERBS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return data["spinnerVerbs"]["verbs"]


def prompt_choice(question, options):
    labels = "/".join(options)
    while True:
        answer = input(f"{question} ({labels}): ").strip().lower()
        if answer in options:
            return answer
        print(f"  Prašau įvesti vieną iš: {labels}")


def resolve_target_path(scope, project_dir):
    if scope == "global":
        return Path.home() / ".claude" / "settings.json"
    base = Path(project_dir).resolve() if project_dir else Path.cwd()
    return base / ".claude" / "settings.json"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", choices=["global", "project"], help="global = ~/.claude/settings.json, project = <dir>/.claude/settings.json")
    parser.add_argument("--mode", choices=["replace", "append"], help="replace = only LT verbs, append = LT + EN defaults mixed")
    parser.add_argument("--project-dir", help="Project directory to use with --scope project (default: current directory)")
    args = parser.parse_args()

    if not VERBS_FILE.exists():
        print(f"Klaida: nerandu {VERBS_FILE} — paleisk skriptą iš repo katalogo.")
        sys.exit(1)

    scope = args.scope or prompt_choice(
        "Kur diegti — globaliai visam kompiuteriui (global), ar tik vienam projektui (project)?",
        ["global", "project"],
    )
    mode = args.mode or prompt_choice(
        "Rodyti TIK lietuviškus žodžius (replace), ar sumaišyti su angliškais (append)?",
        ["replace", "append"],
    )

    target = resolve_target_path(scope, args.project_dir)
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists():
        backup = target.with_suffix(target.suffix + ".bak")
        shutil.copy2(target, backup)
        print(f"Atsarginė kopija: {backup}")
        with open(target, encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = {}

    verbs = load_verbs()
    existing["spinnerVerbs"] = {"mode": mode, "verbs": verbs}

    with open(target, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\nSėkmingai įrašyta į: {target}")
    print(f"mode: {mode}, žodžių: {len(verbs)}")
    print("Pakeitimas turėtų pritaikomas gyvai (be perkrovimo) veikiančiose Claude Code sesijose.")


if __name__ == "__main__":
    main()
