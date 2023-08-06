# DockerizeMe

Generate Dockerfiles and run your applications as Docker containers quickly. Currently supports Spring Boot, Flask, and 
NodeJS applications.

## Installation
(Requires Python 3 and Docker daemon running.)
```
$ pip install dockerizeme
```

## Usage
In the root directory of your application, run:
```
$ dockerizeme --app-type TYPE_OF_APPLICATION
```
This creates a docker image called `dockerized-app` by default and runs it on the default port for the type of 
application.

Example:
```
$ dockerizeme --app-type SPRING_BOOT
```
Creates a docker image called `dockerized-app` for the spring boot application in the current directory and runs it on the port 8080.

For a full list of options and help, run:
```
$ dockerizeme --help
```
