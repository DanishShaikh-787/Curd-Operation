"""
   * Author - danish
   * Date - 23/11/20
   * Time - 10:11 PM
   * Title - CurdOperation for flask
"""
from flask import Flask, request, render_template, redirect, url_for
import os

from flask_mysqldb import MySQL
# from flask_mysql_connector import MySQL
from jinja2 import UndefinedError

app = Flask(__name__, template_folder="Templates")

app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= os.environ['user']
app.config['MYSQL_PASSWORD']= os.environ['password']
app.config['MYSQL_DB']= 'danishDB'

mysql = MySQL(app)

@app.route('/create', methods=['GET', 'POST'])
def insert():
    """ Method Discription
    Insert the Data In Table
    :return: Inserted Data
    """
    if request.method == "POST":
        name = request.form['name']
        address = request.form['address']

        cur = mysql.connection.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS students (id INT AUTO_INCREMENT PRIMARY KEY, \
                    name VARCHAR(20), address VARCHAR(50))")
        table = "INSERT INTO students (name, address) VALUES (%s, %s)"
        val = (name, address)
        cur.execute(table, val)
        mysql.connection.commit()
        cur.close()
        return "Data inserted successfully"
    return render_template("Insert.html")
    return render_template(url_for("show"))

@app.route('/show')
def show():
    """ Method Discription
    Display The table
    :return: Render the display data
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close()
    return render_template("Display.html", data=data)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    """ Mrthod Discription
    Update through ID
    :param id: Id of Student
    :return:
    """
    if request.method == "POST":
        if request.form['update']:
            name = request.form['name']
            address = request.form['address']

            cur = mysql.connection.cursor()
            cur.execute("""UPDATE students SET name=%s, address=%s WHERE id=%s""", (name, address, id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for("show"))

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students WHERE id=%s", (id,))
        data = cur.fetchall()
        cur.close()
        return render_template("Upload.html", data=data)
    except UndefinedError:
        return "id " + str(id) + " not exist"

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    """Method Definition
       Delete Records
       :return Render Template
    """
    try:
        if request.method == "POST":
            id = int(request.form['id'])
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM students WHERE id = %s"
            val = (id,)
            a=cursor.execute(sql, val)
            mysql.connection.commit()
            cursor.close()
            if a == 1:
                return "Student data Deleted Successfully"
            else:
                return "Student data Not Deleted"
        return render_template("Delete.html")
    except request.exceptions.RequestException as e:
        mysql.connection.rollback()
        return ""


if __name__ == "__main__":
    app.run(debug=True)
