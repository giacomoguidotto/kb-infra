#!/usr/bin/env bash
set -u

prototype_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=model.sh
source "$prototype_dir/model.sh"

bold=$'\033[1m'
dim=$'\033[2m'
reset=$'\033[0m'
selected='repository tree'
details=$(prototype_tree)

render() {
  clear 2>/dev/null || printf '\033[2J\033[H'
  printf '%sAgentic OS repository contract prototype%s\n\n' "$bold" "$reset"
  printf '%sQuestion%s\n' "$bold" "$reset"
  printf '%sCan self-contained release modules preserve independent releases and explicit local upgrades without a runtime or synchronized release manifest?%s\n\n' "$dim" "$reset"
  printf '%sSelected%s: %s\n\n' "$bold" "$reset" "$selected"
  printf '%s\n\n' "$details"
  printf '%sActions%s\n' "$bold" "$reset"
  printf '%s[t]%s source tree  %s[i]%s installed tree  %s[a]%s Agentic OS release\n' "$bold" "$reset" "$bold" "$reset" "$bold" "$reset"
  printf '%s[k]%s registry change  %s[c]%s Career Ops release  %s[n]%s internal change\n' "$bold" "$reset" "$bold" "$reset" "$bold" "$reset"
  printf '%s[b]%s breaking interface  %s[v]%s invariants  %s[q]%s quit\n' "$bold" "$reset" "$bold" "$reset" "$bold" "$reset"
  printf '%s[r]%s release contract\n' "$bold" "$reset"
}

while true; do
  render
  IFS= read -r -n 1 key
  case "$key" in
    t) selected='repository tree'; details=$(prototype_tree) ;;
    i) selected='installed tree'; details=$(prototype_installed_tree) ;;
    a) selected='Agentic OS release'; details=$(prototype_scenario agentic-release) ;;
    k) selected='Endpoint Registry change'; details=$(prototype_scenario registry-change) ;;
    c) selected='Career Ops setup release'; details=$(prototype_scenario career-release) ;;
    n) selected='internal-only change'; details=$(prototype_scenario internal-change) ;;
    b) selected='breaking System interface'; details=$(prototype_scenario breaking-interface) ;;
    v) selected='candidate invariants'; details=$(prototype_scenario invariants) ;;
    r) selected='candidate release contract'; details=$(prototype_scenario release-contract) ;;
    q) break ;;
  esac
done
