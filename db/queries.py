CREATE_TABLE_TASKS = """
    CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    completed INTEGER DEFAULT 0
    )
"""

SELECT_TASKS = "SELECT id, task, completed FROM tasks"
INSERT_TASK = "INSERT INTO tasks (task) VALUES (?)"
UPDATE_TASK = 'UPDATE tasks SET task = ? WHERE id = ?'
DELETE_TASK = "DELETE FROM tasks WHERE id = ?"

SELECT_completed = "SELECT id, task FROM tasks WHERE completed = 1"
SELECT_uncompleted = "SELECT id, task FROM tasks WHERE completed = 0"