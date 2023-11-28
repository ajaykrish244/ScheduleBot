import os
import csv
from pathlib import Path
from src.Event import Event
from datetime import datetime
from cryptography.fernet import Fernet
from dotenv import load_dotenv

import mysql.connector

load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

def connect_to_database():
    """
    Function: connect_to_database
    Description: Connects to the event_types database
    Input: None
    Output: Returns a connection to the event_types database
    """

    conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME)

    return conn

def read_type_file(user_id):
    """
    Function: read_event_types
    Description: Reads event types from the MySQL database for a specific user
    Input:
        user_id - String representing the Discord ID of the user
    Output:
        event_types - List of event types (rows)
    """
    event_types = []

    try:
        # Establish a connection to the MySQL database
        db_connection = connect_to_database()
        # Create a cursor object to execute SQL commands
        cursor = db_connection.cursor()

        # Define the SQL query to select event types for the user
        select_query = "SELECT event_type, start_time, end_time FROM event_types WHERE user_id = %s"

        # Execute the SQL query
        cursor.execute(select_query, (user_id,))

        # Fetch all the rows from the result set
        rows = cursor.fetchall()

        # Process the rows and convert them into a list of event types
        for row in rows:
            event_type, start_time, end_time = row
            event_types.append([event_type, start_time, end_time])

    except mysql.connector.Error as error:
        print(f"Error: {error}")
    finally:
        # Close the cursor and database connection
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()

    return event_types


def turn_types_to_string(user_id):
    """
    Function: turn_types_to_string
    Description: Retrieves event types from the MySQL database and turns them into a formatted string
    Input:
        user_id - String representing the Discord ID of the user
    Output:
        output - Formatted string of retrieved event types
    """
    output = ""
    space = [12, 5, 5]
    event_types = read_type_file(user_id)
    line_number = 0
    for event_type, start_time, end_time in event_types:
        # print("________________________")
        start_time_f = start_time.strftime("%I:%M %p")
        end_time_f= end_time.strftime("%I:%M %p")
        # print(start_time_f, end_time_f)
        # print(type(start_time), type(end_time))
        output += f"{event_type:<{space[0]}} Preferred range of {start_time_f:<{space[1]}} - {end_time_f:<{space[2]}}\n"
        line_number += 1
    return output


def get_existing_types(user_id):
    """
    Function: retrieve_existing_types
    Description: Retrieves existing event types for a specific user from the MySQL database
    Input:
        user_id - String representing the Discord ID of the user
    Output:
        types_list - List of existing event types for the user
    """
    types_list = []
    try:
        # Establish a connection to the MySQL database
        db_connection = connect_to_database()

        # Create a cursor object to execute SQL commands
        cursor = db_connection.cursor()

        # Define the SQL query to retrieve existing event types for the user
        select_query = "SELECT DISTINCT event_type FROM event_types WHERE user_id = %s"

        # Execute the SQL query with the provided parameter
        cursor.execute(select_query, (user_id,))

        # Fetch all rows
        rows = cursor.fetchall()

        for row in rows:
            event_type = row[0]
            types_list.append(event_type)

    except mysql.connector.Error as error:
        print(f"Error: {error}")
    finally:
        # Close the cursor and database connection
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()

    return types_list


def read_event_file(user_id):
    """
    Function: read_event_file
    Description: Reads the calendar file and creates a list of rows
    Input:
        user_id - String representing the Discord ID of the user
    Output:
        rows - List of rows
    """

    db_connection = connect_to_database()

    rows = []
    cursor = db_connection.cursor()

    query = """SELECT id, name, start_date, end_date, priority, type, notes, location
            FROM EVENT WHERE user_id='{user_id}'""".format(user_id=user_id)
    cursor.execute(query)

    rows.append(["ID", "Name", "Start Date", "End Date", "Priority", "Type", "Notes", "Location"])

    for r in cursor:
        rows.append(list(r))

    cursor.close()
    return rows

