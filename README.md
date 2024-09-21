# Flask Appointment Booking System

<!-- ![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.x-green.svg)
![Heroku](https://img.shields.io/badge/deployed-on-Heroku-purple.svg) -->

## Table of Contents

- [Flask Appointment Booking System](#flask-appointment-booking-system)
  - [Table of Contents](#table-of-contents)
  - [Project Description](#project-description)
  - [Features](#features)
  - [Technologies Used](#technologies-used)
  - [Project Structure](#project-structure)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Steps](#steps)
  - [Configuration](#configuration)
    - [Environment Variables](#environment-variables)
  - [Usage](#usage)
    - [Running Locally](#running-locally)
  - [API Endpoints](#api-endpoints)
    - [1. Schedule an Appointment](#1-schedule-an-appointment)
    - [2. Cancel an Appointment](#2-cancel-an-appointment)
    - [3. Reschedule an Appointment](#3-reschedule-an-appointment)
  - [Deployment](#deployment)
    - [Deploying to Heroku](#deploying-to-heroku)
      - [1. **Create a Heroku Account**](#1-create-a-heroku-account)
      - [2. **Install the Heroku CLI**](#2-install-the-heroku-cli)
      - [3. **Login to Heroku**](#3-login-to-heroku)
      - [4. **Create a Heroku App**](#4-create-a-heroku-app)
      - [5. **Add the Heroku Remote**](#5-add-the-heroku-remote)
      - [6. **Provision the PostgreSQL Add-on**](#6-provision-the-postgresql-add-on)
      - [7. **Commit and Push Your Code**](#7-commit-and-push-your-code)
      - [8. **Run Database Migrations**](#8-run-database-migrations)
      - [9. **Verify Deployment**](#9-verify-deployment)
      - [10. **Monitor Logs**](#10-monitor-logs)
  - [Testing](#testing)
    - [Manual Testing](#manual-testing)
  - [Contributing](#contributing)
  - [Contact](#contact)

## Project Description

The **Flask Appointment Booking System** is a backend application designed to manage appointment scheduling, cancellations, and rescheduling for services or businesses. Built with Flask and SQLAlchemy, it offers a RESTful API that allows clients to interact seamlessly with the appointment system, ensuring real-time updates of available slots. The application is deployed on Heroku and utilizes PostgreSQL for robust data management.

## Features

- **Appointment Scheduling**: Book appointments by specifying the date, time, and client name.
- **Cancellation**: Cancel existing appointments.
- **Rescheduling**: Modify the date and time of existing appointments.
- **Real-time Availability**: Automatically updates available slots as appointments are managed.
- **API Documentation**: Comprehensive endpoints for easy integration with front-end applications.
- **Database Migrations**: Managed using Flask-Migrate for seamless schema changes.

## Technologies Used

- **Programming Language**: Python 3.8+
- **Web Framework**: Flask
- **API Framework**: Flask-RESTful
- **Database ORM**: Flask-SQLAlchemy
- **Database**: PostgreSQL (Heroku Postgres)
- **Deployment Platform**: Heroku
- **Web Server**: Gunicorn
- **Version Control**: Git & GitHub
- **Environment Management**: python-dotenv

## Project Structure

```
appointment_booking_system/
├── app.py
├── database.py
├── models.py
├── resources/
│   └── appointment.py
├── migrations/
│   └── ... (Flask-Migrate files)
├── requirements.txt
├── Procfile
├── README.md
└── .gitignore
```

- **app.py**: Initializes the Flask application, configures the database, and registers API resources.
- **database.py**: Sets up the SQLAlchemy database instance.
- **models.py**: Defines the database models (e.g., `Appointment`).
- **resources/appointment.py**: Contains API resource classes for managing appointments.
- **migrations/**: Directory managed by Flask-Migrate for handling database migrations.
- **requirements.txt**: Lists all Python dependencies.
- **Procfile**: Specifies the commands Heroku should run to start the application.
- **README.md**: Documentation of the project.
- **.gitignore**: Specifies files and directories to be ignored by Git.

## Installation

### Prerequisites

- **Python 3.8+** installed on your system.
- **pip** package manager.
- **Git** installed for version control.
- **Heroku CLI** installed for deployment.
- **PostgreSQL Account** (e.g., [ElephantSQL](https://www.elephantsql.com/)) for external database hosting.

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/varunbhtt21/appointment_booking_system
   cd appointment_booking_system
   ```

2. **Create and Activate a Virtual Environment** (optional but recommended)

   ```bash
   python -m venv venv
   ```

   - **On Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **On macOS/Linux:**

     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the project root (optional for local development) and add the following:

   ```dotenv
   DATABASE_URL=postgresql://username:password@hostname:port/database_name
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   ```

   **Note:** Ensure the `.env` file is added to `.gitignore` to prevent sensitive information from being committed.

## Configuration

### Environment Variables

The application uses environment variables to manage configurations securely. Below are the essential variables:

- **`DATABASE_URL`**: Connection string for the PostgreSQL database.
- **`FLASK_APP`**: Entry point of the Flask application (`app.py`).
- **`FLASK_ENV`**: Environment mode (`development` or `production`).
- **`SECRET_KEY`**: Secret key for Flask sessions and security.

**Setting Environment Variables on Heroku:**

```bash
heroku config:set DATABASE_URL='postgresql://username:password@hostname:port/database_name'
heroku config:set FLASK_APP=app.py
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY='your_production_secret_key'
```

## Usage

### Running Locally

1. **Activate the Virtual Environment**

   ```bash
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

2. **Set Environment Variables**

   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   export DATABASE_URL=postgresql://username:password@hostname:port/database_name
   export SECRET_KEY=your_secret_key
   ```

   **Note:** On Windows Command Prompt, use `set` instead of `export`.

3. **Run Database Migrations**

   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

4. **Start the Flask Server**

   ```bash
   flask run
   ```

   The application will be accessible at `http://localhost:5000`.

## API Endpoints

### 1. Schedule an Appointment

- **URL**: `/schedule`
- **Method**: `POST`
- **Description**: Book an appointment by specifying the date, time, and client name.
- **Request Body**:

  ```json
  {
    "client_name": "John Doe",
    "date": "2024-10-15",
    "time": "14:00"
  }
  ```

- **Success Response**:

  - **Status Code**: `201 Created`
  - **Content**:

    ```json
    {
      "message": "Appointment scheduled successfully.",
      "appointment_id": 1
    }
    ```

- **Error Responses**:
  - **Status Code**: `400 Bad Request`
    - **Message**: "Invalid date or time format." or "Time slot is not available."

### 2. Cancel an Appointment

- **URL**: `/cancel/<appointment_id>`
- **Method**: `POST`
- **Description**: Cancel an existing appointment by its ID.
- **Success Response**:

  - **Status Code**: `200 OK`
  - **Content**:

    ```json
    {
      "message": "Appointment canceled successfully."
    }
    ```

- **Error Responses**:
  - **Status Code**: `404 Not Found`
    - **Message**: "Appointment not found."
  - **Status Code**: `400 Bad Request`
    - **Message**: "Appointment is already canceled."

### 3. Reschedule an Appointment

- **URL**: `/reschedule/<appointment_id>`
- **Method**: `POST`
- **Description**: Reschedule an existing appointment to a new date and time.
- **Request Body**:

  ```json
  {
    "date": "2024-10-16",
    "time": "15:00"
  }
  ```

- **Success Response**:

  - **Status Code**: `200 OK`
  - **Content**:

    ```json
    {
      "message": "Appointment rescheduled successfully."
    }
    ```

- **Error Responses**:
  - **Status Code**: `404 Not Found`
    - **Message**: "Appointment not found."
  - **Status Code**: `400 Bad Request`
    - **Message**: "Cannot reschedule a canceled appointment." or "New time slot is not available." or "Invalid date or time format."

## Deployment

### Deploying to Heroku

Your application is already deployed on Heroku. Here's a summary of the deployment steps for future reference or for others who might use this guide.

#### 1. **Create a Heroku Account**

Sign up for a free account at [Heroku](https://www.heroku.com/) if you haven't already.

#### 2. **Install the Heroku CLI**

The Heroku CLI allows you to manage and deploy applications from the command line.

- **For macOS/Linux:**

  ```bash
  curl https://cli-assets.heroku.com/install.sh | sh
  ```

- **For Windows:**

  Download and run the installer from the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) page.

#### 3. **Login to Heroku**

```bash
heroku login
```

This command opens a web browser for you to log in.

#### 4. **Create a Heroku App**

```bash
heroku create your-app-name
```

Replace `your-app-name` with a unique name for your application. If omitted, Heroku generates a random name.

#### 5. **Add the Heroku Remote**

If you haven't already added the Heroku remote, do so with:

```bash
heroku git:remote -a appointment-booking-system-be
```

#### 6. **Provision the PostgreSQL Add-on**

Since Heroku no longer offers free PostgreSQL plans, you'll need to choose a paid plan or use an external PostgreSQL service.

**Using Heroku Postgres (Paid Plan):**

```bash
heroku addons:create heroku-postgresql:hobby-basic
```

**Using an External PostgreSQL Service (e.g., ElephantSQL):**

1. **Sign Up** for [ElephantSQL](https://www.elephantsql.com/) and create a new instance.
2. **Copy the Database URL** provided by ElephantSQL.
3. **Set the `DATABASE_URL`** environment variable on Heroku:

   ```bash
   heroku config:set DATABASE_URL='postgresql://username:password@hostname:port/database_name'
   ```

#### 7. **Commit and Push Your Code**

Ensure all changes are committed:

```bash
git add .
git commit -m "Deploy to Heroku"
```

Push to Heroku:

```bash
git push heroku main  # or 'master' if your branch is named 'master'
```

#### 8. **Run Database Migrations**

If using Flask-Migrate:

```bash
heroku run flask db init
heroku run flask db migrate -m "Initial migration."
heroku run flask db upgrade
```

**Or, using `db.create_all()`:**

```bash
heroku run python
```

Inside the Python shell:

```python
from app import app, db

with app.app_context():
    db.create_all()

exit()
```

#### 9. **Verify Deployment**

Access your application via:

```bash
heroku open
```

Test the API endpoints to ensure everything is functioning correctly.

#### 10. **Monitor Logs**

To troubleshoot any issues, monitor the Heroku logs:

```bash
heroku logs --tail
```

## Testing

### Manual Testing

Use **Postman**, **cURL**, or any REST client to manually test the API endpoints.

**Example cURL Command to Schedule an Appointment:**

```bash
curl -X POST https://appointment-booking-system-be-2098804bc63d.herokuapp.com/schedule \
     -H "Content-Type: application/json" \
     -d '{
           "client_name": "Jane Doe",
           "date": "2024-10-20",
           "time": "10:00"
         }'
```

**Expected Response:**

```json
{
  "message": "Appointment scheduled successfully.",
  "appointment_id": 1
}
```

## Contributing

Contributions are welcome! To contribute to this project, please follow these guidelines:

1. **Fork the Repository**

   Click the "Fork" button at the top-right corner of the repository page on GitHub.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/varunbhtt21/appointment_booking_system
   cd appointment_booking_system
   ```

3. **Create a New Branch**

   ```bash
   git checkout -b feature/AmazingFeature
   ```

4. **Make Your Changes**

   Implement your feature or bug fix.

5. **Commit Your Changes**

   ```bash
   git commit -m "Add AmazingFeature"
   ```

6. **Push to Your Fork**

   ```bash
   git push origin feature/AmazingFeature
   ```

7. **Open a Pull Request**

   Navigate to the original repository on GitHub and click "Compare & pull request."

## Contact

For any inquiries or issues, please open an issue on the [GitHub repository](https://github.com/yourusername/appointment_booking_system/issues) or contact me directly at [Email](varunbhatt21@gmail.com).

---
