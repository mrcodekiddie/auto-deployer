from github import Github
import os
import datetime
import yaml
import shutil
import socket
import subprocess
import re

#GITHUB_AUTH_TOKEN=(os.environ["GITHUB_AUTH_TOKEN"])
USER_HOME="/home/timelord" #os.environ['HOME']
LOG_PATH=USER_HOME+"/logs/"
NVM_BIN="/home/timelord/.nvm/versions/node/v12.16.3/bin"#os.environ['NVM_BIN']
g=Github("bowwww")


with open('config.yml') as f:
    config =yaml.load(f,Loader=yaml.FullLoader)
    print(type(config))

def isOpen(ip,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.connect((ip, int(port)))
      s.shutdown(2)
      return True
   except:
      return False

# def get_pids(port):

# 	command = "sudo lsof -i :%s | awk '{print $2}'" % port
# 	pids = subprocess.check_output(command, shell=True)
# 	pids = pids.strip()
# 	if pids:
# 		pids = re.sub(' +', ' ', str(pids))
# 		for pid in pids.split('\n'):
# 			try:
# 				yield int(pid)
# 			except:
# 				pass
#
#SAVED FOR LATER USE


for repo in g.get_user().get_repos():
    print(repo.name+"-"+repo.html_url)

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
                            f.write("ExecStart=/usr/bin/python3 /home/timelord/projects/auto-deployer/HttpStarter.py "+str(configData['port'])+" "+repo_location+" "+LOG_PATH+repo.name)
                            f.write("\n\n")
                            f.write("[Install]\nWantedBy=multi-user.target")
                            f.close
                            os.system("systemctl enable "+repo.name+".service")
                            os.system("systemctl start "+repo.name+".service")

                    else:
                        if(isOpen('127.0.0.1',configData['port'])):
                            print("port is open")
                            port = str(configData['port'])
                            process_kill_command = "sudo kill $(sudo lsof -t -i:"+port+")"
                            print(process_kill_command)
                            print("port "+port+" is killed, Command status:"+os.system(process_kill_command))
                            os.system("systemctl stop "+repo.name+".service")
                            os.system("systemctl start "+repo.name+".service")
                            os.system('restarting service')
                        else:
                            print("someone fucked the port already\n restarting service")
                            os.system("systemctl stop "+repo.name+".service")
                            os.system("systemctl start "+repo.name+".service")




                print(sshCloneUrl)
                print(commit.sha)


      
            
            


with open('config.yml', 'w') as f:
    data = yaml.dump(config, f)
    
