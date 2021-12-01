(saving-code)=
# Saving Code (WIP)

Most Cal-ITP analysts should opt for working directly from JupyterHub. Leveraging this cloud-based, standardized environment should alleviate many of the pain points associated with creating reproducible, collaborative work.

Doing work locally and pushing directly from the command line is a similar workflow, but replace the JupyterHub terminal with your local terminal.

## Table of Contents
1. [Onboarding Setup](#onboarding-setup)
1. What's a typical [project workflow](#project-workflow)?
1. Someone is collaborating on my branch, how do we [stay in sync](#pulling-and-pushing-changes)?
1. The `main` branch is ahead, and I want to sync my branch with `main`
    * [Rebase](#rebase)
    * [Merge](#merge)
    * Differences between `merge` and `rebase`: [Atlassian tutorial](https://www.atlassian.com/git/tutorials/merging-vs-rebasing), [GitKraken](https://www.gitkraken.com/learn/git/problems/git-rebase-vs-merge), [Hackernoon](https://hackernoon.com/git-merge-vs-rebase-whats-the-diff-76413c117333), and [StackOverflow](https://stackoverflow.com/questions/59622140/git-merge-vs-git-rebase-for-merge-conflict-scenarios).
1. [Helpful Hints](#helpful-hints)


## Pushing from JupyterHub

### Onboarding Setup

We'll work through getting set up with GitHub on JupyterHub and cloning one GitHub repo. Repeat steps 6-10 for other repos.

1. Create a GitHub username, get added to the various Cal-ITP teams. You'll be committing directly into the Cal-ITP repos!
1. Create a Personal Access Token (PAT) by following these [directions](https://github.com/cal-itp/data-infra/blob/main/docs/analytics_welcome/03_how_we_work.md#using-the-data-analyses-repo)
1. Navigate to the GitHub repository to clone. We'll work our way throught he `data-analyses` [repo here](https://github.com/cal-itp/data-analyses). Click on the green `Code` button and grab the `HTTPS` URL.
1. Open a terminal in JupyterHub. All our commands will be typed in this terminal.
1. Configure your Git username and email: `git config --global user.name MY_USERNAME` and `git config --global user.name MYEMAIL@EMAIL.COM`
1. Clone the Git repo: `git clone https://github.com/cal-itp/data-analyses.git`
1. Double check  with`ls` to list and see that the remote repo was successfully cloned into your "local" (cloud-based) filesystem.
1. Change into the `data-analyses` directory: `cd data-analyses`
1. Point to the remote repo: `git remote add origin https://github.com/cal-itp/data-analyses.git`. Double check it's set with: `git remote -v`
1. Pull from the `main` branch and sync your remote and local repos: `git pull origin main`

### Project Workflow

It is best practice to do have a dedicated branch for your task. A commit in GitHub is similar to saving your work. It allows the system to capture the changes you have made and offers checkpoints through IDs that both show the progress of your work and can be referenced for particular tasks.

In the `data-analyses` repo, separate analysis tasks live in their own directories, such as `data-analyses/gtfs_report_emails`.

1. Start from the `main` branch: `git pull origin main`
1. Check out a new branch to do your work: `git checkout -b my-new-branch`
1. Do some work...add, delete, rename files, etc
1. See all the status changes to your files: `git status`
1. When you're ready to save some of that work, stage the files you want to commit with `git add foldername/notebook1.ipynb foldername/script1.py`. To stage all the files, use `git add .`.
1. Once you are ready to commit, add a commit message to associate with all the changes: `git commit -m "exploratory work" `
1. Push those changes from local to remote branch (note: branch is `my-new-branch` and not `main`): `git push origin my-new-branch` and enter your username and **personal access token as the password**.
1. To review a log of past commits: `git log`
1. When you are ready to merge all the commits into `main`, open a pull request (PR) on the remote repository, and merge it in!
1. Go back to `main` and update your local to match the remote: `git checkout main`, `git pull origin main`


### Pulling and Pushing Changes

Especially when you have a collaborator working on the same branch, you want to regularly sync your work with what's been committed by your collaborator. Doing this frequently allows you to stay in sync, and avoid unncessary merge conflicts.

1. Stash your changes temporarily: `git stash`
1. Pull from the remote to bring the local branch up-to-date (and pull any changes your collaborator made): `git pull origin my-new-branch`
1. Pop your changes: `git stash pop`
1. Stage and push your commit with `git add` and `git commit` and `git push origin my-new-branch`

### Rebase

A rebase might be preferred, especially if all your work is contained on your branch, within your task's folder, and lots of activity is happening on `main`. You'd like to plop all your commits onto the most recent `main` branch, and have it appear as if all your work took place *after* those PRs were merged in.

1. At this point, you've either stashed or added commits on `my-new-branch`.
1. Check out the `main` branch: `git checkout main`
1. Pull from origin: `git pull origin main`
1. Check out your current branch: `git checkout my-new-branch`
1. Rebase and rewrite history so that your commits come *after* everything on main: `git rebase main`
1. At this point, the rebase may be successful, or you will have to address any conflicts! If you want to abort, use `git rebase --abort`. Changes in scripts will be easy to resolve, but notebook conflicts are difficult. If conflicts are easily resolved, open the file, make the changes, then `git add` the file(s), and `git rebase --continue`.
1. Make any commits you want (from step 1) with `git add`, `git commit -m "commit message"`
1. Force-push those changes to complete the rebase and rewrite the commit history: `git push origin my-new-branch -f`

### Merge

1. At this point, you've either stashed or added commits on `my-new-branch`.
1. Pull from origin: `git checkout main` and `git pull origin main`
1. Go back to your branch: `git checkout my-new-branch`
1. Complete the merge of `my-new-branch` with `main` and create a new commit: `git merge my-new-branch main`
SOMEONE WHO PREFERS MERGE PROCESS TO FILL THIS IN...is there a commit after?

### Helpful Hints

* To discard the changes you made to a file, `git checkout my-notebook.ipynb`, and you can revert back to the version that was last committed.
* Temporarily stash changes, move to a different branch, and come back and retain those changes: `git stash`, `git checkout some-other-branch`, do stuff on the other branch, `git checkout original-branch`, `git stash pop`
* Rename files and retain the version history associated: `git mv old-notebook.ipynb new-notebook.ipynb`
* Once you've merged your branch into `main`, you can delete your branch locally: `git branch -d my-new-branch`

## [WIP] Pushing in GitHub - Drag and Drop

## [WIP] Pushing from the Command Line