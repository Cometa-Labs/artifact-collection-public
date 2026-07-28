---
name: init-project
description: Initialize this template as a named project on GitHub under cometa-labs. Use this whenever the user wants to name their project, push to GitHub, initialize the repo, create the repo, or says they're ready to go. Trigger even if the user just names the project in passing — that's the signal to start.
---

# init-project

Initialize this template as a named project, create a GitHub repo under cometa-labs, and push.

## When to trigger

Trigger this skill when the user says any of:
- "initialize repo"
- "init repo"
- "init project"
- `/init-project`
- "create the repo"
- "push to github"
- "ready to name this project"

If the user provides a project name in the same message (e.g. "initialize repo called my-project"), capture it immediately and skip asking.

## Steps to follow

### Step 1 — Lock in the project name

If the user already provided a name, use it. Otherwise ask: **"What should this project be called?"**

The name will be used as the GitHub repo name and the folder name. Normalize it: lowercase, hyphens for spaces. Warn and re-prompt if it contains invalid characters.

Show a one-line confirmation before proceeding:
```
Creating cometa-labs/<name> and renaming this folder to <name>. Proceed? (yes / no)
```

### Step 2 — Initialize git

Check if a `.git` directory exists:
```bash
git rev-parse --is-inside-work-tree 2>/dev/null
```

**If no `.git` exists:** initialize fresh:
```bash
git init
git branch -m main
git add .
git commit -m "Initial commit"
```

**If `.git` exists:** check if it's the inherited template repo by inspecting the origin URL:
```bash
git remote get-url origin 2>/dev/null
```

- If the URL contains `cometa-labs/_quickstart-blank` (or there is no remote and the log shows the template's scaffolding commits), this is the duplicated template `.git`. Delete it and re-initialize:
  ```bash
  rm -rf .git
  git init
  git branch -m main
  git add .
  git commit -m "Initial commit"
  ```

- If the origin URL points to something else, or the repo looks user-created (commits beyond the template scaffolding, custom remotes, etc.), **stop and ask the user:**
  > "This folder already has a git repo pointing to `<url>`. Should I delete it and start fresh, or stop so you can handle it manually?"
  Do not proceed until the user confirms.

### Step 3 — Create the GitHub repo and push

Try `gh` first:
```bash
gh repo create cometa-labs/<name> --private --source=. --remote=origin
```

If `gh` is not found (`command not found`), fall back to the GitHub REST API:

Check for a token:
```bash
echo $GITHUB_TOKEN
```

If `GITHUB_TOKEN` is empty, tell the user:

> Install the GitHub CLI (`brew install gh && gh auth login`) or set a `GITHUB_TOKEN` env var with `repo` and `write:org` scopes, then try again.

If `GITHUB_TOKEN` is set:
```bash
curl -s -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/orgs/cometa-labs/repos \
  -d "{\"name\":\"<name>\",\"private\":true,\"auto_init\":false}"

git remote add origin https://github.com/cometa-labs/<name>.git
```

### Step 4 — Rename the folder

After the push succeeds:
```bash
mv "<current-absolute-path>" "<parent-dir>/<name>"
```

### Step 5 — Done

```
Done!

  GitHub: https://github.com/cometa-labs/<name> (remote set, not yet pushed)
  Local:  <parent-dir>/<name>

Push when ready using GitHub Desktop or: git push -u origin main
Note: reopen this folder in Claude Code from the new path.
When ready, run /clean-init to remove template scaffolding.
```

## Error handling

- If git is not installed: tell the user to run `xcode-select --install`.
- If the GitHub repo already exists: ask if they want to push to the existing repo or pick a different name.
- If the folder rename fails: show the `mv` command and tell the user to run it manually.
- Never force-push without explicit user confirmation.
