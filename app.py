import os
from fileinput import filename

import mysql.connector
import mysql.connector as mysql
import pandas as pd
from flask import Flask, render_template, request, flash, redirect, url_for, session
from mysql.connector import connection, cursor

from logging import FileHandler, WARNING
from os.path import join, dirname, realpath

app = Flask(__name__)

app.secret_key = os.urandom(24)
app.secret_key = "ayush"

app.config["DEBUG"] = True
# Upload folder
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Get the uploaded files
@app.route("/upload", methods=['POST'])
def upload():
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        parseCSV(file_path)
    # save the file
    return redirect(url_for('adminhome'))


def parseCSV(filePath):
    # CVS Column Names
    col_names = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14']
    # Use Pandas to parse the CSV file
    csvData = pd.read_csv(filePath, names=col_names, header=None, encoding='unicode_escape')
    # Loop through the Rows
    for i, row in csvData.iterrows():
        # sql = "INSERT INTO dataset (s1, s2, s3, s4, s5, s6,s7,s8, s9) VALUES (%s, %s,%s,%s,%s, %s, %s, %s, %s)"
        # value = (row['s1'],row['s2'],row['s3'],row['s4'],row['s5'],row['s6'],row['s7'],row['s8'],row['s9'])
        db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                      database='medical_service')
        cursor = db_connection.cursor()
        cursor.execute("delete from dataset")
        cursor.execute(
            "INSERT INTO dataset (s1, s2, s3, s4, s5, s6,s7,s8, s9,s10,s11,s12,s13,s14) VALUES (%s, %s,%s,%s,%s, %s, %s, %s, %s,%s,%s,%s,%s,%s)",
            (row['s1'], row['s2'], row['s3'], row['s4'], row['s5'], row['s6'], row['s7'], row['s8'], row['s9'],
             row['s10'], row['s11'], row['s12'], row['s13'], row['s14']))
        db_connection.commit()
        # print(i,row['first_name'],row['last_name'],row['address'],row['street'],row['state'],row['zip'])


@app.route('/')
def home():  # put application's code here
    return render_template('index.html')


@app.route("/Login")
def Login():
    return render_template("login.html")


@app.route("/contact1")
def contact1():
    return render_template("contact1.html")


@app.route("/adminhome")
def adminhome():
    return render_template("adminhome.html")


@app.route("/dhome")
def dhome():
    return render_template("donorhome.html")


@app.route("/userhome")
def userhome():
    return render_template("userhome.html")


@app.route("/Register")
def Register():
    return render_template("register.html")


@app.route("/addapproval")
def addapproval():
    return render_template("Approval.html")


@app.route("/donation")
def donation():
    return render_template("adddonor.html")


@app.route("/chat")
def chat():
    return render_template("chat1.html")


@app.route("/addfund")
def addfund():
    db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                  database='medical_service')

    if 'name' in session:
        email = session['name']
    if 'uname' in session:
        name = session['uname']


    else:
        print("Not in sesson")
    cursor = db_connection.cursor()
    cursor.execute("select MAX(id) from fund")
    data = cursor.fetchone()
    lid = data[0]
    if lid == None:
        lid = "1"
    else:
        lid = lid + 1

    return render_template("addfund.html", lid=lid, sid=email, sid1=name)


@app.route("/donorRegister")
def donorRegister():
    return render_template("donorregister.html")


@app.route('/checklogin', methods=['POST'])
def checklogin(rows=None):
    if request.method == 'POST' and 'name' in request.form and 'pass' in request.form:
        username = request.form['name']
        password = request.form['pass']
        usertype = request.form['utype']
    if username == "Admin" and password == "Admin" and usertype == "Admin":
        flash("Login Success")
        return render_template('hospital.html')

    if usertype == "User":
        db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                      database='medical_service')
        cursor = db_connection.cursor()
        cursor.execute("SELECT username,password,name FROM registration WHERE username = '%s' AND password = '%s' "
                       % (username, password))
        account = cursor.fetchone()
        uname, passworddd, user_name = account

        if account:
            flash("Login Success")
            print("welcome")
            session['name'] = request.form['name']
            session['uname'] = user_name

        return render_template('userhome.html')

    if usertype == "Donor":
        db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                      database='medical_service')

        cursor = db_connection.cursor()
        cursor.execute("SELECT username,password FROM donorregistration WHERE username = '%s' AND password = '%s' "
                       % (username, password))
        account = cursor.fetchone()
        if account:
            flash("Login Success")

        return render_template('donorhome.html')


