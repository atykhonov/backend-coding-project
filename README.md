# Mozio Backend Potential hire Project 2.0

## Requirements

* Python 3.6
* PostgreSQL 9.6

# Installation

## Database configuration

Open `psql`:

```
$ sudo -u postgres psql
```

Create database:

```
postgres=# CREATE DATABASE mbcp_db;
```

Create database user:

```
postgres=# CREATE USER mbcp_user WITH ENCRYPTED PASSWORD 'password';
```

And grant all privileges:

```
postgres=# GRANT ALL PRIVILEGES ON DATABASE mbcp_db TO mbcp_user;
```

Connect to the created database:

```
postgres=# \c mbcp_db;
```

Enable the core postgis extension:

```
mbcp_db=# CREATE EXTENSION postgis;
```

