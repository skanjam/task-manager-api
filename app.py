from flask import Flask, jsonify, request

app= Flask(__name__)

tasks = [
    {"id": 1, "task" : "learn python"},
    {"id": 2, "task" : "build API"}
]

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    tasks.append(data)
    return jsonify({"message": "Task added successfully"})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return jsonify({"message": "Task deleted"})
    
    return jsonify({"message": "Task not found"})

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.json
    
    for task in tasks:
        if task["id"] == id:
            task["task"] = data.get("task", task["task"])
            return jsonify({"message": "Task updated"})
    
    return jsonify({"message": "Task not found"})

if __name__ == '__main__':
    app.run(debug=True)