"""
This module initializes the SQLAlchemy database object without binding it to any specific Flask app instance.
It allows the 'db' object to be imported and used across the application modules without causing circular import issues.
"""

from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object
db = SQLAlchemy()