# Developer Setup
This document provides instructions on how to set up the project on your local machine for development purposes.

## Prerequisites
Before you start, make sure the following tools are installed on your system:
- **Git:** Version control system to clone the project repository [Download Git](https://git-scm.com/downloads)
- **Docker:** To containerize the application and ensure it runs consistently across different environments [Download Docker](https://www.docker.com/products/docker-desktop)
- **Node.js v20 or newer:** JavaScript runtime to run the application [Download Node.js](https://nodejs.org/en/download/)
- **Python v3.10 or newer:** Programming language used in the project [Download Python](https://www.python.org/downloads/)


## Setup
Start by making a copy of the `.env.example` file and renaming it to `.env`. This file contains the environment variables that the application needs to run. You can change the values of the variables to match your environment.

Run the following command in the root folder to copy the `.env.example` file:
```bash
cp .env.example .env
```

Make sure to replace the placeholder values with your own values in the `.env` file.
You can generate an API-key [here](https://developers.google.com/custom-search/v1/introduction)

## Run for local development
To run the frontend of the project, you can use the following commands:
```bash
cd frontend;
npm install; npm run dev
```
This command will install the dependencies and start the application in development mode. You can access the application at `http://localhost:5173`.

The backend of the project can be run using the following commands:
```bash
cd backend;
python manage.py runserver 0.0.0.0:8000
```
