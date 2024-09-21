"""
This module defines the resources for scheduling, canceling, rescheduling, and retrieving appointment details.
Each resource corresponds to an API endpoint and handles the necessary logic for appointment management.
"""

import re
from flask_restful import Resource, reqparse
from models import Appointment
from datetime import datetime
from database import db  # Import db from database.py
from flask import request

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
        parser.add_argument('notes', required=False, type=str)
        args = parser.parse_args()

        # Validate the presence of JSON body
        if not request.is_json:
            return {'error': 'Request body must contain JSON.'}, 400

        # Input Length Constraints
        MAX_NAME_LENGTH = 100
        MAX_NOTES_LENGTH = 1000  # Adjust as needed

        if len(args['client_name']) > MAX_NAME_LENGTH:
            return {'error': f"Client name must be at most {MAX_NAME_LENGTH} characters long."}, 400

        # Whitelist Validation: Allow letters, spaces, hyphens, apostrophes, and periods
        if not re.fullmatch(r"[A-Za-z\s\-'.]{1,100}", args['client_name']):
            return {'error': 'Client name contains invalid characters.'}, 400

        if args.get('notes') and len(args['notes']) > MAX_NOTES_LENGTH:
            return {'error': f"Notes must be at most {MAX_NOTES_LENGTH} characters long."}, 400

        # Validate and parse date and time
        try:
            appointment_date = datetime.strptime(args['date'], '%Y-%m-%d').date()
            appointment_time = datetime.strptime(args['time'], '%H:%M').time()
        except ValueError:
            return {'error': 'Invalid date or time format. Use YYYY-MM-DD for date and HH:MM in 24-hour format for time.'}, 400

        # Check if the appointment date and time are in the future
        current_datetime = datetime.now()
        appointment_datetime = datetime.combine(appointment_date, appointment_time)
        if appointment_datetime <= current_datetime:
            return {'error': 'Appointment date and time must be in the future.'}, 400

        # Check if the slot is available
        existing = Appointment.query.filter_by(
            date=appointment_date,
            time=appointment_time,
            status='scheduled'
        ).first()

        if existing:
            return {'error': 'Time slot is not available.'}, 409  # 409 Conflict

        # Create new appointment
        new_appointment = Appointment(
            client_name=args['client_name'],
            date=appointment_date,
            time=appointment_time,
            notes=args.get('notes')
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
        # Validate appointment_id type
        if not isinstance(appointment_id, int):
            return {'error': 'Invalid appointment ID.'}, 400

        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return {'error': 'Appointment not found.'}, 404
        if appointment.status == 'canceled':
            return {'error': 'Appointment is already canceled.'}, 400

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
        # Validate appointment_id type
        if not isinstance(appointment_id, int):
            return {'error': 'Invalid appointment ID.'}, 400

        parser = reqparse.RequestParser()
        parser.add_argument('date', required=True, help="New date is required. Format: YYYY-MM-DD")
        parser.add_argument('time', required=True, help="New time is required. Format: HH:MM")
        parser.add_argument('notes', required=False, type=str)
        args = parser.parse_args()

        # Validate the presence of JSON body
        if not request.is_json:
            return {'error': 'Request body must contain JSON.'}, 400

        # Input Length Constraints
        MAX_NOTES_LENGTH = 1000  # Adjust as needed

        if args.get('notes') and len(args['notes']) > MAX_NOTES_LENGTH:
            return {'error': f"Notes must be at most {MAX_NOTES_LENGTH} characters long."}, 400

        # Validate and parse new date and time
        try:
            new_date = datetime.strptime(args['date'], '%Y-%m-%d').date()
            new_time = datetime.strptime(args['time'], '%H:%M').time()
        except ValueError:
            return {'error': 'Invalid date or time format. Use YYYY-MM-DD for date and HH:MM in 24-hour format for time.'}, 400

        # Check if the new appointment date and time are in the future
        current_datetime = datetime.now()
        new_appointment_datetime = datetime.combine(new_date, new_time)
        if new_appointment_datetime <= current_datetime:
            return {'error': 'New appointment date and time must be in the future.'}, 400

        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return {'error': 'Appointment not found.'}, 404
        if appointment.status == 'canceled':
            return {'error': 'Cannot reschedule a canceled appointment.'}, 400

        # Check if the new slot is available
        existing = Appointment.query.filter_by(
            date=new_date,
            time=new_time,
            status='scheduled'
        ).first()

        if existing:
            return {'error': 'New time slot is not available.'}, 409  # 409 Conflict

        # Update appointment
        appointment.date = new_date
        appointment.time = new_time
        if args.get('notes'):
            appointment.notes = args.get('notes')
        db.session.commit()

        return {'message': 'Appointment rescheduled successfully.'}, 200

class AppointmentDetail(Resource):
    """
    Resource for retrieving details of a specific appointment.
    """

    def get(self, appointment_id):
        """
        Retrieve details of an appointment by its ID.

        Args:
            appointment_id (int): The unique identifier of the appointment.

        Returns:
            tuple: A JSON response with appointment details and an HTTP status code.
        """
        # Validate appointment_id type
        if not isinstance(appointment_id, int):
            return {'error': 'Invalid appointment ID.'}, 400

        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return {'error': 'Appointment not found.'}, 404

        # Assuming 'notes' is an optional field in the model
        response = {
            'id': appointment.id,
            'client_name': appointment.client_name,
            'date': appointment.date.strftime('%Y-%m-%d'),
            'time': appointment.time.strftime('%H:%M'),
            'status': appointment.status
        }

        # Include 'notes' if it exists
        if hasattr(appointment, 'notes') and appointment.notes:
            response['notes'] = appointment.notes

        return response, 200
