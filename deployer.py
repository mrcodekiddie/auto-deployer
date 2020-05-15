from github import Github
import os
import datetime
import yaml
import shutil
import socket
import subprocess
import re

#GITHUB_AUTH_TOKEN=(os.environ["GITHUB_AUTH_TOKEN"])
USER_HOME="/home/foss" #os.environ['HOME']
LOG_PATH=USER_HOME+"/logs/"
NVM_BIN=USER_HOME+"/.nvm/versions/node/v12.16.3/bin"#os.environ['NVM_BIN']
g=Github("04fe4e29649aaaabdfa")


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
                            f.write("ExecStart=/usr/bin/python3 /home/foss/projects/auto-deployer/HttpStarter.py "+str(configData['port'])+" "+repo_location+" "+LOG_PATH+repo.name)
                            f.write("\n\n")
                            f.write("[Install]\nWantedBy=multi-user.target")
                            f.close
                            os.system("systemctl enable "+repo.name+".service")
                            os.system("systemctl start "+repo.name+".service")

                    #nginx configuration
                    print("nginx time")
                    domain_name=configData['domain']
                    nginx_config_file="/etc/nginx/sites-available/"+domain_name
                    print(nginx_config_file)
                    if(os.path.exists(nginx_config_file)==False):
                        print("file not found")
                       #os.system("mkdir -p /etc/nginx/sites-available/"+repo.name+os.sep)
                        with open(nginx_config_file,'w+') as fi:
                            print("writing file")
                            fi.write("server { ")
                            fi.write("\n")
                            fi.write("server_name "+domain_name+";")
                            fi.write("\n") 
                            fi.write("location / { ")
                            fi.write("\n")
                            fi.write("proxy_pass http://127.0.0.1:"+str(configData['port']))
                            fi.write("\n")
                            fi.write("proxy_set_header Host $host;")
                            fi.write("\n")
                            fi.write("proxy_set_header X-Real-IP $remote_addr;")
                            fi.write("\n")
                            fi.write("proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;")
                            fi.write("\n")
                            fi.write("proxy_set_header X-Forwarded-Proto $scheme;")
                            fi.write("\n") 
                            fi.write(" }")
                            fi.write("\n") 
                            fi.write(" }")
                            fi.close
                        os.system("ln -s /etc/nginx/sites-available/"+domain_name+" /etc/nginx/sites-enabled/ -v ")
                        os.system("service nginx restart")
                            



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
    
