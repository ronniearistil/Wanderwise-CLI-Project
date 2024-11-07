# Collaboration Guide for Team Project Using GitHub
- To collaborate effectively without overwriting each other's work, you should follow a branching strategy and communicate frequently. Here are the key steps to follow:

1. Cloning the Repository (Initial Setup)
Each team member should clone the repository to create a local copy on their machine:
# Replace URL with the actual repository URL
- git clone git@github.com:ronniearistil/Travel-Tracker-CLI-Project.git

2. Creating a New Branch
When working on a feature or bug fix, create a separate branch. Start by making sure the main branch is up to date, then create and switch to your new branch:

# Navigate to the main branch
git checkout main

# Pull the latest changes from the main branch
git pull origin main

# Create and switch to a new branch (e.g., feature/add-destination)
- git checkout -b feature/add-destination  # Replace 'feature/add-destination' with your branch name
Naming Convention: Use descriptive branch names, such as feature/add-destination or bugfix/fix-date-format, to keep branches organized.

3. Committing and Pushing Changes
After making changes, stage, commit, and push them to the remote repository:
# Stage all changed files
- git add .

# Commit with a descriptive message
- git commit -m "Added CLI functionality for listing destinations"

# Push the branch to the remote repository
- git push origin feature/add-destination  # Replace with your branch name

4. Pulling Latest Changes and Merging
Keep your branch up-to-date by merging changes from the main branch periodically. Always communicate with the team before merging the main branch into your own to avoid conflicts.

# Switch to your branch
- git checkout feature/add-destination  # Replace with your branch name

# Merge the latest main branch changes into your branch
- git merge main

Important: Coordinate with us before merging to ensure everyone is aligned !!!

5. Creating Pull Requests
When your feature or bug fix is complete, create a pull request on GitHub to merge your branch into the main branch. Review any comments or requested changes from teammates or the project manager, and update your branch if needed.

# Summary of Key Git Commands
Create a new branch: 
    - git checkout -b branch-name
Switch branches: 
    - git checkout branch-name
Push branch to remote: 
    - git push origin branch-name
Pull latest changes: 
    - git pull origin branch-name
Stage files: 
    - git add .
Commit changes: 
    - git commit -m "commit message"
Merge main into your branch: 
    -git merge main (Coordinate with team members before merging)