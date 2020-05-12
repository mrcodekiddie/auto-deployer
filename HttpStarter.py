import os
import sys
import argparse
from datetime import datetime

HTTP_BIN="/home/timelord/.nvm/versions/node/v12.16.3/bin/http-server"#os.environ['NVM_BIN']

args=sys.argv
print(type(args))
port=args[1]
web_dir=args[2]
log_path=args[3]
print(args)
timeNow=datetime.now()
current_datetime=timeNow.strftime("%Y-%m-%d_%H:%M:%S")
exec_cmd=HTTP_BIN+" "+web_dir+" -p "+port+" -a 127.0.0.1 -d false --utc  --log-ip true --no-dotfiles >>  "+log_path+current_datetime+".log"
print(exec_cmd)
os.system(exec_cmd)

