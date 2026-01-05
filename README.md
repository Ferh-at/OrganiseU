Hello and welcome to the repository for OrganiseU.

Here, you will find the commands you will have to use and be familiar with as part of a developer at Qube.

**Onboarding Process**
    Staging = think of it as putting your changes into a shopping basket before checking out --> you haven't paid, but it is a collection of what you have done.
    Committing = imagine it as taking a snapshot of your project at that moment in time
    Branch = a version of the repository, used for code which is not ready to be integrated into main codebase
    Commands are executed through the VSCode Terminal (Ctrl + Shift + ')


1) git clone (insert URL of repository here) - Copies a remote repository to your machine, basically replicating it to your own device
2) git remote add origin (insert URL of repository here) - Links your remote repository to Github -  **ONLY RUN ONCE PER PROJECT**
3) git push -u origin (insert name of branch you're working on) - pushes your changes and sets an upstream branch. Basically, when you first start working on a branch, it sets up the connection between your local main branch and the designated branch on GitHub. **After running it once, you can just run git push while working on that branch.**

When you have done these commands, well done! You have successfully connected your local computer to the repository.

**Key Information**
1) git status - This command shows your current status with regards to the repository - whether you're up to date, what files you have modified etc.
2) git add -A - This command *stages* all the changes you have made. **MAKE SURE TO RUN GIT STATUS BEFORE TO ENSURE NO MISTAKES OCCUR**
3) git commit -m "(insert your brief message)" - Saves a snapshot of the staged changes that you have made in that session. 
    **You should definitely use *git diff* to see what you have changed before committing**


4) git pull - fetches and merges in one step, but **can cause merge conflicts if your local work overlaps with remote changes** — use with caution.
5) git fetch - lets you see remote changes without touching your local files — it's the safest way to stay updated before merging.
6) git push - uploads your local commits to GitHub — **always fetch and review first to avoid overwriting someone else’s work or facing rejected pushes.**

7) git branch - lists all branches - if a branch does not appear, run git fetch to ensure local repository is up to date.
8) git switch -c <branch-name> - make a new branch on the repository 
9) git switch <branch> - switching branches
10) git stash - temporarily saves changes --> use if switching branches but not ready to commit
11) git stash pop - reapplies stashed changes

12) git reset - unstages files from commit area


**Common Mistakes to Avoid**
❌ Forgetting to fetch/pull before pushing - can lead to rejected pushes when integrating into main branch.
❌ Skipping git status - leads to committing the wrong files.
✅ Always check git diff before committing or merging.