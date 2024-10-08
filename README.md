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

```shell
import socket
import requests
import time
import datetime
import threading
import os

# Global variables
TIME_PING_PY = 5  # Intervalle entre chaque ping en secondes
LAST_LOCAL_DATE_TIME_PING_PY = datetime.datetime.now()
continue_reading = True  # Flag pour arrêter le service si nécessaire

config = {
    "URL_ping": "http://ping.logitec.ma/ping_srv/RPI/SDC/",
    "Position": socket.gethostname()  # Example position
}

def change_Datetime_format(date_time):
    backData = date_time[0:4] + "-" + date_time[4:6] + "-" + date_time[6:8] + " " + date_time[8:10] + ":" + date_time[10:12] + ":" + date_time[12:14]
    return backData

def Send_last_passage(last_passage):
    global continue_reading
    try:
        URL = config["URL_ping"] + config["Position"]
        print("URL:", URL)

        my_req = requests.get(URL, verify=False, timeout=5)

        if my_req.status_code != 200:
            print("Ping YAPO : Echec, code:", my_req.status_code)
        else:
            rep = my_req.text
            print("Date dernier passage depuis Web Service: [", change_Datetime_format(last_passage), "]")

            if not rep.startswith("<html"):
                if my_req.text:
                    print("Ping YAPO :", my_req.text[:3], change_Datetime_format(my_req.text[3:]))
                else:
                    print("Ping YAPO : Réponse vide")

                if my_req.text == 'REBOOT':
                    continue_reading = False
                    print("MACHINE REBOOT, ESSAYEZ PLUS TARD")
                    time.sleep(1)
                    os.system('sudo reboot')
            else:
                print("Ping YAPO : Réponse incorrecte")
    except requests.exceptions.ConnectionError:
        print("Ping YAPO : Error Connecting", datetime.datetime.utcnow().strftime("%H:%M:%S"))
    except requests.exceptions.Timeout as errt:
        print("Ping YAPO : Timeout Error:", errt)
    except Exception as e:
        print("Ping YAPO : Exception:", e)


def ping_service():
    global LAST_LOCAL_DATE_TIME_PING_PY, TIME_PING_PY

    while continue_reading:
        if (datetime.datetime.now() - LAST_LOCAL_DATE_TIME_PING_PY).total_seconds() >= TIME_PING_PY:
            last_passage = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            LAST_LOCAL_DATE_TIME_PING_PY = datetime.datetime.now()
            print("LAST LOCAL DATETIME PING YAPO AT:", LAST_LOCAL_DATE_TIME_PING_PY.strftime("%H:%M:%S"))
            TIME_PING_PY = 60
            pLast_pass = threading.Thread(target=Send_last_passage, args=(last_passage,))
            pLast_pass.start()
            pLast_pass.join(5)

        time.sleep(1)

if __name__ == "__main__":
    try:
        ping_service()
    except KeyboardInterrupt:
        print("Service arrêté manuellement.")



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

