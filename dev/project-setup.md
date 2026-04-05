# API Setup
1) Now that you have the project pulled down, create another directory adjacent to the root of this project called `postgres-volume`, with the file system looking like this:
    1) PARENT DIR
        1) PROJECT DIR
        2) postgres-volume
        3) ...
2) To setup a development PostgreSQL DB with Adminier, run the Docker compose file from the root of the project directory: `docker compose -f docker-development.yaml -d up`
    1) This will create the containers and immediately start them. You can manage them using Docker Desktop or the Docker CLI from now on. 
3) It is recommended to use `Pyenv` for Python version control in addition to `Pipenv` which is used to manage project dependencies (both are already in use by the project and should configure properly if you have these tools installed). 
4) To start the development server, use: `fastapi dev --host 0.0.0.0 --port 8000`
    1) This will start the server in development mode and make it accessible via `localhost:8000` in the browser as well as make it able to receive connections via other devices on the network.
    2) OpenAPI docs are accessible via `localhost:8000/docs`
