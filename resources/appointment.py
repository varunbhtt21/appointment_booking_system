"""
This module defines the resources for scheduling, canceling, and rescheduling appointments.
Each resource corresponds to an API endpoint and handles the necessary logic for appointment management.
"""

from flask_restful import Resource, reqparse
from models import Appointment
from datetime import datetime
from database import db  # Import db from database.py

class AppointmentSchedule(Resource):
    """
    Resource for scheduling new appointments.

    Methods:
        post(): Handles POST requests to schedule a new appointment.
    """

    def post(self):
        """
        Schedule a new appointment if the requested time slot is available.

        Parses the incoming request data for client name, date, and time.
        Validates the input, checks for slot availability, and creates a new
        appointment if possible.

        Returns:
            tuple: A JSON response with a success message and appointment ID,
                   and an HTTP status code.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('client_name', required=True, help="Client name is required.")
        parser.add_argument('date', required=True, help="Date is required. Format: YYYY-MM-DD")
        parser.add_argument('time', required=True, help="Time is required. Format: HH:MM")
        args = parser.parse_args()

        # Validate and parse date and time
        try:
            appointment_date = datetime.strptime(args['date'], '%Y-%m-%d').date()
            appointment_time = datetime.strptime(args['time'], '%H:%M').time()
        except ValueError:
            return {'message': 'Invalid date or time format.'}, 400

        # Check if the slot is available
        existing = Appointment.query.filter_by(
            date=appointment_date,
            time=appointment_time,
            status='scheduled'
        ).first()

        if existing:
            return {'message': 'Time slot is not available.'}, 400

        # Create new appointment
        new_appointment = Appointment(
            client_name=args['client_name'],
            date=appointment_date,
            time=appointment_time
        )
        db.session.add(new_appointment)
        db.session.commit()

        return {
            'message': 'Appointment scheduled successfully.',
            'appointment_id': new_appointment.id
        }, 201

class AppointmentCancel(Resource):
    """
    Resource for canceling existing appointments.

    Methods:
        post(appointment_id): Handles POST requests to cancel an appointment by its ID.
    """

    def post(self, appointment_id):
        """
        Cancel an existing appointment.

        Validates the appointment ID, checks if the appointment exists and is not
        already canceled, and updates its status to 'canceled'.

        Args:
            appointment_id (int): The unique identifier of the appointment to cancel.

        Returns:
            tuple: A JSON response with a success or error message,
                   and an HTTP status code.
        """
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return {'message': 'Appointment not found.'}, 404
        if appointment.status == 'canceled':
            return {'message': 'Appointment is already canceled.'}, 400

        appointment.status = 'canceled'
        db.session.commit()
        return {'message': 'Appointment canceled successfully.'}, 200

class AppointmentReschedule(Resource):
    """
    Resource for rescheduling existing appointments.

    Methods:
        post(appointment_id): Handles POST requests to reschedule an appointment by its ID.
    """

    def post(self, appointment_id):
        """
        Reschedule an existing appointment to a new date and time.

        Parses the incoming request data for the new date and time.
        Validates the input, checks if the new slot is available, and updates
        the appointment if possible.

        Args:
            appointment_id (int): The unique identifier of the appointment to reschedule.

        Returns:
            tuple: A JSON response with a success or error message,
                   and an HTTP status code.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('date', required=True, help="New date is required. Format: YYYY-MM-DD")
        parser.add_argument('time', required=True, help="New time is required. Format: HH:MM")
        args = parser.parse_args()

        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return {'message': 'Appointment not found.'}, 404
        if appointment.status == 'canceled':
            return {'message': 'Cannot reschedule a canceled appointment.'}, 400

        # Validate and parse new date and time
        try:
            new_date = datetime.strptime(args['date'], '%Y-%m-%d').date()
            new_time = datetime.strptime(args['time'], '%H:%M').time()
        except ValueError:
            return {'message': 'Invalid date or time format.'}, 400

        # Check if the new slot is available
        existing = Appointment.query.filter_by(
            date=new_date,
            time=new_time,
            status='scheduled'
        ).first()

        if existing:
            return {'message': 'New time slot is not available.'}, 400

        # Update appointment
        appointment.date = new_date
        appointment.time = new_time
        db.session.commit()

        return {'message': 'Appointment rescheduled successfully.'}, 200