@app.route('/checkhospital', methods=['POST'])
def checkhospital():
    if request.method == 'POST':
        usertype = request.form['utype']
        print("WELCOME")
        db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                      database='medical_service')
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM fund WHERE hname = '%s'  "
                       % (usertype))
        data = cursor.fetchall()
        cursor.close()
        return render_template('viewdonreg.html', userlist=data)


@app.route('/register_details', methods=['POST'])
def register_details():
    if request.method == "POST":
        uname = request.form['name']
        email = request.form['Email']
        contact = request.form['contact']
        address = request.form['Address']
        username = request.form['Username']
        password = request.form['Password']

        db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                      database='medical_service')
        cursor = db_connection.cursor()

        cursor.execute(
            "INSERT INTO registration (name,Email,contact,Address,username,password ) VALUES(%s, %s, %s,%s, %s, %s)",
            (uname, email, contact, address, username, password))
        db_connection.commit()

        return render_template('Login.html')


@app.route('/donor_details', methods=['POST'])
def donor_details():
    if request.method == "POST":
        uname = request.form['name']
        email = request.form['Email']
        contact = request.form['contact']
        address = request.form['Address']
        username = request.form['Username']
        password = request.form['Password']

        db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                      database='medical_service')
        cursor = db_connection.cursor()

        cursor.execute(
            "INSERT INTO donorregistration (name,Email,contact,Address,username,password ) VALUES(%s, %s, %s,%s, %s, %s)",
            (uname, email, contact, address, username, password))
        db_connection.commit()

        return render_template('Login.html')


@app.route('/fund_details', methods=['POST'])
def fund_details():
    if request.method == "POST":
        Requestid = request.form['id']
        Name = request.form['name']
        FundAmount = request.form['amt']
        pid = request.form['regid']
        Disease = request.form['disease']
        HospitalName = request.form['utype1']
        Priority = request.form['utype']
        f = request.files['proof']
        f.save("static/uploads/" + f.filename)
        f1 = request.files['proof2']
        f1.save("static/uploads/" + f1.filename)

        UPI = request.form['upi']
        status = "Approved"

        db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                      database='medical_service')
        cursor = db_connection.cursor()


        print(pid,Name,Disease,HospitalName,FundAmount)

        cursor.execute("SELECT s2,s3,s8,s9,s14 FROM dataset WHERE s2 = '%s' AND s3 = '%s' AND s8 = '%s' AND s9 = '%s' AND s14 = '%s' "
                       % (pid, Name,Disease,HospitalName,FundAmount))
        data = cursor.fetchone()

        print(data)
        cursor.close()

        if data:
            print("after data")
            db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                          database='medical_service')
            cursor = db_connection.cursor()

            cursor.execute(
                "INSERT INTO fund (id,name,amt,patientid,disease,hname,Priority,proof,proof2,upi,statusinfo ) VALUES(%s, %s, %s,%s, %s, %s,%s, %s, %s,%s,%s)",
                (Requestid, Name, FundAmount, pid, Disease, HospitalName, Priority, f.filename, f1.filename,
                 UPI, status))
            print("hi")
            db_connection.commit()
        else:
            print("Fake")

        return render_template('index.html')


@app.route('/approval', methods=['POST'])
def approval():
    if request.method == "POST":
        Requestid = request.form['id']
        status = request.form['tid5a']
        db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                      database='medical_service')
        cursor = db_connection.cursor()

        statement = "UPDATE fund SET statusinfo='" + status + "'  WHERE id ='" + Requestid + "'"

        cursor.execute(statement)

        db_connection.commit()

        return render_template('index.html')


@app.route('/donor', methods=['POST'])
def donor():
    if request.method == "POST":
        Requestid = request.form['id']

        getinfo = request.form['getinfo1']
        pname = request.form['pname']
        Amount = request.form['amt']
        payusername = request.form['puname']

        upid = request.form['upid']
        Remarks = request.form['remarks']
        name = 'admin'
        # if len(getinfo) >= 0:

        print("welcome" + pname)






        if getinfo.__eq__("uploaddonation"):

            if (len(pname) > 1):
                f = request.files['pproof']
                f.save("static/uploads1/" + f.filename)
                db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                              database='medical_service')
                cursor = db_connection.cursor()

                cursor.execute(
                    "INSERT INTO donor (id,pname,amt,puname,file,upid,remarks ) VALUES(%s, %s, %s,%s, %s,%s,%s)",
                    (Requestid, pname, Amount, payusername, f.filename, upid, Remarks))

                db_connection.commit()
                return render_template('index.html')
            if len(pname) <= 1:
                db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                              database='medical_service')
                cursor = db_connection.cursor()

                cursor.execute("SELECT id,name,upi FROM fund WHERE id = '%s' OR name = '%s'  "
                               % (Requestid, name))
                account = cursor.fetchone()

                idinfo, nameinfo, upiinfo = account

                return render_template('adddonor.html', glid=Requestid, gname=nameinfo, gupi=upiinfo)


