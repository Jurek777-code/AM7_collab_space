# AM7 Collaboration Space

## Welcome to the AM7 Collaboration Space! This repository is designed to facilitate teamwork and project management for our AM7 group. Here, you can share code, documents, and resources related to our projects.

How to Use This Repository:

1. **Clone the Repository**: Use Git to clone this repository to your local machine.
2. **Create Branches**: For each project or task, create a new branch to keep your work organized and separate from the main branch.
3. **Commit Changes**: Regularly commit your changes with clear messages to keep track of your progress.
4. **Push to Remote**: Push your commits to the remote repository to share your work with the team.
5. **Pull** Changes\*\*: Regularly pull changes from the remote repository to stay updated with your teammates' work.

For all points above and more detailed instructions, please refer to the Quick Start Guide below.

## Quick Start Guide

### 1. Clone the Repository

In your Terminal go to the directory where you want to store the project and run:

```bash
git clone https://github.com/Jurek777-code/AM7_collab_space.git
cd AM7_collab_space
```

### 2. Configure Git (First Time Only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 3. Make Changes

Edit or add files to the project.

### 4. Check Status

```bash
git status
```

### 5. Stage Changes

```bash
# Stage all changes
git add *

# Or stage specific files
git add filename.txt
```

### 6. Commit Changes

```bash
git commit -m "Your commit message describing the changes"
```

### 7. Push to Remote

```bash
git push origin main
```

## Working with Branches

### Switch to the Referat_Geschichte_der_Fotografie Branch

```bash
# View all available branches
git branch -a

# Switch to the Referat_Geschichte_der_Fotografie branch
git checkout Referat_Geschichte_der_Fotografie
```

After switching to the branch, all your commits will be made to that branch instead of main.

## Useful Commands

- `git log` — View commit history
- `git diff` — See changes before committing
- `git pull` — Update local repository with remote changes
- `git branch` — List or create branches
- `git checkout <branch-name>` — Switch to a different branch
- `git push origin <branch-name>` — Push changes to a specific branch

---

_Last updated: March 25, 2026_
