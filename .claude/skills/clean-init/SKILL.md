---
name: clean-init
description: Remove template scaffolding after a project has been initialized. Use this after init-project has run successfully, or when the user says "clean up template", "remove bootstrap files", "clean up", or "/clean-init".
---

# clean-init

Run the cleanup script to remove template scaffolding after init-project has completed.

## When to trigger

Trigger this skill when the user says any of:
- "clean init"
- "clean up template"
- "remove template files"
- `/clean-init`

## Steps

Run the script:
```bash
bash .claude/skills/clean-init/scripts/clean-init.sh
```

That's it. The script handles everything and removes itself.
