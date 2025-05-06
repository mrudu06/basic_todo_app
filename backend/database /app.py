from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        user="mrudu",
        password="xp",
        database="contacts"
    )
    return conn

@app.route('/all_tasks')
def all_contacts():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks')
    contacts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('tasks.html', contacts=contacts)

@app.route('/modify_tasks', methods=['GET', 'POST'])
def modify_contacts():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()

    cur.close()
    conn.close()