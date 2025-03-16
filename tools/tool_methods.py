import math
import sqlite3

conn = sqlite3.connect("geographical_data.db")

import sqlite3
import re


def list_tables():
    """
    Lists all tables in a SQLite3 database.
    Parameters:
        no parameters
    Returns:
        list: List of table names in the database
    """
    try:
        # Connect to the database
        cursor = conn.cursor()

        # Query to get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        # Fetch all results
        tables = [table[0] for table in cursor.fetchall()]

        return tables
    except sqlite3.Error as e:
        return f"Error accessing database: {e}"


def list_table_schema(table_name: str):
    """
    Returns the schema for a specific table in a SQLite database.

    Parameters:
        table_name (str): Name of the table to get schema for

    Returns:
        list: List of tuples containing column information (cid, name, type, notnull, default_value, pk)
    """
    try:
        cursor = conn.cursor()

        # Get table schema
        cursor.execute(f"PRAGMA table_info({table_name});")
        schema = cursor.fetchall()
        return schema
    except sqlite3.Error as e:
        print(e)
        return f"Error getting schema: {e}"


def execute_sql(sql_query: str, params=None):
    """
    Executes a SQL query on the specified database.

    Parameters:
        sql_query (str): SQL query to execute
        params (tuple, optional): Parameters for the query

    Returns:
        list: Query results or success message
    """
    try:
        cursor = conn.cursor()

        if params:
            cursor.execute(sql_query, params)
        else:
            cursor.execute(sql_query)

        # Check if query is a SELECT statement
        if sql_query.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            conn.commit()
            return results
        else:
            conn.commit()
            rows_affected = cursor.rowcount
            return f"Query executed successfully. Rows affected: {rows_affected}"
    except sqlite3.Error as e:
        return f"Error executing query: {e}"


def check_sql(sql_query: str):
    """
    Performs basic validation on a SQL query.

    Parameters:
        sql_query (str): SQL query to validate

    Returns:
        dict: Validation results with status and messages
    """
    result = {"valid": True, "messages": []}

    # Check for empty query
    if not sql_query.strip():
        result["valid"] = False
        result["messages"].append("Query is empty")
        return result

    # Check for basic SQL injection patterns
    injection_patterns = [
        r'--',  # SQL comment
        r'/\*.*\*/',  # Multi-line comment
        r';.*?;',  # Multiple statements
        r'UNION\s+ALL\s+SELECT',  # UNION-based injection
        r'OR\s+1\s*=\s*1',  # OR 1=1 injection
        r'DROP\s+TABLE',  # DROP TABLE
        r'DELETE\s+FROM\s+\w+\s+WHERE\s+1\s*=\s*1'  # DELETE FROM table WHERE 1=1
    ]

    for pattern in injection_patterns:
        if re.search(pattern, sql_query, re.IGNORECASE):
            result["valid"] = False
            result["messages"].append(f"Potential SQL injection detected: {pattern}")

    # Check for basic syntax
    query_type = sql_query.strip().split()[0].upper()
    if query_type not in ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP", "PRAGMA"]:
        result["messages"].append("Warning: Unrecognized query type")

    return result


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points using the Haversine formula.
  Parameters:
       lat1: The latitude of the first point in decimal degrees.
       lon1: The longitude of the first point in decimal degrees.
       lat2: The latitude of the second point in decimal degrees.
       lon2: The longitude of the second point in decimal degrees.

   Returns: float: The distance between the two points in kilometers.
   """

    # Haversine formula
    R = 6371  # Radius of the Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
