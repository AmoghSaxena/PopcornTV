# Auto Provisioning Cloud Server.


#### This is the Auto Provisioning Cloud Server files which can be hosted as Standalone or Dockerized Container


## To Run the server follow the Steps below!

> Step 1 [Clone this Repository]
```
git clone https://github.com/AmoghSaxena/APS.git AutoProvisionCloud
```

> Step 2 [Change the Working directory to the cloned directory]
```
cd AutoProvisionCloud
```

###  To Start with it with Docker you can run few Simple Commands

> Step 3 [Build the image of it]
```
docker build -t autoprovision:1.0 .
```

> Step 4 [Run the container with the same image]
```
docker run -d --name autoprovisioncloud -p 8042:5085 -v autoprovisiondatabase:/var/lib/mysql autoprovision:1.0
```

> Step 5 [Make Initial Migrations]
```
docker exec -it autoprovisioncloud /migrate
```

> Step 6 [Run the Cloud Server]
```
docker exec -itd autoprovisioncloud gunicorn --config gunicorn-cfg.py AutoProvision.wsgi
```

### To Start with it as a Standalone
> Step 3 [Install the Requirements - Make sure you Have Python3.8 +]
```
pip install -r requirements.txt
```

> Step 4 [To perform Migrations]
```
python manage.py makemigrations
```

> Step 5 [To migrate the database]
```
python manage.py migrate
```

> Step 6 [This will run your server on Port 5085]
```
gunicorn --config gunicorn-cfg.py AutoProvision.wsgi
```

