from flask import Flask,render_template,redirect,url_for,request
from flask_mysqldb import MySQL

app=Flask(__name__)

# MySql Configuration 

app.config['MYSQL_DB']='eedb'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_PORT']=3306

# Connection Flask with MySql
mysql=MySQL(app)

@app.route('/')
def index():
    d=(101,'Hello')
    return render_template('index.html')

@app.route('/add')
def regEmployee():
    return render_template('reg.html')

@app.route('/reg',methods=['GET','POST'])
def saveEmployee():
    if request.method == 'POST':
        eid=request.form['eid']
        ename=request.form['ename']
        esal=request.form['esal']
        eaddr=request.form['eaddr']

       # send data into a databases
        cursor=mysql.connection.cursor()
        cursor.execute("INSERT INTO employee(eid,ename,esal,eaddr) values(%s,%s,%s,%s)",(eid,ename,esal,eaddr))
        mysql.connection.commit()

    return redirect('/')

@app.route('/view')
def viewEmployee():
    cursor=mysql.connection.cursor()
    cursor.execute("select * from employee")
    emp=cursor.fetchall()  
    print(emp) #((101, 'Sudhir', 5000.0, 'Nagpur'), (102, 'Rahul', 90000.0, 'pune'), (103, 'dinesh', 50000.0, 'Nagpur'))
    mysql.connection.commit()
    return render_template('view.html',employee=emp)

@app.route('/delete/<int:eid>')  #/delete/101
def deleteEmployee(eid):
    cursor=mysql.connection.cursor()
    cursor.execute("delete from employee where eid=%s",(eid,))
    mysql.connection.commit()
    return redirect('/view')

@app.route('/edit/<int:eid>')  #/edit/101
def editEmployee(eid):
    cursor=mysql.connection.cursor()
    cursor.execute("select * from employee where eid=%s",(eid,)) #(101,sudhir,5000,Nagpur)
    employee=cursor.fetchone()
    mysql.connection.commit()
    return render_template('edit.html',emp=employee)

@app.route('/update/<int:eid>',methods=['GET','POST'])
def updateEmployee(eid):
    if request.method == 'POST':
        eid=request.form['eid']
        ename=request.form['ename']
        esal=request.form['esal']
        eaddr=request.form['eaddr']

       # send data into a databases
        cursor=mysql.connection.cursor()
        cursor.execute("update employee set ename=%s, esal=%s,eaddr=%s where eid=%s",(ename,esal,eaddr,eid))
        mysql.connection.commit()

        return redirect('/view')


if __name__ == '__main__':
    app.run(debug=True)
