import sqlite3
import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS


def dic_fac(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def init_sql_db():
    conn = sqlite3.connect('blogs.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS blog_info (id INTEGER PRIMARY KEY AUTOINCREMENT, Title TEXT, '
                 'Content TEXT, Author TEXT, Date TEXT, image TEXT)')
    print("Table created successfully ")
    conn.close()


init_sql_db()
app = Flask(__name__)
CORS(app)


@app.route('/')
def load_post_form():
    return render_template('add-blog.html')


@app.route('/add-new/', methods=['POST'])
def add_new_post():
    if request.method == "POST":
        msg = None
        try:
            title = request.form['title']
            content = request.form['content']
            author = request.form['author']
            image = request.form['image']

            with sqlite3.connect('blogs.db') as connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO blog_info (Title, Content, Author, Date, image) VALUES (?, ?, ?, ?, ?)",
                               (title, content, author, datetime.datetime.now(), image))
                connection.commit()
                msg = "Post added.."
        except Exception as e:
            msg = "Something happened: " + str(e)
        finally:
            connection.close()
            return msg


@app.route('/get-all-posts/', methods=['GET'])
def get_all_posts():
    if request.method == 'GET':
        try:
            with sqlite3.connect('blogs.db') as connection:
                connection.row_factory = dic_fac
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM blog_info")

                data = cursor.fetchall()
        except Exception as e:
            print("Something happened: " + str(e))
        finally:
            connection.close()
            return jsonify(data)


@app.route('/get-single-post/<int:data_id>/', methods=['GET'])
def show_single_post(data_id):
    data = []
    try:
        with sqlite3.connect('blogs.db') as con:
            con.row_factory = dic_fac
            cur = con.cursor()
            cur.execute('SELECT * FROM blog_info WHERE id=' + str(data_id))
            data = cur.fetchone()
    except Exception as e:
        con.rollback()
        print("Error fetching data from the database" + str(e))
    finally:
        con.close()
        return jsonify(data)
