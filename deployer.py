from github import Github
import os
import datetime
import yaml
g=Github('censored_for_privacy')

with open('config.yml') as f:
    config =yaml.load(f,Loader=yaml.FullLoader)
    print(type(config))

for repo in g.get_user().get_repos():
   
    for configData in config['repos']:


        if(repo.html_url==configData['url']):
           
            print(type(repo))
            print(repo.html_url)
            commit = repo.get_commits()[0]
            if(configData['lastCommitHash']!=commit.sha):
                configData['lastCommitHash']=commit.sha
                configData['lastCloned']=datetime.datetime.now()
                print(commit.sha)
            
            


with open('config.yml', 'w') as f:
    data = yaml.dump(config, f)