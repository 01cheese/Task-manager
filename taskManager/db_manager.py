import sqlite3

class DBManager:
    def __init__(self, db_name='database.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT,
            progress INTEGER
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_task(self, title, description, status, progress):
        query = "INSERT INTO tasks (title, description, status, progress) VALUES (?, ?, ?, ?)"
        self.conn.execute(query, (title, description, status, progress))
        self.conn.commit()

    def get_tasks(self, status=None):
        query = "SELECT * FROM tasks WHERE status = ?" if status else "SELECT * FROM tasks"
        cursor = self.conn.execute(query, (status,) if status else ())
        return cursor.fetchall()

    def update_task(self, task_id, title, description, status, progress):
        query = "UPDATE tasks SET title = ?, description = ?, status = ?, progress = ? WHERE id = ?"
        self.conn.execute(query, (title, description, status, progress, task_id))
        self.conn.commit()

    def delete_task(self, task_id):
        query = "DELETE FROM tasks WHERE id = ?"
        self.conn.execute(query, (task_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
