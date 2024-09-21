"""
This module defines the database models for the appointment booking system.
It includes the 'Appointment' model representing appointment records.
"""

from database import db  # Import db from database.py

class Appointment(db.Model):
    """
    Represents an appointment in the scheduling system.

    Attributes:
        id (int): The unique identifier for the appointment.
        client_name (str): The name of the client.
        date (datetime.date): The date of the appointment.
        time (datetime.time): The time of the appointment.
        status (str): The status of the appointment ('scheduled', 'canceled', etc.).
    """

    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='scheduled')
