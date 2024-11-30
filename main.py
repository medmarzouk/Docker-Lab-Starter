from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os 

app = Flask(__name__)

# Database configuration
DB_HOST = os.getenv('DB_HOST', 'db')
DB_USER= os.getenv('DB_USER' , 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'example')
DB_NAME = os.getenv('DB_NAME' , 'tasks_db')


# Helper function to get database connection
def get_db_connection():
    return mysql.connector.connect(
        host = DB_HOST,
        user = DB_USER,
        password = DB_PASSWORD,
        database=DB_NAME
    )

@app.route('/')
def index():
    """Display all tasks from the database."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, task FROM tasks")
    tasks = cursor.fetchall()  # Fetch all tasks from the database
    connection.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    """Add a new task to the database."""
    task = request.form.get('task')
    if task:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tasks (task) VALUES (%s)", (task,))
        connection.commit()
        connection.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
