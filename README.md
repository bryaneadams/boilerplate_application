[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![forthebadge](https://forthebadge.com/images/badges/made-with-crayons.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg)](https://forthebadge.com)

# Boilerplate Application
This boilerplate is designed as a tutorial for deploying a Flask application with additional services.

# New to Docker? Go to [Getting Started](#-Getting-started)

This application contains the following services:

1. Flask Application
2. PostgresSQL
3. MinIO
4. Redis
5. A worker

The default is to use KeyCloak for authentication. I have commented out the decorators for requiring a login [here](https://github.com/bryaneadams/boilerplate_application/blob/9fe7878558bb57ac9e431ff3f53770cf3411a43a/flask-app/boilerplate/boilerform/boilerform.py#L35) and [here](https://github.com/bryaneadams/boilerplate_application/blob/9fe7878558bb57ac9e431ff3f53770cf3411a43a/flask-app/manage.py#L110). This is to help people new to authentication.

## Quick initial comments.

All environment variables used in the deployment are located in the [.env](https://github.com/bryaneadams/boilerplate_application/blob/main/.env) file.

### To run the tech stack

* Using prebuilt images
`docker-compose up`

* Building images
`docker-compose -f docker-compose-development.yml up`

### URLs

1. Application:  `localhost:5000`
2. MinIO:  `localhost:9000`

# Getting started

[![forthebadge](https://forthebadge.com/images/badges/reading-6th-grade-level.svg)](https://forthebadge.com)
## Docker what is Docker?!

I am assuming if you are new to Docker you are probably using a Windows machine. This is not a bad thing, in fact often at work it is all you get. You will need to install some services to use this repo. I will assume you have a `github` account and I will provide you a list of software to install (and recommend others).

### Install the following

#### Must have

1. Install [Docker](https://docs.docker.com/docker-for-windows/install/).

#### Nice to have (assuming you are using Windows, again this is just recommended)

1. Install [Git](https://git-scm.com/downloads)

### Getting started

Now the hard part is out of the way, go ahead and ensure Docker is running. For this I will assume you are using a Windows computer. In the bottom left-hand corner click the windows `start` button. Type `git` in the search menu and select [`Git Bash`](https://git-scm.com/downloads) `Git Bash`. Once the black window opens, type `docker ps` and you should get something back that looks like this:

```
% docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

If you got something that looks like this, then you most likely need to start Docker. In the bottom left-hand corner click the windows `start` button. Type `docker` and select `Docker Desktop`. This will get it running and repeat the step before.

[![forthebadge](https://forthebadge.com/images/badges/ctrl-c-ctrl-v.svg)](https://forthebadge.com)

### Pulling Docker Images

There are five Docker images used in this techstack. You can pull them using the following commands in any of your favorite OS's

```
docker pull <image_name>
```

For this you will need to run this application stack you will need to run the following lines of code:

* Note if you are going to paste into Git Bash, `Shift+Insert` is paste.
```
docker pull statculus/boilerplate_app:latest
docker pull statculus/boilerplate_worker:latest
docker pull bitnami/postgresql:latest
docker pull bitnami/minio:latest
docker pull bitnami/postgresql:latest
```

It might take a while, but now you will have five images saved locally.

### Run the application with its supporting services

Run the following command from the base directory of this repo.

```
docker-compose up
```

There will be a bunch of logs appear, but that is normal. After approximately 30 seconds your application will be running.

Visit [http://localhost:5000](http://localhost:5000) to see your application. Under `Create Form` select `Create New Form`. Type some text and click `Submit`. Next visit [http://localhost:9000](http://localhost:9000) and sign into MinIO. The default Access Key is [bryanisawesome](https://github.com/bryaneadams/boilerplate_application/blob/9fe7878558bb57ac9e431ff3f53770cf3411a43a/.env#L16) and Secret Key is [bryanrocks](https://github.com/bryaneadams/boilerplate_application/blob/9fe7878558bb57ac9e431ff3f53770cf3411a43a/.env#L17). Under the `results` bucket you will see a text file with the text you just typed. The name of the file will be [`dd-mm-yyyy_HH:MM:SS_Bryan_Rocks.txt`](https://github.com/bryaneadams/boilerplate_application/blob/9fe7878558bb57ac9e431ff3f53770cf3411a43a/worker/boiler_worker.py#L41)


[![forthebadge](https://forthebadge.com/images/badges/it-works-why.svg)](https://forthebadge.com)

### Pulling and building at once!

Run the following command from the base directory of this repo:

```
docker-compose up
```

If you have not pulled the images already, they will be pulled and start running!


[![forthebadge](https://forthebadge.com/images/badges/powered-by-black-magic.svg)](https://forthebadge.com)

### Ready to build them locally?

Run the following command from the base directory of this repo:

```
docker-compose -f docker-compose-development.yml up
```

Your images will build locally (might take some time) and then start running.



