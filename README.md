# Airbnb Clone

Cloning Airbnb with Python, Django, Tailwind and more..

# mail account

```
testnova0713@gmail.com
```

# test account

```

id : test_account11@gmail.com
id : test_account22@gmail.com
id : test_account33@gmail.com
pw : 1q2w3e4r
```

# virtual enviroment setting (select 1 or 2.)

## - pipenv setting(recommed window)

### pipenv install

```
pip install --user pipenv
```

### pipenv shell & pakage install

```
# 가상환경 활성화
pipenv shell

# 패키치 설치
pipenv install <package-name>

```

### package install

```
pipenv install pillow django-countries django-seed django-dotenv requests djangorestframework channels-redis channels
pipenv install awsebcli flake8 --dev
pipenv install black --dev --pre
```

## - venv setting

### venv

```
# 가상환경 위치 셋팅
python -m venv .venv

# 가상환경 활성화
source .venv/Scripts/activate

# 가상환경 종료
deactivate

```

---

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
# requirements pip 패키지 추출
pip freeze > requirements.txt

# requirements 추출한 pip 패키지 설치
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 삭제 명령어(질의 없이)
pip uninstall -r requirements.txt -y
```

# start server

```

python manage.py runserver <port>

python manage.py runserver 8080

python manage.py runserver --port 8000

python manage.py runserver <ip>:<port>

python manage.py runserver 127.0.0.1:8000
```

# 장고 셸 활성

```
python manage.py shell

```

# start django-project

```

django-admin startproject config

```

# translate commend

```
django-admin makemessages -l ko
django-admin makemessages -d djangojs -l ko
django-admin compilemessages

```

-   주의사항 : 서버 배포시 `gettext` 패키지 필요 없다면 아래 명령어로 `gettext` 설치

```
# 우분투
sudo apt-get install gettext


# centsot
sudo yum install gettext-devel
or
sudo yum install gettext

```

# migration command

```
# 장고내 데이터에 대한 추가/수정/삭제시 마이그레이션 파일로 만드는 명령어

python manage.py makemigrations

# 생성된 마이그레이션 파일을 실제 데이터에 적용.

python manage.py migrate

```

# channel setting install

### command

```

pipenv install channls
pipenv install channels-redis

```

# static file upload( static 파일 s3 등 업로드)

```

python manage.py collectstatic
python manage.py collectstatic --no-input ## 따로 인풋없이 static 업로드

```

# docker-redis(local)

```

yum -y install docker
systemctl start docker
docker run -p 6379:6379 -d redis:6.2.6

docker network create redis-net
docker run --name airb -p 6379:6379 --network redis-net -d redis:6.2.6 redis-server --appendonly yes

```

# 처음 배포 시 실행 명령어.

```

sudo yum install postgresql-devel
sudo yum install gettext-devel
```

# static 파일 s3 등 업로드

```
python manage.py compilemessages
or
python manage.py collectstatic --no-input

```

# 배포시 psycopg2 설치 되지않아 에러날 시

```

requirements.txt psycopg2 대신에 psycopg2-binary 로 변경.

```

# 로그 확인

```
sudo tail -f /var/log/service/uwsgi.log

```

# 서버 재시작 명령어

```
sudo systemctl start nginx uwsgi daphne

```

# docker-supervior 명령어

```
# supervisor start/stop/restart/status
supervisorctl start uwsgi
supervisorctl restart uwsgi
supervisorctl stop uwsgi
supervisorctl status uwsgi

supervisorctl restart all


# supervior 갱신
supervisorctl reread && supervisorctl update
```
