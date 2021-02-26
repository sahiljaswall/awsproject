from flask import Flask, render_template, request
from pymysql import connections
import boto3
import os
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)

Output = {}
table = 'foodstorage'


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("addRestaurant.html")


@app.route('/returnRest', methods=['POST'])
def returnRest():
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']
    cell = request.form['cell']
    awaste = request.form['awaste']
    bwaste = request.form['bwaste']
    cwaste = request.form['cwaste']
    dwaste = request.form['dwaste']
    suggestion = request.form['suggestion']
    image_file = request.form['image_file']
    insert_sql = "INSERT INTO foodstorage VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s )"
    cursor = db_conn.cursor()
    cursor.execute(insert_sql, (name, email, address, cell, awaste, bwaste, cwaste, dwaste, suggestion))
    db_conn.commit()
    cursor.close()

    if image_file.filename == "":
        return "Please select a file"

    try:
        image_file_name_in_s3 = "rest-name-" + str(name) + "_image_file"
        s3 = boto3.resource('s3')
        s3.Bucket(custombucket).put_object(Key=image_file_name_in_s3, Body=image_file)
        bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
        s3_location = (bucket_location['LocationConstraint'])

    if s3_location is None:
        s3_location = ''
    else:
        s3_location = '-' + s3_location

    object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
        s3_location,
        custombucket,
        image_file_name_in_s3)



    return render_template('addRestaurantOutput.html', name=name)


@app.route('/getRestaurant', methods=['GET', 'POST'])
def getRestaurant():
    return render_template("getRestaurant.html")


@app.route('/deleteData', methods=['GET', 'POST'])
def deleteData():
    if request.method == 'POST':
        fetch_sql = "DELETE FROM foodstorage"
        cursor = db_conn.cursor()
        cursor.execute(fetch_sql)
        db_conn.commit()
        cursor.close()
        return render_template("getRestaurant.html")


@app.route('/showName', methods=['GET', 'POST'])
def showName():
    if request.method == 'POST':
        fetch_sql = "SELECT name FROM foodstorage "
        cursor = db_conn.cursor()
        cursor.execute(fetch_sql)
        data = cursor.fetchall()
        db_conn.commit()
        cursor.close()
        return render_template("getRestaurant.html", outp=data)


@app.route('/fetchdata', methods=['GET', 'POST'])
def fetchdata():
    if request.method == 'POST':
        name1 = request.form['name']
        fetch_sql = "SELECT email FROM foodstorage WHERE name = %s"
        cursor = db_conn.cursor()
        cursor.execute(fetch_sql, name1)
        email1 = cursor.fetchone()
        db_conn.commit()
        cursor.close()

        fetch_sql = "SELECT address FROM foodstorage WHERE name = %s"
        cursor = db_conn.cursor()
        cursor.execute(fetch_sql, name1)
        address1 = cursor.fetchone()
        db_conn.commit()
        cursor.close()

        fetch_sql = "SELECT cell FROM foodstorage WHERE name = %s"
        cursor = db_conn.cursor()
        cursor.execute(fetch_sql, name1)
        cell1 = cursor.fetchone()
        db_conn.commit()
        cursor.close()

        fetch_sql = "SELECT awaste FROM foodstorage WHERE name = %s"
        cursor = db_conn.cursor()
        cursor.execute(fetch_sql, name1)
        awaste1 = cursor.fetchone()
        db_conn.commit()
        cursor.close()

        fetch_sql = "SELECT bwaste FROM foodstorage WHERE name = %s"
        cursor = db_conn.cursor()
        cursor.execute(fetch_sql, name1)
        bwaste1 = cursor.fetchone()
        db_conn.commit()
        cursor.close()

        fetch_sql = "SELECT cwaste FROM foodstorage WHERE name = %s"
        cursor = db_conn.cursor()
        cursor.execute(fetch_sql, name1)
        cwaste1 = cursor.fetchone()
        db_conn.commit()
        cursor.close()

        fetch_sql = "SELECT dwaste FROM foodstorage WHERE name = %s"
        cursor = db_conn.cursor()
        cursor.execute(fetch_sql, name1)
        dwaste1 = cursor.fetchone()
        db_conn.commit()
        cursor.close()

        fetch_sql = "SELECT suggestion FROM foodstorage WHERE name = %s"
        cursor = db_conn.cursor()
        cursor.execute(fetch_sql, name1)
        suggestion1 = cursor.fetchone()
        db_conn.commit()
        cursor.close()

        return render_template("getRestaurantOutput.html", name=name1, email=email1, address=address1, cell=cell1,
                               awaste=awaste1, bwaste=bwaste1, cwaste=cwaste1, dwaste=dwaste1, suggestion=suggestion1)


if __name__ == '__main__':
    app.run(debug=True)
