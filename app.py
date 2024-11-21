from flask import Flask, request, jsonify
from models import db, TodoItem
import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}"
db.init_app(app)

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = TodoItem.query.all()
    return jsonify([{'id': t.id, 'task': t.task, 'completed': t.completed} for t in todos])

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    new_task = TodoItem(task=data['task'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task added!'}), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    task = TodoItem.query.get(todo_id)
    if not task:
        return jsonify({'message': 'Task not found!'}), 404
    task.task = data.get('task', task.task)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify({'message': 'Task updated!'})

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    task = TodoItem.query.get(todo_id)
    if not task:
        return jsonify({'message': 'Task not found!'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
