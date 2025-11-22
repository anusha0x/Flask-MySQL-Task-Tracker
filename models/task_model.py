from db_config import get_db_connection
from mysql.connector import Error

# Add a new task
def add_task(title, description, due_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO tasks (title, description, due_date) VALUES (%s, %s, %s)"
    cursor.execute(query, (title, description, due_date))
    conn.commit()
    cursor.close()
    conn.close()
    return cursor.lastrowid  # returns the ID of the new task

# Get all tasks
def get_all_tasks(filter_by=None, sort_by=None, sort_order='ASC'):
    """Returns the list of all tasks, with optional filtering and sorting."""
    conn = get_db_connection()
    if not conn:
        return []

    cursor = conn.cursor(dictionary=True)
    
    # Base query
    query = "SELECT * FROM tasks"
    
    # --- 1. Filtering ---
    values = []
    
    if filter_by and filter_by.get('status'):
        # Add WHERE clause to filter by status
        query += " WHERE status = %s"
        values.append(filter_by['status'])

    # --- 2. Sorting ---
    if sort_by:
        # Define valid sorting fields to prevent SQL Injection
        valid_sort_fields = ['id', 'title', 'due_date', 'status', 'created_at']
        
        if sort_by.lower() in valid_sort_fields:
            # Validate sort order
            order = 'DESC' if sort_order.upper() == 'DESC' else 'ASC'
            
            # Add ORDER BY clause
            query += f" ORDER BY {sort_by} {order}"
        else:
            # Optional: Add error logging for invalid sort field
            print(f"Warning: Invalid sort field '{sort_by}' ignored.")

    # Execute the final query
    try:
        cursor.execute(query, tuple(values))
        tasks = cursor.fetchall()
        return tasks
    except Error as e:
        print(f"Error executing get_all_tasks: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# Get a single task by ID
def get_task_by_id(task_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM tasks WHERE id = %s"
    cursor.execute(query, (task_id,))
    task = cursor.fetchone()  # Use fetchone() for a single result
    cursor.close()
    conn.close()
    return task

# Update task status
def update_task_status(task_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE tasks SET status=%s WHERE id=%s"
    cursor.execute(query, (status, task_id))
    conn.commit()
    cursor.close()
    conn.close()
    return cursor.rowcount  # number of rows updated


def update_task_details(task_id, updates):
    """
    Updates specified fields (title, description, due_date, status) of a task.
    'updates' is a dictionary like {'title': 'New Title', 'status': 'Completed'}
    """
    conn = get_db_connection()
    if not conn:
        return 0

    cursor = conn.cursor()
    
    # 1. Build the SET clause dynamically
    set_clauses = []
    values = []
    
    # Map valid keys to their corresponding database fields
    valid_fields = ['title', 'description', 'due_date', 'status']
    
    for key, value in updates.items():
        if key in valid_fields:
            # Add the field name to the SET clause: `field=%s`
            set_clauses.append(f"{key}=%s")
            # Add the value to the list of values to execute
            values.append(value)

    if not set_clauses:
        # No valid fields provided, nothing to update
        cursor.close()
        conn.close()
        return 0

    # 2. Construct the final query
    set_sql = ", ".join(set_clauses)
    query = f"UPDATE tasks SET {set_sql} WHERE id=%s"
    
    # 3. Append the task_id to the values list for the WHERE clause
    values.append(task_id)

    # 4. Execute and Commit
    try:
        cursor.execute(query, tuple(values))
        conn.commit()
        return cursor.rowcount  # Number of rows updated (0 or 1)
    except Error as e:
        print(f"Error executing update_task_details: {e}")
        return 0
    finally:
        cursor.close()
        conn.close()

# Delete a task
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM tasks WHERE id=%s"
    cursor.execute(query, (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return cursor.rowcount  # number of rows deleted
