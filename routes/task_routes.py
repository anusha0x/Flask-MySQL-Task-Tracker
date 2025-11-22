from flask import Blueprint, request, jsonify
from models.task_model import add_task, get_all_tasks, update_task_status, delete_task, get_task_by_id, update_task_details

# Create a Blueprint for task routes
task_bp = Blueprint('task_bp', __name__)

# Add new task
@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    task_id = add_task(title, description, due_date)
    return jsonify({'message': 'Task added successfully', 'task_id': task_id}), 201


# Get all tasks
@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    # Get parameters from the request query string
    status_filter = request.args.get('status')
    sort_by = request.args.get('sort_by')
    sort_order = request.args.get('sort_order', 'ASC') # Default to ASC
    
    filter_params = {}
    if status_filter:
        # Basic validation for the status filter
        if status_filter.lower() in ['pending', 'completed']:
            filter_params['status'] = status_filter
        else:
            return jsonify({'error': 'Invalid status filter value. Use "Pending" or "Completed"'}), 400

    # Call the model function with the extracted parameters
    tasks = get_all_tasks(
        filter_by=filter_params, 
        sort_by=sort_by, 
        sort_order=sort_order
    )
    
    return jsonify(tasks), 200


# Get a single task
@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    # This calls the database function we planned for task_model.py
    task = get_task_by_id(task_id) 
    
    if task:
        return jsonify(task), 200
    else:
        # If the function returns None, the task doesn't exist
        return jsonify({'error': 'Task not found'}), 404


# Update task status
@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_status(task_id):
    data = request.get_json()
    status = data.get('status')

    if status not in ['Pending', 'Completed']:
        return jsonify({'error': 'Invalid status'}), 400

    updated = update_task_status(task_id, status)
    if updated:
        return jsonify({'message': 'Task updated successfully'}), 200
    else:
        return jsonify({'error': 'Task not found'}), 404


# Update specific fields of a task
@task_bp.route('/tasks/<int:task_id>', methods=['PATCH'])
def patch_task(task_id):
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No update data provided'}), 400

    # The function handles building the query based on the 'data' dictionary
    updated_rows = update_task_details(task_id, data)
    
    if updated_rows > 0:
        return jsonify({'message': 'Task updated successfully'}), 200
    else:
        # Check if task exists first (optional, but good practice)
        # For simplicity, we just return 404 if no rows were updated
        return jsonify({'error': 'Task not found or no changes were made'}), 404
    

# Delete a task
@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def remove_task(task_id):
    deleted = delete_task(task_id)
    if deleted:
        return jsonify({'message': 'Task deleted successfully'}), 200
    else:
        return jsonify({'error': 'Task not found'}), 404
