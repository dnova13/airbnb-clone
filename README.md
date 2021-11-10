# Airbnb Clone

Cloning Airbnb with Python, Django, Tailwind and more..


# mail accout
testnova0713@gmail.com

# package install
```
pipenv install pillow django-countries django-seed django-dotenv requests djangorestframework channels-redis channels
pipenv install awsebcli flake8 --dev
pipenv install black --dev --pre
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

#### docker
```
yum -y install docker 
systemctl start docker
docker run -p 6379:6379 -d redis:6.2.6
```

