# Task Manager

A web-based Task Manager application built using Flask, SQLite, and Chart.js, allowing users to manage tasks, view dashboard statistics, and perform CRUD (Create, Read, Update, Delete) operations on tasks. The project includes features such as filtering, dark mode, and chart visualization for task statuses, categories, and priorities.

## Features

- **Task Management**: Create, edit, complete, and delete tasks.
- **Dashboard**: Visualize task statistics using dynamic charts (categories, statuses, priorities).
- **Filtering & Search**: Filter tasks by category, priority, and status; search tasks by name.
- **Dark Mode**: Toggle between light and dark themes for better usability.
- **Responsive Design**: The layout is responsive and adapts to different screen sizes.

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Charts**: Chart.js for visualizing task data
- **Icons**: Font Awesome for UI elements

## Installation

### Prerequisites
- Python 3.x
- Flask (`pip install Flask`)
- SQLite3 (included with Python)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/task-manager.git
   cd task-manager
   ```

2. **Set up Virtual Environment (Optional)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install Flask
   ```

4. **Initialize the SQLite Database**:
   Run the following command to create the necessary database:
   ```bash
   python app.py
   ```

5. **Run the Application**:
   Start the Flask development server:
   ```bash
   flask run
   ```
   The app will be available at `http://127.0.0.1:5000/`.

## Usage

- Navigate to `/index` to manage your tasks (create, edit, and delete).
- Go to `/dashboard` to view the task statistics with dynamic charts.
- Tasks can be filtered by category, priority, and status, or searched by name.

## Folder Structure

```
├── static
│   ├── dashboard.css  # Styles for dashboard page
│   ├── styles.css     # General styles for task management
│   └── script.js      # Client-side logic and task handling
├── templates
│   ├── index.html     # Task management page
│   └── dashboard.html # Dashboard page
├── app.py             # Flask application and routes
├── database.db        # SQLite database (generated automatically)
└── README.md          # Project documentation
```

## API Endpoints

- **`GET /get_tasks`**: Retrieve all tasks from the database.
- **`POST /add_task`**: Add a new task to the database.
- **`POST /update_task/<int:id>`**: Update an existing task.
- **`DELETE /delete_task/<int:id>`**: Delete a task by ID.
- **`POST /complete_task/<int:id>`**: Mark a task as completed.
- **`GET /dashboard_data`**: Fetch data for dashboard charts (task counts by category, status, and priority).

## Future Enhancements

- Implement user authentication for personal task management.
- Add task categories and priorities as dynamic dropdown options.
- Enable export/import tasks as CSV or JSON files.

---

Feel free to modify this `README.md` as per your project's final structure and features!
