# Front soup

Download give newspapers in different schedules


## Docker

For exec the complete project, you should run:

```
$ docker-compose up -d
```

This will wake up the full environment in localhost:8000


## Create admin user

You need to create a superuser for enter in django admin:

```
$ docker exec -ti fs_web python manage.py createsuperuser
```


## Add newspapers and review extract datas


1. Enter in localhost:8000/admin and enter your credentials
2. Add new newspaper in NEWSPAPER section and save it
3. Wait some time and you could see some download html in DATA section


## Run tests

```
$ docker exec -ti fs_web python manage.py test
```
