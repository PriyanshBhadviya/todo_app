from flask import Blueprint, request, jsonify
from models import db, Task
from schemas import TaskSchema
from datetime import datetime
from sqlalchemy import func

task_bp = Blueprint('task_bp', __name__)
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

def standardize_priority(priority):
    priority = priority.lower()
    if priority == 'high':
        return 'High'
    elif priority == 'medium':
        return 'Medium'
    elif priority == 'low':
        return 'Low'
    else:
        raise ValueError("Invalid priority value")

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    errors = task_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    priority = standardize_priority(data['priority'])  # Standardize priority value

    new_task = Task(
        title=data['title'],
        description=data.get('description'),
        due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
        priority=priority  # Assign standardized priority value to the task
    )
    db.session.add(new_task)
    db.session.commit()
    return task_schema.jsonify(new_task), 201

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return tasks_schema.jsonify(tasks), 200

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.due_date = datetime.fromisoformat(data['due_date']) if data.get('due_date') else task.due_date
    task.priority = standardize_priority(data.get('priority', task.priority))  # Standardize priority value
    db.session.commit()
    return task_schema.jsonify(task), 200

@task_bp.route('/tasks/<int:task_id>', methods=['PATCH'])
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.status = data.get('status', task.status)
    db.session.commit()
    return task_schema.jsonify(task), 200

@task_bp.route('/tasks/filter', methods=['GET'])
def filter_tasks():
    due_date = request.args.get('due_date')
    priority = request.args.get('priority')
    tasks_query = Task.query
    if due_date:
        tasks_query = tasks_query.filter(Task.due_date <= datetime.fromisoformat(due_date))
    if priority:
        tasks_query = tasks_query.filter_by(priority=priority)
    tasks = tasks_query.all()
    return tasks_schema.jsonify(tasks), 200

@task_bp.route('/tasks/sort', methods=['GET'])
def sort_tasks():
    sort_by = request.args.get('sort_by')

    if sort_by == 'due_date':
        tasks = Task.query.order_by(Task.due_date).all()
    elif sort_by == 'priority':
        tasks = Task.query.order_by(Task.priority).all()
    else:
        tasks = Task.query.all()

    return tasks_schema.jsonify(tasks), 200
