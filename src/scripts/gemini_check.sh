#!/bin/bash
# Pipe a file (or stdin) to Gemini for verification.
#
# Usage:
#   ./gemini_check.sh <file> "<question>"
#   cat <file> | ./gemini_check.sh - "<question>"
#   ./gemini_check.sh <file>          # uses default verification prompt
#
# Examples:
#   ./gemini_check.sh math/derivation.md "Check dimensions and signs."
#   cat math/result.md | ./gemini_check.sh - "Is this physically reasonable?"

DEFAULT_PROMPT="Verify this derivation step by step. Check: (1) If it has good physical meaning (2) sign conventions, (3) limiting cases (zero coupling, infinite volume, classical limit), (4) whether approximations are justified and their regime of validity is stated. Report any errors clearly. Do not be encouraging if there are problems."

if [ "$1" = "-" ]; then
    INPUT=$(cat)
elif [ -f "$1" ]; then
    INPUT=$(cat "$1")
else
    echo "Error: '$1' is not a file or '-' (stdin)" >&2
    exit 1
fi

QUESTION="${2:-$DEFAULT_PROMPT}"

printf '%s\n\n---\n\n%s' "$INPUT" "$QUESTION" | gemini
