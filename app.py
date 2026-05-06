from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model (table)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)

# Create database
with app.app_context():
    db.create_all()

# GET all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    result = []
    for t in tasks:
        result.append({"id": t.id, "task": t.task})
    return jsonify(result)

# POST add task
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    new_task = Task(task=data['task'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added"})

# PUT update task
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({"message": "Task not found"})
    
    data = request.json
    task.task = data.get('task', task.task)
    db.session.commit()
    return jsonify({"message": "Task updated"})

# DELETE task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({"message": "Task not found"})
    
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})

if __name__ == '__main__':
    app.run(debug=True)