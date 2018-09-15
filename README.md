<img src="https://s3.amazonaws.com/warriorbeatapp-hosting-mobilehub-1527922673/imgs/logo.jpg" align="right" height="170" width=170>

# WarriorBeatApi

Flask Serverless API for Warrior Beat</br>
Hosted via AWS

## Install & Setup

### Dependencies / Prerequisites

- [Python 3.7](https://www.python.org/)
- [Yarn](https://yarnpkg.com/en/)
- [Serverless](https://serverless.com/)
- Python Virtual Environment (_[Pipenv recommended](https://pipenv.readthedocs.io/en/latest/)_)
- [AWS CLI](https://aws.amazon.com/cli/)

### Setup

Clone the Repo

```sh
$ git clone https://github.com/WarriorBeat/WarriorBeatApi.git

$ cd WarriorBeatApi
```

Install the rest of the dependencies via yarn.

```sh
$ yarn
```

Create and enter python virtual environment. Install dependencies.

```sh
$ pipenv shell
$ pipenv update --dev
$ pipenv sync
```

Configure AWS if you have not already.

```sh
$ aws configure
# Enter your IAM name and secret key
```

> [AWS Configure Docs](https://docs.aws.amazon.com/cli/latest/reference/configure/index.html)

Install Serverless dynamodb local.

```sh
$ serverless dynamodb install
```

Create an instance config file for flask.

```sh
# In WarriorBeatAPI folder
$ mkdir instance && cd instance
$ touch instance/config.py
```

In instance/config.py, configure as you wish. Here is a sample instance/config.py:

```python
# instance/config.py
DEBUG = True
SECRET_KEY = 'superdupersecretkey'
SERVER_NAME = 'localhost:5000'
```

> NOTE: SERVER_NAME is required in order to properly point API url_for calls to the absolute url path.

The Server is now ready to be ran whenever needed.

### Running the Server

Running the server at full functionality requires starting three seperate services:

1.  Dynamodb Local - (_Database_)
2.  S3 Local - (_File Storage_)
3.  WSGI Server - (_Serverless & Flask Offline_)

There are two methods to do so.

**Method 1:**

Run all three in a detached process.

```sh
$ yarn detach_local
# or "yarn dlo" for a shortcut
```

> Note: If you are unable to stop the server, kill the services by killing the processing running on ports: 5000 (wsgi), 8000 (dynamodb), and 9000 (s3 bucket)

**Method 2:**

Run all three services in seperate terminal windows.

```sh
$ yarn startdb # starts database
$ yarn starts3 # starts s3 server
$ yarn local # starts local wsgi/sls server
```

---

Server should now be up and running. When restarting the WarriorBeatApp, you should see the following:

> CONNECTED TO LOCALHOST

In the console.
