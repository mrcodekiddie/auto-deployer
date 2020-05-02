from github import Github
import os
g=Github(os.environ['GITHUB_AUTH_TOKEN'])

for repo in g.get_user().get_repos():
   
    
    if(repo.name=="summa"):
        print(type(repo))
        print(repo.html_url)
        for commit in repo.get_commits():
            print(commit.sha)

        #print(dir(repo))

# for repo in gitty.get_user().get_repos():
#     print(repo.name)
#     repo.edit(has_wiki=False)
#     # to see all the available attributes and methods
#     print(dir(repo))
