from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        user="mrudu",
        password="xp",
        database="basic_todo"
    )
    return conn

@app.route('/all_tasks')
def all_contacts():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('tasks.html', tasks=tasks)

@app.route('/modify_tasks', methods=['GET', 'POST'])
def modify_contacts():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()

    cur.close()
    conn.close()

    if request.method == 'POST':
        task_id = request.form['task_id']
        task_name = request.form['task_name']
        task_description = request.form['task_description']
        task_status = request.form['task_status']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE tasks SET name = %s, description = %s, status = %s WHERE id = %s',
                    (task_name, task_description, task_status, task_id))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('all_contacts'))
    return render_template('modify_tasks.html', tasks=tasks)

@app.route('/delete_tasks', methods=['GET', 'POST'])
def delete_contacts():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()

    cur.close()
    conn.close()

    if request.method == 'POST':
        task_id = request.form['task_id']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('all_contacts'))
    return render_template('delete_tasks.html', tasks=tasks)

@app.route('/add_tasks', methods=['GET', 'POST'])
def add_contacts():
    if request.method == 'POST':
        task_name = request.form['task_name']
        task_description = request.form['task_description']
        task_status = request.form['task_status']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO tasks (name, description, status) VALUES (%s, %s, %s)',
                    (task_name, task_description, task_status))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('all_contacts'))
    return render_template('add_tasks.html')

if __name__ == '__main__':
    app.run(debug=True)
    