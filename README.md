# service_manager
…or create a new repository on the command line
```shell
echo "# service_manager" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/mnedev-cell/service_manager.git
git push -u origin main
```
…or push an existing repository from the command line
```shell
git remote add origin https://github.com/mnedev-cell/service_manager.git
git branch -M main
git push -u origin main
```

## Création Service ping
- Create file ping_service.py  
```shell
  sudo nano /usr/local/bin/ping_service.py
```
- Add the Following code:
# Python script for periodic ping service
# Copy and save this script to use in your project
import socket
import requests
import time
import datetime
import threading
import os

# Global variables
config = {
    "URL_ping": "http://ping.logitec.ma/ping_srv/RPI/SDC/",
    "Position": socket.gethostname()  # Example position
}
```shell

```

## Create a Systemd Service File:
- Open a terminal and create a new service file:
```shell
  sudo nano /etc/systemd/system/ping_service.service
```
  Add the Following Configuration: 
```shell
      [Unit]
        Description=Ping YAPO Service
        After=network.target
      
      [Service]
        ExecStart=/usr/bin/python3 /usr/local/bin/ping_service.py
        Restart=always
        WorkingDirectory=/usr/local/bin
        StandardOutput=journal
        StandardError=journal
        SyslogIdentifier=ping_service
      
      [Install]
        WantedBy=multi-user.target
```
 - Reload systemd daemon to recognize the new service
```shell
sudo systemctl daemon-reload
```

- Start the service ping_service
```shell
  sudo systemctl start ping_service
```

  
- check status ping service
```shell
   sudo systemctl status ping_service
```

- enable service ping service
```shell
    sudo systemctl enable ping_service
```
 

- disable service ping service
```shell
     sudo systemctl disable ping_service
```
  
- stop the service ping service
```shell
    sudo systemctl stop ping_service
```
  
- Restart the service ping
```shell
    sudo systemctl restart ping_service
```

## Download service manager file
```shell
  wget https://upload.yapo.ovh/update/service_manager.py -O /home/pi/service_manager.py
```

