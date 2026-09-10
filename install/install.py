#!/usr/bin/env python3
"""
Installs the Lithuanian spinnerVerbs list into a Claude Code settings.json.

Usage (interactive):
    python install.py

Usage (non-interactive):
    python install.py --scope global --mode replace
    python install.py --scope project --project-dir /path/to/project --mode append

Merges into any existing settings.json instead of overwriting it -- only the
"spinnerVerbs" key is touched, every other key (statusLine, tui, theme,
enabledPlugins, custom hooks/permissions, etc.) is preserved byte-for-byte.
Writes a timestamped ".bak" backup before making any change, and verifies
after writing that nothing else was lost -- if anything looks wrong, the
original file is restored automatically and nothing is left half-broken.
"""
import argparse
import datetime
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


def load_existing(target):
    """Returns (dict, raw_text_or_None). Aborts loudly on malformed JSON
    instead of risking silent data loss by treating it as empty."""
    if not target.exists():
        return {}, None
    raw = target.read_text(encoding="utf-8")
    try:
        return json.loads(raw), raw
    except json.JSONDecodeError as e:
        print(f"Klaida: {target} egzistuoja, bet nėra tvarkingas JSON ({e}).")
        print("Nieko nekeičiu, kad neprarastum esamo turinio — pataisyk failą rankiniu")
        print("būdu (arba pervadink/pašalink, jei jis nebereikalingas) ir bandyk vėl.")
        sys.exit(1)


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

    existing, raw = load_existing(target)
    other_keys_before = {k: v for k, v in existing.items() if k != "spinnerVerbs"}

    backup = None
    if raw is not None:
        stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        backup = target.with_name(target.name + f".bak.{stamp}")
        backup.write_text(raw, encoding="utf-8")
        print(f"Atsarginė kopija: {backup}")

    verbs = load_verbs()
    existing["spinnerVerbs"] = {"mode": mode, "verbs": verbs}

    with open(target, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # Verify: re-read what we just wrote and confirm every OTHER key survived
    # untouched. If anything looks wrong, restore the original immediately --
    # never leave the user with a silently-broken settings.json.
    try:
        written = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        written = None

    problem = None
    if written is None:
        problem = "įrašytas failas pats savaime nėra tvarkingas JSON"
    else:
        for k, v in other_keys_before.items():
            if written.get(k) != v:
                problem = f"raktas \"{k}\" pasikeitė arba dingo po įrašymo"
                break

    if problem:
        print(f"\nKLAIDA po patikros: {problem}.")
        if backup is not None:
            shutil.copy2(backup, target)
            print(f"Atstatyta iš atsarginės kopijos: {backup}")
        else:
            target.unlink(missing_ok=True)
            print("Naujai sukurtas failas pašalintas.")
        print("Niekas neprarasta, bet spinnerVerbs NEBUVO įdiegtas. Praneškite apie šią klaidą.")
        sys.exit(1)

    print(f"\nSėkmingai įrašyta į: {target}")
    print(f"mode: {mode}, žodžių: {len(verbs)}")
    if other_keys_before:
        print(f"Kiti esami raktai išsaugoti nepaliesti: {', '.join(other_keys_before)}")
    print("Pakeitimas turėtų pritaikomas gyvai (be perkrovimo) veikiančiose Claude Code sesijose.")


if __name__ == "__main__":
    main()
