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
@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/dashboard_data', methods=['GET'])
def dashboard_data():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Получить данные по категориям задач
    cursor.execute("SELECT category, COUNT(*) FROM tasks GROUP BY category")
    category_data = cursor.fetchall()

    # Получить данные по статусам задач
    cursor.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
    status_data = cursor.fetchall()

    # Получить данные по приоритетам задач
    cursor.execute("SELECT priority, COUNT(*) FROM tasks GROUP BY priority")
    priority_data = cursor.fetchall()

    conn.close()

    # Формируем ответ в виде JSON
    return jsonify({
        'categories': category_data,
        'statuses': status_data,
        'priorities': priority_data
    })


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


# API to update an existing task
@app.route('/update_task/<int:id>', methods=['POST'])
def update_task(id):
    try:
        task_name = request.form['task_name']
        category = request.form['category']
        priority = request.form['priority']
        status = request.form['status']
        due_date = request.form['due_date']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tasks
            SET task_name = ?, category = ?, priority = ?, status = ?, due_date = ?
            WHERE id = ?
        """, (task_name, category, priority, status, due_date, id))
        conn.commit()
        conn.close()

        return jsonify({'status': 'Task updated successfully'}), 200
    except Exception as e:
        return jsonify({'status': 'Error', 'message': str(e)}), 500


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
