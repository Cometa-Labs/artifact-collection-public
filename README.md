# _quickstart-blank

A blank project template for Cometa. Start here to spin up a new Claude Code project with GitHub integration and skill scaffolding pre-wired.

## How to use

### 1. Duplicate the folder

Copy `_quickstart-blank` to a sibling directory. The name doesn't matter yet — call it `_untitled` or anything temporary.

```
Cometa/
├── _quickstart-blank/   <- keep this as the master copy
└── _untitled/           <- your new project (copy of template)
```

### 2. Open in Claude Code

Open the duplicated folder in Claude Code and start describing what you want to build. Use Claude to brainstorm, plan, and explore freely — nothing is committed until you say so.

### 3. Initialize the repo

When you're ready to give the project a name and push it to GitHub, say:

```
initialize repo
```

or run `/init-project`. Claude will:

1. Ask for a project name (used as the GitHub repo name and folder name)
2. Initialize git and make an initial commit
3. Create a private repo under the **cometa-labs** GitHub organization
4. Push the code
5. Rename the folder on disk to match the repo name

### GitHub auth

The init skill uses `gh` CLI if available, otherwise falls back to the GitHub REST API with a `GITHUB_TOKEN` env var.

**Recommended:** install `gh` and authenticate once:

```bash
brew install gh && gh auth login
```

**Alternative:** generate a fine-grained personal access token with `cometa-labs` as the resource owner, then:

```bash
export GITHUB_TOKEN=your_token_here
```

### 4. Clean up template scaffolding

After the repo is initialized, run:

```
/clean-init
```

This removes template files (including this README), strips the `init-project` and `clean-init` skills from the registry, and commits the result — leaving you with a clean slate to build on.

## Included skills

| Skill | Trigger | Purpose |
|---|---|---|
| `init-project` | `/init-project` | Name and push this project to GitHub |
| `clean-init` | `/clean-init` | Remove template scaffolding post-init |
| `skill-creator` | `/skill-creator` | Create, edit, and benchmark Claude skills |

## What's included

| Path | Purpose |
|---|---|
| `CLAUDE.md` | Project-level instructions Claude reads on startup |
| `.claude/settings.json` | Registers the project skills |
| `.claude/skills/init-project/` | Step-by-step logic for the init flow |
| `.claude/skills/clean-init/` | Cleanup script and skill definition |
| `.claude/skills/skill-creator/` | Tooling to build and evaluate new skills |
| `README.md` | This file (removed by `/clean-init`) |
