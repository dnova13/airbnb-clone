# BY 장고, DB dump 작업

```
python manage.py dumpdata >data.json

# utf-8로 변환
python -Xutf8 ./manage.py dumpdata > data.json
```

# BY 장고, DB 복원

```
python manage.py loaddata data.json
```

# postgres 덤프

```
pg_dump -U username -d dbname > backup.sql
```

# postgres 복원

```
psql -U username -d dbname < backup.sql
```
