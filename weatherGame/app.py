from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)


# Database setup
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    conn.execute(
        'CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task_name TEXT, category TEXT, priority TEXT, status TEXT, due_date TEXT)')
    conn.close()


init_sqlite_db()


# Route to display the task manager
@app.route('/')
def home():
    return render_template('index.html')


# API to fetch tasks
@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return jsonify(tasks)


# API to add a new task
@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        task_name = request.form['task_name']
        category = request.form['category']
        priority = request.form['priority']
        status = 'pending'
        due_date = request.form['due_date']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task_name, category, priority, status, due_date) VALUES (?, ?, ?, ?, ?)",
                       (task_name, category, priority, status, due_date))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))


# API to delete a task
@app.route('/delete_task/<int:id>', methods=['DELETE'])
def delete_task(id):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?", (id,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'Task deleted'})
    except Exception as e:
        return jsonify({'status': 'Error', 'message': str(e)})



# API to update a task status to completed
@app.route('/complete_task/<int:id>', methods=['POST'])
def complete_task(id):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'Task completed'}), 200
    except Exception as e:
        return jsonify({'status': 'Error', 'message': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
