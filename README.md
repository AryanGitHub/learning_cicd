# Contents
- [Tech Stack](#tech-stack)
- [Deployment](#deployment)
  - [Docker Deployment](#docker-deployment)
    - [Using Docker Compose](#using-docker-compose)
    - [Manually Building the Docker Image](#manually-building-the-docker-image)
  - [Manual Deployment](#manual-deployment)
- [Todo](#todo)
- [API Endpoints](#api-endpoints)
  - [Authentication](#-authentication)
  - [Users](#-users)
  - [Posts](#-posts)
  - [Voting](#-voting)

##  Tech Stack

  - **FastAPI**
  - **PostgreSQL**
  - **Pydantic**
  - **SQLAlchemy**
  - **Alembic**
  - **Uvicorn**
  - **JWT (JSON Web Tokens)**
  - **Hashing Libraries**
    - bcrypt
  - **Virtual Environments (venv)**
  - **`.env` File**
  - **Docker**

# Deployment

> **Note:**  
> **PLEASE DO REPLACE ENVIRONMENT VARIABLES**, `db_password` AND `secret` WITH A NEW PASSWORD in `.env` file and `./docker-compose.yaml`
> You can try the command to generate.

```bash
openssl rand -hex 100
```

#  Docker Deployment

This guide explains how to deploy the application using Docker. There are two methods available for deployment:

1. **Using Docker Compose** (Recommended) *(See the note below)*
2. **Manually Building the Image and Running the Container**

> **Note:**  
> The application requires a PostgreSQL database. The PostgreSQL instance is configured in the Docker Compose setup, not within the `cs_explorer_fastapi` image itself. The application will connect to the database container at runtime as per the specified environment configuration.

##  Using Docker Compose

## # 1. Starting the Docker Containers

To start the application with Docker Compose, run the following command:

```bash
docker-compose up --build --force-recreate
```

This command will:

  - Build the Docker images (if they are not already built).
  - Recreate any existing containers to ensure the latest changes are applied.

## # 2. Stopping the Docker Containers

To stop the running containers and remove them, execute:

```bash
docker-compose down
```

This will stop and remove all containers defined in the `docker-compose.yml` file.

##  Manually Building the Docker Image

## # 1. Building the Image Locally

If you prefer to manually build the Docker image, use the following command:

```bash
docker build -t cs_explorer_fastapi:1.0 .
```

This will build a Docker image with the tag `cs_explorer_fastapi:1.0`.

## # 2. Running the Docker Container

Once the image is built, you can start the container using:

```bash
docker run -p 8080:8000 cs_explorer_fastapi:1.0
```

This command will:

  - Start the container.
  - Map port `8080` on your host machine to port `8000` on the container, which is the port used by the FastAPI application.

#  Docker Deployment and Manual Deployment for FastAPI

This guide provides steps for deploying your FastAPI application using Docker and manually without Docker.

##  Prerequisites for Manual Deployment

Before proceeding with manual deployment, ensure the following prerequisites are installed on your system:

1. **Python** (version 3.7 or later)
     - Download and install Python from [python.org](https://www.python.org/).

2. **Pip** (Python package installer)
     - Pip comes pre-installed with Python. To verify, run:
     ```bash
     pip --version
     ```

3. **Dependencies** (Install from `requirements.txt`)
     - Install the necessary dependencies for the FastAPI application using the following command:
     ```bash
     pip install -r requirements.txt
     ```

##  Manual Deployment Steps

## # 1. Running the FastAPI Application

To manually start your FastAPI project, execute:

```bash
uvicorn app.main:app --port 8080
```

This command will:

  - Launch the FastAPI application.
  - Make it accessible on port `8080`.

## # 2. Testing the Application

Once the server is running, you can test the API by navigating to the following URLs in your web browser or API client (e.g., Postman):

  - **Interactive API Documentation (Swagger UI):** `http://localhost:8080/docs`
  - **ReDoc Documentation:** `http://localhost:8080/redoc`

##  Todo

  - [ ] Implement API security measures (e.g., rate limiting)
  - [ ] Write tests for the application
  - [ ] Create Docker development configuration file
  - [ ] Create Docker production configuration file
  - [ ] Set up CI/CD pipeline
  - [ ] Create Terraform file for infrastructure deployment
  - [ ] Implement Ansible for deployment automation

##  API Endpoints

## # Authentication

  - **Login**
    - **POST** `/login`
      - **Description**: Get a token from credentials.
      - **Request Body**:
        - `username`: string
        - `password`: string
      - **Responses**:
        - `200`: Successful response with access token.
        - `422`: Validation error.

## # Users

  - **Create User**
    - **POST** `/users`
      - **Description**: Create a new user.
      - **Request Body**:
        - `username`: string
        - `email`: string
        - `password`: string
      - **Responses**:
        - `201`: Successful response with user details.
        - `422`: Validation error.

  - **Get User by Username**
    - **GET** `/users/username/{username}`
      - **Description**: Retrieve user details by username.
      - **Parameters**:
        - `username`: string (path parameter)
      - **Responses**:
        - `200`: Successful response with user details.
        - `422`: Validation error.

## # Posts

  - **Get All Posts**
    - **GET** `/posts` and `/posts/all`
      - **Description**: Retrieve all posts.
      - **Responses**:
        - `200`: Successful response with a list of posts.

  - **Create Post**
    - **POST** `/posts`
      - **Description**: Create a new post.
      - **Request Body**:
        - `title`: string
        - `description`: string (optional)
        - `http_link`: string
      - **Responses**:
        - `201`: Successful response with post details.
        - `422`: Validation error.

  - **Get Post by ID**
    - **GET** `/posts/{id}`
      - **Description**: Retrieve a post by its ID.
      - **Parameters**:
        - `id`: integer (path parameter)
      - **Responses**:
        - `200`: Successful response with post details.
        - `422`: Validation error.

  - **Update Post**
    - **PUT** `/posts/{id}`
      - **Description**: Update an existing post.
      - **Parameters**:
        - `id`: integer (path parameter)
      - **Request Body**:
        - `title`: string
        - `description`: string (optional)
        - `http_link`: string
      - **Responses**:
        - `200`: Successful response with updated post details.
        - `422`: Validation error.

  - **Delete Post**
    - **DELETE** `/posts/{id}`
      - **Description**: Delete a post by its ID.
      - **Parameters**:
        - `id`: integer (path parameter)
      - **Responses**:
        - `204`: Successful response (no content).
        - `422`: Validation error.

## # Voting

  - **Upvote Post**
    - **GET** `/votes/up/{post_id}`
      - **Description**: Set an upvote on a post by its ID.
      - **Parameters**:
        - `post_id`: integer (path parameter)
      - **Responses**:
        - `201`: Successful response with vote details.
        - `422`: Validation error.

  - **Downvote Post**
    - **GET** `/votes/down/{post_id}`
      - **Description**: Set a downvote on a post by its ID.
      - **Parameters**:
        - `post_id`: integer (path parameter)
      - **Responses**:
        - `201`: Successful response with vote details.
        - `422`: Validation error.
