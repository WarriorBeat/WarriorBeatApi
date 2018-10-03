<img src="https://s3.amazonaws.com/warriorbeatapp-hosting-mobilehub-1527922673/imgs/logo.jpg" align="right" height="170" width=170>

# WarriorBeatApi

Flask Zappa API for Warrior Beat</br>
Hosted via AWS

## Install & Setup

### Dependencies / Prerequisites

- [Python 3.6](https://www.python.org/)
- [Zappa](https://github.com/Miserlou/Zappa)
- Python Virtual Environment (_[Pipenv recommended](https://pipenv.readthedocs.io/en/latest/)_)
- [AWS CLI](https://aws.amazon.com/cli/)

### Setup

Clone the Repo

```sh
$ git clone https://github.com/WarriorBeat/WarriorBeatApi.git

$ cd WarriorBeatApi
```

Create and enter python virtual environment. Install dependencies.

```sh
$ pipenv shell
$ pipenv install --dev
$ pipenv sync
```

Configure AWS if you have not already.

```sh
$ aws configure
# Enter your IAM name and secret key
```

> [AWS Configure Docs](https://docs.aws.amazon.com/cli/latest/reference/configure/index.html)

The server is now installed and configured.

## Setting up your Environment

To setup a development/testing environment, you require the following:

1. Flask Instance Config
2. Flask Env Variables
3. A Local AWS DynamoDB Server
4. A Local AWS S3 Storage Server

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

In order to run the application, you need to set some environment variables:

```sh
$ export FLASK_APP=warriorbeat
$ export FLASK_ENV=development
# To make use of local database/storage:
$ export FLASK_TESTING=True
```

> NOTE: SERVER_NAME is required if you wish to use/work on webhooks in your testing environment.

The Local AWS servers can be configured in a few different ways, but in my opinion the easiest way is to use [Docker](https://www.docker.com/).

Once you have Docker installed, you need to pull the images and run the docker containers.

**DynamoDB:**

Pull the image:

```sh
$ docker pull amazon/dynamodb-local
```

> By default, this dynamodb image keeps all its data in memory. Therefore, by restarting or stopping the container, you effectively wipe the testing database.
> You can read more [here](https://hub.docker.com/r/amazon/dynamodb-local/).

Run the image:

```sh
$ docker run -p 8000:8000
```

Running the image like this doesn't detach it from your active terminal process, so to stop it simply `ctrl-c`

**S3 Storage:**

Pull the image:

```sh
# To store all files in memory:
$ docker pull scality/s3server:mem-latest
# If you want to keep the files:
$ docker pull scality/s3server:latest
```

> For my purposes, I generally just run the S3 Server in memory. You can read more [here](https://hub.docker.com/r/scality/s3server/).

Run the image:

```sh
$ docker run -d --name s3server -p 9000:8000 scality/s3server:mem-latest
```

To start/stop the image:

```sh
# start
$ docker start s3server
# stop
$ docker stop s3server
```

### Running the Server

Once you have setup your environment, running the server is pretty simple.

Make sure your environment variables are set (as in step two from above), you docker containers are up and running, and run:

```sh
$ flask run
```

Or, make a quick `run` bash script if your like me and forget to reset your environment variables when starting to work again:

```sh
#!/usr/bin/env bash
export FLASK_APP=warriorbeat
export FLASK_ENV=development
export FLASK_TESTING=True

flask run
```

Save the above as `run` in the projects root directory and set it as executable:

```sh
$ chmod +x ./run
```

Now you can run the server by calling the script:

```
$ ./run
```

## Running the Tests

Finally, to ensure that everything is setup properly, you need to run the UnitTests in the `tests/` directory.

> Make sure to have your Docker containers and flask server running.

Generally your IDE will come with functionality to recognize and run these tests, but you can also run them via `python -m unittest` command.

For VSCode, the Python Extension comes with full testing suite functionality. To get it started, open the action menu via: `#(your OS super key, CMD for macOS) ⌘CMD + P` and select the `> Python: Discover Unit Tests` command. Following that, run the `> Python: Run All Unit Tests` command.

You should now have a full development/testing environment ready to go.
