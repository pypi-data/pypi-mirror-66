import subprocess


def info():
    packageinfo = '''

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

        '''
    print(packageinfo)


def push(username=None, email=None, scriptname=None, gitrepositoryurl=None):

    if (username and email and gitrepositoryurl and scriptname) != None:

        cmd1 = ['git', 'config', '--global', 'user.name', f"{username}"]
        p1 = subprocess.run(cmd1, capture_output=True, shell=True, text=True)
        print(p1.stdout)

        cmd2 = ['git', 'config', '--global', 'user.email', f"{email}"]
        p2 = subprocess.run(cmd2, capture_output=True, shell=True, text=True)
        print(p2.stdout)

        cmd3 = ['git', 'init']
        p3 = subprocess.run(cmd3, capture_output=True, shell=True, text=True)
        print(p3.stdout)

        cmd4 = ['git', 'add', '.']
        cmd41 = ['git', 'reset', scriptname]
        p4 = subprocess.run(cmd4, capture_output=True, shell=True, text=True)
        p41 = subprocess.run(cmd41, capture_output=True, shell=True, text=True)
        print(p4.stdout)
        print(p41.stdout)

        cmd5 = ['git', 'commit', '-m', "my first commit"]
        p5 = subprocess.run(cmd5, capture_output=True, shell=True, text=True)
        print(p5.stdout)

        cmd7 = ['git', 'remote', 'add', 'origin', gitrepositoryurl]
        p7 = subprocess.run(cmd7, capture_output=True, shell=True, text=True)
        print(p7.stdout)

        cmd8 = ['git', 'push', '-u', 'origin', 'master']
        p8 = subprocess.run(cmd8, capture_output=True, shell=True, text=True)
        print(p8.stdout)

    else:
        print('Warning: 1. push() accepts 4 required arguments (username,email, script, giturl)')
