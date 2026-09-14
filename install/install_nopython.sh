#!/bin/sh
# Pure-shell installer for spinnerVerbs -- no Python required.
# Linux/macOS equivalent of install_nopython.bat. Only POSIX tools are used
# (sh, sed, grep, wc, mktemp) -- no bash-only features, no jq/python.
#
# Usage:
#   ./install_nopython.sh                                (global scope, replace mode)
#   ./install_nopython.sh project                         (this directory, replace mode)
#   ./install_nopython.sh project /my/project             (explicit project dir, replace mode)
#   ./install_nopython.sh global append                   (global scope, append mode)
#   ./install_nopython.sh project /my/project append      (any order/combination works)
#
# ASSUMPTION: an existing settings.json (if any) is standard pretty-printed
# JSON (like Node's JSON.stringify(obj, null, 2)) with the root "}" as the
# very last line. This covers every settings.json Claude Code itself writes.
# If yours has been hand-edited unusually, use install.py/install.sh instead
# (more robust) -- this script backs up your file first regardless, so it's
# safe to try.
#
# SAFETY: shell has no real JSON parser here, so this script can only do a
# rough line-count sanity check after writing (the merged file should never
# end up SHORTER than the original -- if it does, the original is left
# untouched and nothing is overwritten). This is weaker than install.py's
# exact key-by-key verification, which actually re-parses both files and
# confirms every original key's VALUE is untouched -- prefer install.py when
# you want the strongest guarantee that no existing custom setting
# (statusLine, hooks, permissions, etc.) was lost.

set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VERBS_FILE="$SCRIPT_DIR/../data/spinnerVerbs.settings.json"

if [ ! -f "$VERBS_FILE" ]; then
    echo "Klaida: nerandu $VERBS_FILE - paleisk sita skripta is repo katalogo."
    exit 1
fi

SCOPE="global"
MODE="replace"
PROJ_DIR=""

for arg in "$@"; do
    case "$arg" in
        global) SCOPE="global" ;;
        project) SCOPE="project" ;;
        replace) MODE="replace" ;;
        append) MODE="append" ;;
        *) PROJ_DIR="$arg" ;;
    esac
done

if [ "$SCOPE" = "project" ]; then
    [ -z "$PROJ_DIR" ] && PROJ_DIR="$(pwd)"
    TARGET="$PROJ_DIR/.claude/settings.json"
else
    TARGET="$HOME/.claude/settings.json"
fi

echo "Diegimo apzvalga:"
echo "  Apimtis (scope): $SCOPE"
if [ "$SCOPE" = "project" ]; then
    echo "  Projekto katalogas: $PROJ_DIR"
fi
echo "  Mode: $MODE"
echo "  Tikslo failas: $TARGET"
echo
echo "Nera Python priklausomybiu -- viskas atliekama grynu shell tekstu."
echo "Jei tikslo faile jau yra kitu nustatymu, jie NEBUS istrinti; failas bus"
echo "sujungtas, o originalas issaugotas kaip .bak.N pries rasant."
echo
printf "Testi? (Y/n): "
read -r CONFIRM
case "$CONFIRM" in
    [nN]*)
        echo "Atsaukta, niekas nepakeista."
        exit 0
        ;;
esac

mkdir -p "$(dirname "$TARGET")"

# Find an unused numbered backup name (.bak.1, .bak.2, ... -- never overwrite
# an earlier backup).
BN=0
BACKUP=""
while :; do
    BN=$((BN + 1))
    CANDIDATE="$TARGET.bak.$BN"
    if [ ! -e "$CANDIDATE" ]; then
        BACKUP="$CANDIDATE"
        break
    fi
done

TMP_BODY="$(mktemp)"
TMP_NEW="$(mktemp)"
trap 'rm -f "$TMP_BODY" "$TMP_NEW"' EXIT INT TERM

NEED_FRESH=0
if [ ! -f "$TARGET" ]; then
    NEED_FRESH=1
    TLINES=0
    : > "$TMP_BODY"
else
    echo "Radau esama settings.json - darau atsargine kopija."
    if grep -q '"spinnerVerbs"' "$TARGET"; then
        echo 'DEMESIO: faile jau yra "spinnerVerbs" raktas. Sis skriptas nezino'
        echo "kaip pilnai issitrinti seno rakto teksto, tad prides NAUJA"
        echo "spinnerVerbs bloka po juo. JSON liks galiojantis ir naujausias"
        echo "blokas galios, bet jei nori svaraus failo, isvalyk sena bloka"
        echo "rankiniu budu po sio veiksmo (originalas issaugotas .bak faile)."
        echo
    fi
    cp "$TARGET" "$BACKUP"
    echo "Atsargine kopija: $BACKUP"

    TLINES=$(wc -l < "$TARGET" | tr -d ' ')

    # All lines except the opening "{" and the final "}" (the root braces --
    # both get re-added when the new file is assembled below).
    sed '1d;$d' "$TARGET" > "$TMP_BODY"

    # Give the new last line (the previous last real key) a trailing comma
    # if it doesn't already have one.
    LAST_LINE="$(tail -n 1 "$TMP_BODY" 2>/dev/null || true)"
    case "$LAST_LINE" in
        *,|"") : ;;
        *)
            sed '$s/$/,/' "$TMP_BODY" > "$TMP_NEW" && cp "$TMP_NEW" "$TMP_BODY"
            ;;
    esac
fi

# Append the spinnerVerbs block: every VERBS_FILE line except its first ("{")
# and its last ("}"), swapping "replace" -> "append" in the mode line if
# needed.
if [ "$MODE" = "replace" ]; then
    sed '1d;$d' "$VERBS_FILE" >> "$TMP_BODY"
else
    sed '1d;$d' "$VERBS_FILE" | sed 's/"replace"/"append"/' >> "$TMP_BODY"
fi

# The body already ends with the spinnerVerbs object's own closing "  }"
# line (preserved from VERBS_FILE), so only the root "}" needs adding here.
{
    echo "{"
    cat "$TMP_BODY"
    echo "}"
} > "$TMP_NEW"

# Safety check: a merge should never make the file SHORTER than the
# original (we only ever add content) -- if it did, something went wrong,
# so leave the original untouched and bail instead of overwriting it.
NEWLINES=$(wc -l < "$TMP_NEW" | tr -d ' ')

SAFE=1
if [ "$NEED_FRESH" -eq 1 ]; then
    [ "$NEWLINES" -lt 10 ] && SAFE=0
else
    [ "$NEWLINES" -le "$TLINES" ] && SAFE=0
fi

if [ "$SAFE" -eq 0 ]; then
    echo
    echo "KLAIDA: rezultatas atrodo neteisingas (per trumpas) - originalas NEPALIESTAS."
    if [ "$NEED_FRESH" -eq 0 ]; then
        echo "Atsargine kopija vis tiek issaugota: $BACKUP"
    fi
    exit 1
fi

mv "$TMP_NEW" "$TARGET"

echo
echo "Sekmingai irasyta i: $TARGET"
echo "mode: $MODE"
if [ "$NEED_FRESH" -eq 0 ]; then
    echo "Jei kazkas atrodo sugadinta - originalas issaugotas kaip $BACKUP"
fi
