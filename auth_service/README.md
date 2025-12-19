# Auth Microservice

This is one of the foremost microservices that is responsible for authenticating users who are trying to access the system. 

This microservice handles the creation as well as the authorization of the users.

## Technology Used

The entire `auth_service` is written in `FastAPI`, an asynchronous Python framework that is scalable and efficient for developing a backend. 

The entire project has been deployed by using `Docker`, a software that is helpful to deploy applications.

## Requirements

Ensure that for a local deployment, you have the following installed:
- Python 3.11 or higher 
- MongoDB 

In case you are using Docker, install the required dependencies for Docker.

## Local Runner

You can run this application locally by using the `start_server.sh` in `app/` directory. Run the following to start application locally:

```bash
cd app
chmod +x start_server.sh
./start_server.sh
```

## Docker Helper

### Running The Application
To run the Docker application, you need to build an image of this microservice. This service usually runs on port `4500`, and you can build the image as follows:

```bash
docker-compose up --build
```

This will create two images: one for `auth_service` and one for the `db` i.e. MongoDB.
