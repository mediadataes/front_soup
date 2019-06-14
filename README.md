# Front soup

Download give newspapers in different schedules


## Docker

For exec the complete project, you should run:

```
$ docker-compose up -d
```

The fisrt time you execute the project, you must create database:

```
$ docker exec -ti fs_db psql -U postgres -c "create user front_soup password 'front_soup'"
$ docker exec -ti fs_db psql -U postgres -c "create database front_soup owner front_soup"
$ docker exec -ti fs_db psql -U postgres -c "alter user front_soup createdb"
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
