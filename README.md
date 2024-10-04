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
  ```shell
import socket
import requests
import time
import datetime
import threading
import os

# Variables globales
config = {
    "URL_ping": "http://0.0.0.0/ping_srv/{device}/{company}/",
    "Position": socket.gethostname() # Exemple de position
}

TIME_PING_PY = 5  # Intervalle entre chaque ping en secondes
LAST_LOCAL_DATE_TIME_PING_PY = datetime.datetime.now()

continue_reading = True  # Flag pour arrêter le service si nécessaire


# Fonction pour changer le format de la date et heure
def change_Datetime_format(date_time):
    backData = date_time[0:4] + "-" + date_time[4:6] + "-" + date_time[6:8] + " " + date_time[8:10] + ":" + date_time[
                                                                                                            10:12] + ":" + date_time[
                                                                                                                           12:14]
    return backData


# Fonction pour envoyer un ping et gérer la réponse
def Send_last_passage(last_passage):
    global continue_reading
    try:
        # Construire l'URL
        URL = config["URL_ping"] + config["Position"]
        print("URL:", URL)

        # Effectuer la requête
        my_req = requests.get(URL, verify=False, timeout=5)

        # Gérer la réponse
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


# Fonction principale pour lancer le service
def ping_service():
    global LAST_LOCAL_DATE_TIME_PING_PY, TIME_PING_PY

    while continue_reading:
        if (datetime.datetime.now() - LAST_LOCAL_DATE_TIME_PING_PY).total_seconds() >= TIME_PING_PY:
            # Réinitialisation des temps
            last_passage = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            LAST_LOCAL_DATE_TIME_PING_PY = datetime.datetime.now()
            print("LAST LOCAL DATETIME PING YAPO AT:", LAST_LOCAL_DATE_TIME_PING_PY.strftime("%H:%M:%S"))
            TIME_PING_PY = 60
            # Lancer le thread pour envoyer le ping
            pLast_pass = threading.Thread(target=Send_last_passage, args=(last_passage,))
            pLast_pass.start()
            pLast_pass.join(5)  # Attend 5 secondes que le thread se termine

        time.sleep(1)  # Pour éviter une boucle trop intensive


# Lancer le service
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

