# Airbnb Clone
Cloning Airbnb with Python, Django, Tailwind and more..


# mail account
testnova0713@gmail.com


# virtual enviroment setting.


## 1. pipenv setting(recommed window)
### pipenv shell & pakage install
```
pipenv shell
pipenv install <package-name>
```


### package install
```
pipenv install pillow django-countries django-seed django-dotenv requests djangorestframework channels-redis channels
pipenv install awsebcli flake8 --dev
pipenv install black --dev --pre
```
  

  
## 2. venv setting
### venv 
```
python -m venv .venv
source .venv/Scripts/activate
```
  

# pip upgrade
```
pip install --upgrade pip
```
  

# pip rollback
```
python -m ensurepip
```
  

# rerequirements 
```
pip freeze > requirements.txt
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip uninstall -r requirements.txt -y
```

# stat django-project
```
django-admin startproject config
```

# translate commend
```
django-admin makemessages -l ko
django-admin makemessages -d djangojs -l ko
django-admin compilemessages
```

# migration command
```
python manage.py makemigrations
python manage.py migrate
```

# channel setting
#### commend
```
pipenv install channls
pipenv install channels-redis
```

# static file upload
```
python manage.py collectstatic
```

#### docker
```
yum -y install docker 
systemctl start docker
docker run -p 6379:6379 -d redis:6.2.6

docker network create redis-net
docker run --name airb -p 6379:6379 --network redis-net -d redis:6.2.6 redis-server --appendonly yes
```

