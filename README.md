# Keemail Server

Never expose your personal email again

- [Keemail Server](#keemail-server)
  * [About / Synopsis](#about---synopsis)
  * [Installation](#installation)
    + [Docker](#docker)
    + [Basic Install](#basic-install)
      - [Env](#env)
      - [Requirements](#requirements)
      - [Migration](#migration)
  * [Run](#run)



## About / Synopsis

Keemail Server is the webserver part of Keemail. It's using python Flask + SQLAlchemy.

* Keemail allows you to easily generate aliases to your personal email address
* Provide a REST API to let you integrate it into your favorite tools
* Aliases are randomly generated but can be customized

## Installation

Keemail Server needs [Keemail Postfix](https://github.com/Guisch/keemailpostfix) to be installed in order to work. See the main [Keemail](https://github.com/Guisch/keemail) repo for a full detailed guides.



### Docker

You can automate deployment with Docker. Please visit the main [Keemail](https://github.com/Guisch/keemail) repo for a full detailed guide.



### Basic Install

#### Env

You need to set environment variables

| Name              | Required / Optional | Default       | Description                                              | Value                                 |
| ----------------- | ------------------- | ------------- | -------------------------------------------------------- | ------------------------------------- |
| KEEMAIL_SECRETKEY | Required            |               | Flask Session secret key                                 | Any random key                        |
| KEEMAIL_DB_URI    | Required            |               | Database URI including table name                        | `mysql://user:pass@domain:port/table` |
| KEEMAIL_DOMAIN    | Required            |               | Email alias domain                                       | example.com                           |
| KEEMAIL_ENV       | Optional            | `development` | Server environment (used for Flask and SqlAlchemy debug) | `development` or `production`         |
| FLASK_APP         | Required            |               | Flask entry point                                        | `run.py`                              |



#### Requirements

Keemail server is tested for Python3. Python 2.7 and lower are not supported. To install Python required, please use pip3

```bash
$ pip3 install -r requirements.txt
```



#### Migration

Keemail Server is using database migration through Flask. If it is the first time that you are setting up Keemail, please init the database

```bash
# Only run this command on first setup
$ flask db init
```

Then, create the migration file and upgrade the database. Please run the 2 following commands every time you upgrade Keemail Server

```bash
# Run those commands every time you update the server
$ flask db migrate
$ flask db upgrade
```



## Run

It is recommended that you run Keemail inside dockers, but if you prefer you can run the server. By default, the server is listening on `0.0.0.0:80`

```bash
$ python3 run.py
```

Alternatively, you can use Flask Run Script but you need first to setup env

```bash
$ export FLASK_APP=run.py
$ flask run
```

