#!/usr/bin/env bash
set -euo pipefail

TS=$(date -Is)
HOST=$(hostname)

# Files to check (only if present)
SHELL_FILES=(
  "$HOME/.bashrc"
  "$HOME/.bash_profile"
  "$HOME/.bash_login"
  "$HOME/.profile"
  "$HOME/.zshrc"
  "$HOME/.zprofile"
  "$HOME/.zshenv"
)

# High-signal suspicious patterns (keep tight to reduce false positives)
SUSP_RE='(node[[:space:]]+-e|eval[[:space:]]*\(.*atob|atob\(|base64[^\n]*decode|curl[^\n]*\|[^\n]*(sh|bash)|wget[^\n]*\|[^\n]*(sh|bash)|python[[:space:]]+-c|perl[[:space:]]+-e|ruby[[:space:]]+-e|\.node_modules|/tmp/tmp[0-9A-F]+\.tmp|C250617A|C250618A|\[\x27_V\x27\]|\[\x27_H\x27\]|_\$af)'

# Secret env var exposure (report names only)
SECRET_ENV_RE='^[[:space:]]*(export[[:space:]]+)?([A-Z0-9_]+(API_KEY|ACCESS_TOKEN|SECRET|TOKEN|PASSWORD|PRIVATE_KEY))='

print_section() {
  echo
  echo "## $1"
}

echo "Daily Security Triage"
echo "Timestamp: $TS"
echo "Host: $HOST"

print_section "Shell profile injection indicators"
found_any=0
for f in "${SHELL_FILES[@]}"; do
  [[ -f "$f" ]] || continue
  # Ignore commented lines to reduce false positives
  hits=$(grep -nE "$SUSP_RE" "$f" 2>/dev/null | grep -vE '^[0-9]+:[[:space:]]*#' || true)
  if [[ -n "$hits" ]]; then
    found_any=1
    echo "- $f"
    echo "$hits" | head -20 | sed 's/^/    /'
  fi

done
if [[ $found_any -eq 0 ]]; then
  echo "No suspicious injection patterns found in shell profiles."
fi

print_section "Secret-like env vars present in shell profiles (names only)"
secret_any=0
for f in "${SHELL_FILES[@]}"; do
  [[ -f "$f" ]] || continue
  while IFS= read -r line; do
    # line format from grep -n: "<lno>:<content>"
    lno=${line%%:*}
    content=${line#*:}
    # Ignore commented exports
    if echo "$content" | grep -qE '^[[:space:]]*#'; then
      continue
    fi
    secret_any=1
    # Extract variable name from content like: export FOO_API_KEY=...
    var=$(echo "$content" | sed -nE 's/^[[:space:]]*(export[[:space:]]+)?([A-Z0-9_]+).*/\2/p' | head -1)
    echo "- ${f}:${lno} -> ${var}"
  done < <(grep -nE "$SECRET_ENV_RE" "$f" 2>/dev/null || true)

done
if [[ $secret_any -eq 0 ]]; then
  echo "No secret-like exported env vars detected in shell profiles."
fi

print_section "Git config tampering indicators"
if [[ -f "$HOME/.gitconfig" ]]; then
  git_hits=$(grep -nEi '(core\.hooksPath|alias\..*(curl|wget|node)|pager[^\n]*sh)' "$HOME/.gitconfig" 2>/dev/null || true)
  if [[ -n "$git_hits" ]]; then
    echo "$HOME/.gitconfig"
    echo "$git_hits" | sed 's/^/  /'
  else
    echo "No suspicious patterns in ~/.gitconfig."
  fi
else
  echo "~/.gitconfig not present."
fi

print_section "~/.node_modules persistence"
if [[ -d "$HOME/.node_modules" ]]; then
  echo "Directory exists: $HOME/.node_modules"
  echo "Top files:"
  find "$HOME/.node_modules" -maxdepth 2 -type f \( -name package.json -o -name "*.js" \) 2>/dev/null | head -20 | sed 's/^/  /'
  echo "Signature scan (first hits):"
  grep -RInE '(C250617A|C250618A|\[\x27_V\x27\]|\[\x27_H\x27\]|eval\(atob|atob\()' "$HOME/.node_modules" 2>/dev/null | head -20 | sed 's/^/  /' || true
else
  echo "Not present."
fi

print_section "node external network connections (snapshot)"
# Only print header + any node lines
lsof_out=$(lsof -i 2>/dev/null | awk 'NR==1 || $1=="node"' | head -60 || true)
if [[ -n "$lsof_out" ]]; then
  echo "$lsof_out"
else
  echo "(no lsof output)"
fi

print_section "Result"
# This script is triage-only; do not auto-remediate.
# Return exit 0 always; use content to decide next steps.
echo "Triage completed. If any section above lists findings, review before taking action."
