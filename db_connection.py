import mysql.connector
from mysql.connector import Error
import streamlit as st
import pandas as pd

# RUBRIC: Centralized Database Connection
# Database configuration - replace with your actual credentials
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '<your_password>',
    'database': '<your_database>'
}

# Use Streamlit's connection management for robustness
@st.cache_resource
def get_connection():
    """Establishes a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None


def execute_query(query, params=None, fetch=None):
    """
    A reusable helper function to execute database queries.
    :param query: SQL query string.
    :param params: A tuple of parameters for prepared statements.
    :param fetch: "one", "all", or None (for INSERT/UPDATE/DELETE).
    :return: Query result or last inserted ID.
    """
    conn = get_connection()
    if conn is None:
        return None
    cursor = conn.cursor(prepared=True if params else False)
    try:
        cursor.execute(query, params)
        if fetch == "one":
            result = cursor.fetchone()
            return result
        elif fetch == "all":
            result = cursor.fetchall()
            # If results are returned, get column names for DataFrame conversion
            if result:
                columns = [i[0] for i in cursor.description]
                return pd.DataFrame(result, columns=columns)
            return pd.DataFrame()
        else:
            conn.commit()
            return cursor.lastrowid # Useful for INSERT operations
    except Error as e:
        st.error(f"Database Query Error: {e}")
        return None
    finally:
        cursor.close()
        # The connection itself is managed by st.cache_resource, so we don't close it here.


def call_procedure(proc_name, args=()):
    """
    A reusable helper function to call stored procedures.
    :param proc_name: Name of the stored procedure.
    :param args: A tuple of arguments for the procedure.
    :return: The result from the procedure.
    """
    conn = get_connection()
    if conn is None:
        return None
    cursor = conn.cursor()
    try:
        # The last argument is for the OUT parameter
        result_args = cursor.callproc(proc_name, args)
        conn.commit()
        return result_args
    except Error as e:
        st.error(f"Error calling procedure '{proc_name}': {e}")
        return None
    finally:
        cursor.close()


def call_function(func_name, args=()):
    """
    A reusable helper function to call database functions.
    :param func_name: Name of the function.
    :param args: A tuple of arguments for the function.
    :return: The return value from the function.
    """
    conn = get_connection()
    if conn is None:
        return None
    
    # Construct the query string with placeholders for prepared statements
    placeholders = ', '.join(['%s'] * len(args)) if args else ''
    query = f"SELECT {func_name}({placeholders})" if placeholders else f"SELECT {func_name}()"
    
    cursor = conn.cursor(prepared=True)
    try:
        cursor.execute(query, args)
        result = cursor.fetchone()
        if result:
            return result[0]
        return None
    except Error as e:
        st.error(f"Error calling function '{func_name}': {e}")
        return None
    finally:
        cursor.close()
