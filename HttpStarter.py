import os
import sys
import argparse
from datetime import datetime

HTTP_BIN="http-server"#os.environ['NVM_BIN']

args=sys.argv
#print(type(args))
port=str(args[2])
web_dir=args[1]
log_path=args[3]
if(os.path.exists(log_path)==False):
    os.system("mkdir -p "+log_path)
print(args)
timeNow=datetime.now()
current_datetime=timeNow.strftime("%Y-%m-%d_%H:%M:%S")
exec_cmd=HTTP_BIN+" "+web_dir+" -p "+port+" -a 127.0.0.1 -d false --utc  --log-ip true --no-dotfiles"# >>  "+log_path+current_datetime+".log"
print(exec_cmd)
os.system(exec_cmd)

