"""
This module serves as the entry point for the appointment booking application.
It initializes the Flask app, configures the database, and registers the API resources.
"""
import os
from flask import Flask
from flask_restful import Api
from database import db  # Import db from database.py
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///appointments.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db with app
db.init_app(app)

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
    # Create all database tables
    with app.app_context():
        db.create_all()

    # Run the Flask application
    app.run(debug=True)