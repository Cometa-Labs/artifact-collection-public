#!/bin/bash
# clean-init.sh
# Run once after init-project to remove template scaffolding.
# Deletes itself on completion.

set -e

PROJECT_NAME=$(basename "$(git rev-parse --show-toplevel)")

echo "Cleaning up bootstrap files for: $PROJECT_NAME"

# Remove template files
rm -f README.md

# Replace CLAUDE.md with a clean project stub
cat > CLAUDE.md <<EOF
# $PROJECT_NAME

> Add project description here.
EOF

# Remove init-project and clean-init skill directories
rm -rf .claude/skills/init-project
rm -rf .claude/skills/clean-init

# Remove init-project and clean-init from the skills registry
python3 -c "
import json
with open('.claude/settings.json') as f:
    s = json.load(f)
remove = {'.claude/skills/init-project', '.claude/skills/clean-init'}
s['skills'] = [sk for sk in s.get('skills', []) if sk not in remove]
with open('.claude/settings.json', 'w') as f:
    json.dump(s, f, indent=2)
    f.write('\n')
"

# Commit
git add -A
git commit -m "Remove bootstrap scaffolding"

echo "Done. Update CLAUDE.md with project context."