def add_event_to_file(user_id, current):
    """
    Function: add_event_to_file
    Description: Adds an event to the calendar file in chronological order
    Input:
        user_id - String representing the Discord ID of the user
        current - Event to be added to calendar
    Output: None
    """

    db_connection = connect_to_database()

    cursor = db_connection.cursor()
    query = """ INSERT INTO EVENT (name, start_date, end_date, priority, type, notes, location, user_id)
                VALUES('{name}', '{start_date}', '{end_date}', {priority}, '{type}', '{notes}', '{location}', '{user_id}')
            """.format(name=current.name, start_date=current.start_date, end_date=current.end_date,
                       priority=current.priority, type=current.event_type, notes=current.description, location=current.location,
                       user_id=user_id)

    print(query)

    cursor.execute(query)
    db_connection.commit()
    cursor.close()


def delete_event_from_file(user_id, to_remove):
    db_connection = connect_to_database()
    cursor = db_connection.cursor()
    query = """ DELETE FROM EVENT WHERE name='{name}' and user_id={user_id}
            """.format(name=to_remove["name"], user_id=user_id)
    cursor.execute(query)
    db_connection.commit()
    cursor.close()


def create_key_directory():
    """
    Function: create_event_directory
    Description: Creates ScheduleBot event directory in users Documents folder if it doesn't exist
    Input: None
    Output: Creates Event folder if it doesn't exist
    """
    if not os.path.exists(os.path.expanduser("~/Documents/ScheduleBot/Key")):
        Path(os.path.expanduser("~/Documents/ScheduleBot/Key")).mkdir(parents=True, exist_ok=True)



def check_key(user_id):
    """
    Function: check_key
    Description: Creates ScheduleBot event key in users Documents folder if it doesn't exist
    Input: user_id String representing the Discord ID of the user
    Output: the key for the given user
    """
    create_key_directory()
    if not os.path.exists(os.path.expanduser("~/Documents") + "/ScheduleBot/Key/" + user_id + ".key"):
        key = write_key(user_id)
    else:
        key = load_key(user_id)

    return key


def write_key(user_id):
    """
    Function: write_key
    Description: Generate the key for the user
    Input:
        user_id - String representing the Discord ID of the user
    Output: the writen key
    """
    #Generates a key and save it into a file
    key = Fernet.generate_key()
    with open(os.path.expanduser("~/Documents") + "/ScheduleBot/Key/" + user_id + ".key", "wb") as key_file:
        key_file.write(key)
    return key


def load_key(user_id):
    """
    Function: load_key
    Description: read the key for the user
    Input:
        userid - String representing the Discord ID of the user
    Output: the loaded key
    """
    with open(os.path.expanduser("~/Documents") + "/ScheduleBot/Key/" + user_id + ".key","rb") as filekey:
        key = filekey.read()

    return key


def encrypt_file(key, filepath):
    """
    Function: encrypt_file
    Description: encrypt the given file with the given key
    Input:
        key - key to encrypt
        filepath - filepath to encrypt
    Output: None
    """
    # using the generated key
    fernet = Fernet(key)
    # opening the original file to encrypt
    with open(filepath, 'rb') as file:
        original = file.read()

    # encrypting the file
    encrypted = fernet.encrypt(original)

    # opening the file in write mode and
    # writing the encrypted data
    with open(filepath, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

def decrypt_file(key, filepath):
    """
    Function: decrypt_file
    Description: decrypt the given file with the given key
    Input:
        key - key to decrypt
        filepath - filepath to decrypt
    Output: None
    """
    # using the key
    fernet = Fernet(key)

    # opening the encrypted file
    with open(filepath, 'rb') as enc_file:
        encrypted = enc_file.read()

    # decrypting the file
    decrypted = fernet.decrypt(encrypted)

    # opening the file in write mode and
    # writing the decrypted data
    with open(filepath, 'wb') as dec_file:
        dec_file.write(decrypted)
