# API Setup
1) Now that you have the project pulled down, create another directory adjacent to the root of this project called `postgres-volume`, with the file system looking like this:
    1) PARENT DIR
        1) PROJECT DIR
        2) postgres-volume
        3) ...
2) To setup a development PostgreSQL DB with Adminier, run the Docker compose file from the root of the project directory: `docker compose -f docker-development.yaml -d up`
    1) This will create the containers and immediately start them. You can manage them using Docker Desktop or the Docker CLI from now on. 
3) It is recommended to use `Pyenv` for Python version control in addition to `Pipenv` which is used to manage project dependencies (both are already in use by the project and should configure properly if you have these tools installed). 
    1) On first start-up of the project will need to run:
        1) `pipenv install` to get all project dependencies in the shell
        2) `pipenv shell` if not already in the shell. Use this in the future whenever you need to use the CLI with this project (like for running it).
4) Copy `example.env` from `envs/` directory and rename it to `.env` placing it in the root of the project. This will be used to pull environment variables from during developlment. The example is a template that will be useful only for local work, assuming you have been following this guide.
5) To start the development server, use: `fastapi dev --host 0.0.0.0 --port 8000`
    1) This will start the server in development mode and make it accessible via `localhost:8000` in the browser as well as make it able to receive connections via other devices on the network.
    2) OpenAPI docs are accessible via `localhost:8000/docs`
    3) Alembic handles migrations. Run `alembic upgrade head` to migrate to the most recent database update
