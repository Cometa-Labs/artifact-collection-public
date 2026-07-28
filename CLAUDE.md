# New Project

This is a fresh project from the Cometa template. The project has no name yet.

## Getting started

Start by describing what you want to build. Use Claude to brainstorm, plan, and explore ideas freely. Nothing is committed until you say so.

When you're ready to give this project a name and push it to GitHub, say **"initialize repo"** or run `/init-project`.

## Initialize repo

Running `/init-project` will:
1. Ask you for a project name (becomes the GitHub repo name and folder name)
2. Initialize git with an initial commit
3. Create a private repo under the **cometa-labs** GitHub organization
4. Push the code
5. Tell you the new remote URL

## Notes

- GitHub CLI (`gh`) is used if available; otherwise the skill uses the GitHub REST API via `curl` with a `GITHUB_TOKEN` env var
- The folder will be renamed on disk after the push
- You can cancel at any point before the final push
- After the repo is initialized, run `/clean-init` to remove template scaffolding in one shot
