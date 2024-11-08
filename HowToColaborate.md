# Collaboration Guide for Team Project Using GitHub
- To collaborate effectively without overwriting each other's work, you should follow a branching strategy and communicate frequently. Here are the key steps to follow:

1. Cloning the Repository (Initial Setup)
Each team member should clone the repository to create a local copy on their machine:
# Replace URL with the actual repository URL
- git clone git@github.com:ronniearistil/Travel-Tracker-CLI-Project.git
-Uncheck "copy the master branch only"

2. Creating a New Branch
When working on a feature or bug fix, create a separate branch. Start by making sure the main branch is up to date, then create and switch to your new branch:

# Always make a new BRANCH when working on any code you do!!!

# To make a NEW branch:
- git checkout -b whatever-name-you-want    <--- try to make sure its something related would be best!

# ALWAYS make sure you are in that branch that you just created:
- git branch <---- this will show you what specific branch you are on! (Should be the new one you've created)

# Once that is all set, then continue with the following:

3. # Committing and Pushing Changes
 After making changes, stage, commit, and push them to the remote repository:

# Stage all changed files
- git add .

# Commit with a descriptive message
- git commit -m "Make sure this message is specific to what you are doing"

# Push the branch to the remote repository
- git push origin name-of-your-repo  <----- Replace with your branch name

 Once you've pushed the code to the repo:
- Go to the repo and merge it to the main

4. # Pulling Latest Changes and Merging
Keep your branch up-to-date by merging changes from the main branch periodically. Always communicate with the team before merging the main branch into your own to avoid conflicts.

# Make sure you are in the new branch for which task you are doing! 
- git checkout feature/add-destination    <---- Replace with your branch name

# Pulling the code that your partner uploaded:
git pull origin main <----- once your team has successfully pushed a code to the main repo pull it but make sure you are in a NEW BRANCH

Important: Coordinate with us before merging to ensure everyone is aligned !!!

5. Creating Pull Requests
When your feature or bug fix is complete, create a pull request on GitHub to merge your branch into the main branch. Review any comments or requested changes from teammates or the project manager, and update your branch if needed.

# Summary of Key Git Commands
- Command &  Description
git checkout main ---> Switch to the main branch
git pull origin main ---> Pull the latest changes from the main branch
git checkout -b branch-name	--->Create a new branch and switch to it
git add . --->Stage all changes
git commit -m "message"	---> Commit changes with a message
git push origin branch-name	--->Push your branch to the remote repository
git pull origin main	---> Pull updates from main while on your branch
git merge main	--->Merge main into your branch to resolve conflicts