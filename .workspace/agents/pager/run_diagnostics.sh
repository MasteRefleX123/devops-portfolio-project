#!/usr/bin/env bash
set -euo pipefail

echo "=== PAGER Diagnostics ==="
date '+%F %T %Z'
echo "Shell: ${SHELL:-unknown}"
uname -a || true

echo
echo "--- Environment ---"
printf "PAGER=%q\nGIT_PAGER=%q\nMANPAGER=%q\nAWS_PAGER=%q\nLESS=%q\n" "${PAGER-}" "${GIT_PAGER-}" "${MANPAGER-}" "${AWS_PAGER-}" "${LESS-}"

echo
echo "--- Git ---"
git --version 2>/dev/null || true
git rev-parse --is-inside-work-tree 2>/dev/null && echo "Inside git repo: yes" || echo "Inside git repo: no"
git config --get core.pager 2>/dev/null || true
git config --global --get core.pager 2>/dev/null || true
git config --system --get core.pager 2>/dev/null || true
git var GIT_PAGER 2>/dev/null || true

echo
echo "--- Commands presence ---"
command -v less 2>/dev/null && { less --version 2>/dev/null | head -1; } || echo "less: not found"
for alt in delta bat most moar more; do
  if command -v "$alt" >/dev/null 2>&1; then
    echo "found: $alt => $(command -v "$alt")"
  fi

done

echo
echo "--- Aliases (subset) ---"
alias 2>/dev/null | grep -E '\\b(less|more|cat|git|aws|kubectl)\\b' || true

echo
echo "--- AWS CLI ---"
aws --version 2>/dev/null || true
aws configure list 2>/dev/null || true

echo
echo "--- Safe sample commands (no pager flags) ---"
git --no-pager status -s 2>/dev/null | head -10 || true
git --no-pager log -1 --oneline 2>/dev/null || true
aws --no-cli-pager sts get-caller-identity 2>/dev/null || true
man -P cat echo 2>/dev/null | head -5 || true

echo
echo "Diagnostics complete. Attach this output to RESPONSES.md (or save under reports/)."
