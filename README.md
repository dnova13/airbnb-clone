# Airbnb Clone
Cloning Airbnb with Python, Django, Tailwind and more..


# mail account
testnova0713@gmail.com


# virtual enviroment setting.

## 1. pipenv setting(recommed window)

### pipenv install
```
pip install --user pipenv
```

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
### commend
```
pipenv install channls
pipenv install channels-redis
```

# static file upload
```
python manage.py collectstatic
python manage.py collectstatic --no-input ## 따로 인풋없이 static 업로드
```

#### docker(local)
```
yum -y install docker 
systemctl start docker
docker run -p 6379:6379 -d redis:6.2.6

docker network create redis-net
docker run --name airb -p 6379:6379 --network redis-net -d redis:6.2.6 redis-server --appendonly yes
```


#### 배포 시 명령어.
```
sudo yum install postgresql-devel
sudo yum install gettext-devel

python manage.py compilemessages
python manage.py collectstatic --no-input
```

#### 배포시 psycopg2 설치 되지않아 에러날 시
```
requirements.txt psycopg2 대신에 psycopg2-binary 로 변경.
```

#### 로그 확인
```
sudo tail -f /var/log/service/uwsgi.log
```

#### 서버 재시작 명령어
```
sudo systemctl start nginx uwsgi daphne 
```