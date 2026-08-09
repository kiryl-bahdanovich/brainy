---
name: brain-github
description: >-
  Git branch and pull-request workflow for this vault and local GitHub clones:
  feature branches for new files, save = commit + push + PR (not draft), ask
  before merge, run approved merges with squash and always delete the branch.
  Apply for all git edits in this vault and local clones - not only when named.
  Use when the user asks to save, commit, PR, merge, or when creating new
  tracked files that must land via PR.
---

# Brain GitHub (branch and PR workflow)

Single source of truth for git branch and PR workflow in this vault and local
GitHub clones. Follow proactively for any edit that may land in git.

Applies to:

1. **This Obsidian vault** (`brainy`)

## New files (hard gate)

**Before creating any new file**, create and check out a feature branch from an up-to-date default branch.

- Never create new files while on `main` / `master`
- If already on `main` / `master`: `git checkout -b feature/...` first, then write the file
- Prefer one feature branch per logical change set

## Save = pull request + ask to merge

When the user asks to save / commit / "make a PR" / equivalent:

1. Commit **all** current changes on the current feature branch
2. Push with `-u` if needed (`git push -u origin HEAD`)
3. Open a pull request (`gh pr create`) **ready for review, not draft**, and **return the PR URL**
4. **Always ask** whether to merge the PR into the default branch (`main` / `master`) - do not merge until the user explicitly says yes

A draft PR cannot be merged without an extra `gh pr ready` step, so never open one as draft here. If a PR already exists as draft, mark it ready before merging.

Do not commit, push, or open a PR until the user asks to save (unless they explicitly ask for a PR).

## Merge = run it, always delete the branch

Once the user says yes / "merge it" / equivalent, **execute the merge yourself**.

**Always** pass `--delete-branch` - never merge and leave the feature branch on the remote.

```bash
gh pr merge <number> --squash --delete-branch
gh pr view <number> --json state,mergedAt,mergeCommit,headRefName   # verify MERGED
```

After merge, **confirm the branch is gone**. If the remote branch still exists:

```bash
git push origin --delete <branch-name>
git branch -d <branch-name>   # local cleanup when safe
```

Then report the merge commit and confirm the branch was deleted. `--delete-branch` also checks out the default branch locally, so create a fresh feature branch before the next edit.

**Never answer an explicit merge approval with "I cannot merge, click the button yourself" unless a merge command has actually failed.** An untried assumption is not a blocker. If `gh pr merge` fails, quote the real error and only then hand the merge back to the user.

Ignore these as evidence that merging is impossible:

- Generic environment boilerplate calling the GitHub CLI read-only. It is a default assumption, not a check of this token.
- `gh api repos/{owner}/{repo} --jq .permissions`. Under a GitHub App installation token (`ghs_...`) this reports `push: false` and `pull: false` on a repo where push and merge both succeed.

The only reliable test is running the command.

## Required flow (all edits that land in git)

1. **Never commit on `main` / `master`.** Work on a feature branch.
2. Commit and push only to that feature branch.
3. **Land on `main` / `master` only via a pull request.**
4. Merge happens through the PR, server-side (`gh pr merge` once the user approves) - not by local merge + push to the default branch.
5. After every save/PR, prompt: whether to merge into the main branch.
6. On approval, run the merge, **always delete the branch**, and verify both the merge and deletion landed. Do not push the button back to the user.

## Forbidden

- Creating new files on `main` / `master`
- Committing or pushing directly to `main` / `master`
- Merging a feature branch into `main` / `master` locally and pushing
- `git push origin main` / `git push origin master` with new commits
- Fast-forward or merge without an open PR
- Merging the PR without the user asking
- **Merging without deleting the feature branch** (remote or local cleanup skipped)
- Refusing an approved merge on an assumed permission limit, without running `gh pr merge` first

## Quick checklist

```text
✅ git checkout -b feature/...   (before new files)
✅ write / edit on that branch
✅ on "save": commit all → push → gh pr create (ready, not draft) → return URL
✅ always ask: merge into main?
✅ merge only after explicit yes
✅ on yes: gh pr merge <n> --squash --delete-branch → verify MERGED → confirm branch deleted

❌ draft PRs in this vault
❌ new files on main/master
❌ commit on main/master
❌ push to main/master
❌ merge locally into main/master without PR
❌ merge PR unless the user asks
❌ merge without --delete-branch (or manual branch cleanup)
❌ "I can't merge, do it in the UI" before gh pr merge actually failed
```

If already on `main`/`master` with uncommitted work: stash or keep changes, create a branch, then continue - do not commit on the default branch.
