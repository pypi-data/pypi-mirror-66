# gituploader

A Python package to upload a local repository to Github from your Local Machine without 
writing  git commands in shell


# Usage:

This package will upload your repository from your local machine to github 
by  using github URL of your repository.

Package's function push() needs 4 parameters:

1.gitrepositoryurl :  URL of new repository created on github
  
2.scriptname :  Name of the script in which this package is being used

3.Username : github username

4.Email:  github email 

User need to run ascript of this package in a directory from where local Repository are to be uploaded to github  

# Example:

user = GithubUser

email = GithubEmail

scriptname = 'setup.py'

giturl = 'https://github.com/user/project1'

gituploader.push(user, email, scriptname, giturl)


# Version 1.0.1:
 
This version is compatible with Windows OS only 

Next release will focus on other OS

# Requirement:

Python version>=3.6

Git has to be installed in local machine as this package is based on Git



