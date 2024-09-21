"""
This module serves as the entry point for the appointment booking application.
It initializes the Flask app, configures the database, and registers the API resources.
"""
import os
from flask import Flask
from flask_restful import Api
from database import db  # Import db from database.py
from dotenv import load_dotenv
from models import Appointment  
from flask_migrate import Migrate
from urllib.parse import urlparse, urlunparse


load_dotenv()  # Load variables from .env file

app = Flask(__name__)

# Retrieve the DATABASE_URL from environment variables
db_url = os.environ.get('DATABASE_URL', 'sqlite:///appointments.db')

# Check if the URL starts with 'postgres://' and replace it with 'postgresql://'
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)

# Configure the database using the corrected DATABASE_URL
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db with app
db.init_app(app)

# After initializing db
migrate = Migrate(app, db)

# Initialize Flask-RESTful API
api = Api(app)

# Import resources after initializing db to avoid circular imports
from resources.appointment import (
    AppointmentSchedule,
    AppointmentCancel,
    AppointmentReschedule
)

# Register resources with the API
api.add_resource(AppointmentSchedule, '/schedule')
api.add_resource(AppointmentCancel, '/cancel/<int:appointment_id>')
api.add_resource(AppointmentReschedule, '/reschedule/<int:appointment_id>')


if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)