@app.route('/insertchat', methods=['GET', 'POST'])
def insertchat():
    if request.method == "POST":
        keyword = list()

        msginfo = request.form['msg']
        if msginfo == "hi":
            keyword.append('Welcome User')
        if msginfo == "Maximum Donation Amount":
            keyword.append('50000')
        if msginfo == "How Much Amount I Can Donate":
            keyword.append('You can Donate Maximum 50000/- Rs')
        if msginfo == "This Site is Trust":
            keyword.append('Yes')
        else:
            keyword.append('Sorry I cant Understand, Please Contact Hospital')
        return render_template('chat1.html', userdata=keyword)


@app.route('/Viewuser')
def Viewuser():
    db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                  database='medical_service')
    cursor = db_connection.cursor()
    cursor.execute("SELECT  * from registration")
    data = cursor.fetchall()
    cursor.close()
    return render_template('viewuser.html', userlist=data)


@app.route('/viewfund')
def viewfund():
    db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                  database='medical_service')
    cursor = db_connection.cursor()
    cursor.execute("SELECT  * from fund")
    data = cursor.fetchall()
    cursor.close()
    return render_template('viewfund.html', fundlist=data)


@app.route('/viewdataset')
def viewdataset():
    db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                  database='medical_service')
    cursor = db_connection.cursor()
    cursor.execute("SELECT  * from dataset")
    data = cursor.fetchall()
    cursor.close()
    return render_template('viewdataset.html', dataset=data)


@app.route('/viewfund1')
def viewfund1():
    db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                  database='medical_service')
    cursor = db_connection.cursor()
    cursor.execute("SELECT  * from fund where statusinfo='Approved' ")
    data = cursor.fetchall()
    cursor.close()
    return render_template('viewfund1.html', fundlist=data)


@app.route('/viewfund2')
def viewfund2():
    db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                  database='medical_service')
    cursor = db_connection.cursor()
    cursor.execute("SELECT  * from fund where statusinfo='Approved' ")
    data = cursor.fetchall()
    cursor.close()
    return render_template('viewfund2.html', fundlist=data)


@app.route('/viewfund3')
def viewfund3():
    if 'uname' in session:
        name = session['uname']
    print("user fund view" + name)
    db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                  database='medical_service')
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM fund WHERE name = '%s' "
                   % (name))
    data = cursor.fetchall()
    cursor.close()
    return render_template('viewfund3.html', fundlist=data)


@app.route('/viewapproval')
def viewapproval():
    db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                  database='medical_service')
    cursor = db_connection.cursor()
    cursor.execute("SELECT  id,statusinfo from fund where statusinfo='Approved'")
    data = cursor.fetchall()
    cursor.close()
    return render_template('viewapproval.html', approvallist=data)


@app.route('/viewapproval1')
def viewapproval1():
    if request.method == 'POST':
        statusinfo = "Approved"

        db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                      database='medical_service')
        cursor = db_connection.cursor()
        cursor.execute("SELECT id,statusinfo FROM fund WHERE statusinfo = '%s'  "
                       % (statusinfo))
        data = cursor.fetchall()
        cursor.close()
        return render_template('viewapproval1.html', approvallist=data)


@app.route('/viewdonor')
def viewdonor():
    db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                  database='medical_service')
    cursor = db_connection.cursor()
    cursor.execute("SELECT  * from donor")
    data = cursor.fetchall()
    cursor.close()
    return render_template('viewdonor.html', donorlist=data)


@app.route('/viewdonor1')
def viewdonor1():
    if 'uname' in session:
        name = session['uname']
    print("user" + name)
    db_connection = mysql.connect(user='root', password='', host='127.0.0.1', charset='utf8',
                                  database='medical_service')
    cursor = db_connection.cursor()

    cursor.execute("SELECT  * from donor  WHERE pname = '%s' " % (name))
    data = cursor.fetchall()
    cursor.close()
    return render_template('viewdonor1.html', donorlist=data)


if __name__ == '__main__':
    app.run()
