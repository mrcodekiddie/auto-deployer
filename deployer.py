from github import Github
import os
import datetime
import yaml
import shutil


#GITHUB_AUTH_TOKEN=(os.environ["GITHUB_AUTH_TOKEN"])
USER_HOME="/home/timelord" #os.environ['HOME']
LOG_PATH=USER_HOME+"/logs/"
NVM_BIN="/home/timelord/.nvm/versions/node/v12.16.3/bin"#os.environ['NVM_BIN']
g=Github("d0d654264d79398d9134eb82942f1a70d86e76a5")


with open('config.yml') as f:
    config =yaml.load(f,Loader=yaml.FullLoader)
    print(type(config))


for repo in g.get_user().get_repos():
   
    for configData in config['repos']:


        if(repo.html_url==configData['url']):
            print(repo.html_url)
            commit = repo.get_commits()[0]
            if(configData['lastCommitHash']!=commit.sha):
                configData['lastCommitHash']=commit.sha
                configData['lastCloned']=datetime.datetime.now()
                sshCloneUrl=repo.ssh_url
                
                clone_path=USER_HOME+os.sep+"deploy"+os.sep
                repo_location=clone_path+repo.name
                if(os.path.exists(repo_location)):
                    shutil.rmtree(repo_location)

                os.system("git clone "+sshCloneUrl +" "+repo_location+" --depth=1")
                if(configData['language']=='html'):
                    service_file="/etc/systemd/system/"+repo.name+".service"
                    if(os.path.exists(service_file)==False):
                        with open(service_file,'w+') as f:

                            f.write("Description="+repo.name+" Server")
                            f.write("\n") 
                            f.write("After=network.target remote-fs.target nss-lookup.target")
                            f.write("\n\n")
                            f.write("[Service]")
                            f.write("\n")
                            f.write("Type=simple")
                            f.write("\n")
                            f.write("RemainAfterExit=yes")
                            f.write("\n\n")
                            f.write("ExecStart="+NVM_BIN+"/http-server "+repo_location)
                            f.write(" -a 127.0.0.1  --port "+str(configData['port']))
                            f.write(" -d false")
                            f.write(" --no-dotfiles --log-ip true")
                            LOG_PATH=USER_HOME+os.sep+"logs"+os.sep+repo.name
                            if(os.path.exists(LOG_PATH)==False):
                                os.system("mkdir -p "+LOG_PATH)
                            f.write(" | tee -i "+LOG_PATH+os.sep+repo.name+".log")
                            f.write("\n\n")
                            f.write("[Install]\nWantedBy=multi-user.target")
                            f.close
                    
                    os.system("systemctl enable "+repo.name+".service")
                    os.system("systemctl start "+repo.name+".service")
                
                print(sshCloneUrl)
                print(commit.sha)
            
            


with open('config.yml', 'w') as f:
    data = yaml.dump(config, f)
    
