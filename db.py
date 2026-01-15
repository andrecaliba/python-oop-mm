"""
Database Connection Module

This module establishes and manages the MySQL database connection for the task management application.
"""

import mysql.connector
from decouple import config

# Establish connection to MySQL database using credentials from environment variables
db = mysql.connector.connect(
    host=config("DB_HOST"),        # Database host address
    user=config("DB_USER"),        # Database user credentials
    password=config("DB_PASSWORD"), # Database password
    database=config("DB_DATABASE")  # Target database name
)

# Create a cursor object for executing SQL queries
cursor = db.cursor()