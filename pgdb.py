import psycopg2
import os
import pandas as pd

# Environment Variables for your local Postgres
postgres_user = os.environ.get('POSTGRES_USER')
postgres_password = os.environ.get('POSTGRES_PASSWORD')
postgres_host = os.environ.get('POSTGRES_HOST')
postgres_port = os.environ.get('POSTGRES_PORT')


def create_table():
    connection = psycopg2.connect(
    host=postgres_host,
    port=postgres_port,
    database="postgres",
    user=postgres_user,
    password=postgres_password
    )

    cursor = connection.cursor()

    # Create a new table
    create_query = "CREATE TABLE IF NOT EXISTS chat_log (message_id SERIAL PRIMARY KEY, created_at TIME DEFAULT CURRENT_TIME(2), created_on DATE DEFAULT CURRENT_DATE, name VARCHAR(50), message VARCHAR(255))"
    cursor.execute(create_query)

    # Commit the transaction and close cursor and connection
    connection.commit()
    cursor.close()
    connection.close()

    print("chat_log table created")

def insert_message(chat_name, message_string):
    connection = psycopg2.connect(
    host=postgres_host,
    port=postgres_port,
    database="postgres",
    user=postgres_user,
    password=postgres_password
    )

    cursor = connection.cursor()
    insert_query = "INSERT INTO chat_log (name, message) VALUES (%s, %s)"
    data_to_insert = (chat_name, message_string)

    cursor.execute(insert_query, data_to_insert)

    # Commit the transaction and close cursor and connection
    connection.commit()
    cursor.close()
    connection.close()

def create_dataframe(table_name):
    connection = psycopg2.connect(
    host=postgres_host,
    port=postgres_port,
    database="postgres",
    user=postgres_user,
    password=postgres_password
    )

    cursor = connection.cursor()

    # Execute an SQL query to fetch data from the database
    query = f'''SELECT * FROM {table_name}'''
    cursor.execute(query)

    # Fetch all the rows from the result set
    rows = cursor.fetchall()

    # Get the column names from the cursor description
    column_names = [desc[0] for desc in cursor.description]

    # Create a Pandas DataFrame from the fetched data and column names
    df = pd.DataFrame(rows, columns=column_names)

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return df


def create_convo_log():
    connection = psycopg2.connect(
    host=postgres_host,
    port=postgres_port,
    database="postgres",
    user=postgres_user,
    password=postgres_password
    )

    cursor = connection.cursor()
    query = "SELECT CONCAT(name, ': ', message) FROM chat_log"
    cursor.execute(query)

    # Fetch all the rows from the result set
    rows = cursor.fetchall()
    message_list = [row[0] for row in rows]
    s = '\n'.join(message_list)

    return s