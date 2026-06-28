import os
from flask import Flask, request, jsonify
from datetime import datetime
from models import db, Task
from config import config

def create_app(config_name=None):
    """Application factory function"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))
    
    db.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Error handler for 404
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    # Error handler for 500
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy'}), 200
    
    # GET all tasks
    @app.route('/api/tasks', methods=['GET'])
    def get_tasks():
        """Get all tasks with optional filtering"""
        status = request.args.get('status')
        priority = request.args.get('priority')
        
        query = Task.query
        
        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=priority)
        
        tasks = query.order_by(Task.created_at.desc()).all()
        return jsonify([task.to_dict() for task in tasks]), 200
    
    # GET single task
    @app.route('/api/tasks/<int:task_id>', methods=['GET'])
    def get_task(task_id):
        """Get a single task by ID"""
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify(task.to_dict()), 200
    
    # POST create new task
    @app.route('/api/tasks', methods=['POST'])
    def create_task():
        """Create a new task"""
        data = request.get_json()
        
        # Validation
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400
        
        # Validate status
        valid_statuses = ['pending', 'in_progress', 'completed']
        status = data.get('status', 'pending')
        if status not in valid_statuses:
            return jsonify({'error': f'Status must be one of {valid_statuses}'}), 400
        
        # Validate priority
        valid_priorities = ['low', 'medium', 'high']
        priority = data.get('priority', 'medium')
        if priority not in valid_priorities:
            return jsonify({'error': f'Priority must be one of {valid_priorities}'}), 400
        
        try:
            # Parse due_date if provided
            due_date = None
            if data.get('due_date'):
                due_date = datetime.fromisoformat(data.get('due_date'))
            
            task = Task(
                title=data.get('title'),
                description=data.get('description'),
                status=status,
                priority=priority,
                due_date=due_date
            )
            
            db.session.add(task)
            db.session.commit()
            
            return jsonify(task.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    
    # PUT update task
    @app.route('/api/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        """Update an existing task"""
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        try:
            # Update fields if provided
            if 'title' in data:
                task.title = data.get('title')
            
            if 'description' in data:
                task.description = data.get('description')
            
            if 'status' in data:
                valid_statuses = ['pending', 'in_progress', 'completed']
                if data.get('status') not in valid_statuses:
                    return jsonify({'error': f'Status must be one of {valid_statuses}'}), 400
                task.status = data.get('status')
            
            if 'priority' in data:
                valid_priorities = ['low', 'medium', 'high']
                if data.get('priority') not in valid_priorities:
                    return jsonify({'error': f'Priority must be one of {valid_priorities}'}), 400
                task.priority = data.get('priority')
            
            if 'due_date' in data:
                if data.get('due_date'):
                    task.due_date = datetime.fromisoformat(data.get('due_date'))
                else:
                    task.due_date = None
            
            task.updated_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify(task.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    
    # DELETE task
    @app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        """Delete a task"""
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        try:
            db.session.delete(task)
            db.session.commit()
            return jsonify({'message': 'Task deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    
    # DELETE all tasks
    @app.route('/api/tasks', methods=['DELETE'])
    def delete_all_tasks():
        """Delete all tasks"""
        try:
            Task.query.delete()
            db.session.commit()
            return jsonify({'message': 'All tasks deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
