from flask import Flask,render_template,request,flash,redirect,url_for,session
import sqlite3
app=Flask(__name__)
app.secret_key="123"
@app.route('/')
def home():
    return render_template('home.html')
#--------------------------------------------------------------------------------------------
@app.route('/index')
def index():
    return render_template('index.html')
#--------------------------------------------------------------------------------------------
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        con=sqlite3.connect('data2.db')
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from customers where name=? and email=?",(name,password))
        data =cur.fetchall()
        if data:
            return redirect("customer")
        else:
            flash("Details mismatch","danger")
    return render_template('index.html')
#--------------------------------------------------------------------------------------------
@app.route("/contact")
def contact():
    return render_template("contact.html")
#--------------------------------------------------------------------------------------------
@app.route('/about')
def about():
    return render_template('about.html')
#--------------------------------------------------------------------------------------------
@app.route('/header')
def header():
    return render_template('header.html')
#--------------------------------------------------------------------------------------------
@app.route('/main')
def main():
    return render_template('main.html')
#--------------------------------------------------------------------------------------------
@app.route('/menu')
def menu():
    return render_template('menu.html')
#--------------------------------------------------------------------------------------------
@app.route('/main1')
def main1():
    return render_template('main1.html')
#--------------------------------------------------------------------------------------------
@app.route('/menu1')
def menu1():
    return render_template('menu1.html')
#--------------------------------------------------------------------------------------------
@app.route('/logo')
def logo():
    return render_template('logo.html')
#--------------------------------------------------------------------------------------------
@app.route('/customer')
def customer():
    return render_template("customer.html")
#--------------------------------------------------------------------------------------------        
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            name=request.form['name']
            email=request.form['email']
            birth=request.form['birth']
            address=request.form['address']
            phone=request.form['phone']
            con=sqlite3.connect("data2.db")
            con.execute("""create table if not exists customers (pid integer primary key,name text,
            email varchar(20),birth date,address text,phone integer)""")
            cur=con.cursor()
            cur.execute("insert into customers (name,email,birth,address,phone)values(?,?,?,?,?)",(name,email,birth,address,phone))
            con.commit()
            flash("Record Added successfully","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:
            return redirect(url_for('index'))
            con.close()
    return render_template('register.html')
#--------------------------------------------------------------------------------------------
@app.route('/update/<string:id>',methods=['GET','POST'])
def update(id):
    con=sqlite3.connect('data2.db')
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from customers where pid=?",(id))
    data=cur.fetchone()
    con.close()
    if request.method=='POST':
        try:
            name=request.form['name']
            email=request.form['email']
            birth=request.form['birth']
            address=request.form['address']
            phone=request.form['phone']
            con=sqlite3.connect('data2.db')
            cur=con.cursor()
            cur.execute("""update customers set name=?,email=?,birth=?,address=?,phone=? where pid=?""",
            (name,email,birth,address,phone,id))
            con.commit()
            flash("Record update successfully","success")
        except:
            flash("Record Update Error","danger")
        finally:
            return redirect(url_for('view'))
            con.close()
    return render_template('update.html',data=data)
#--------------------------------------------------------------------------------------------
@app.route('/delete/<string:id>',methods=['GET','POST'])
def delete(id):
    try:
        con=sqlite3.connect("data2.db")
        cur=con.cursor()
        cur.execute("delete from customers where pid=?",(id))
        con.commit()
        flash("Record Deleted successfully","success")
    except:
        flash("Record Deleted Error","danger")
    finally:
        return redirect(url_for('view'))
        con.close()
#--------------------------------------------------------------------------------------------
@app.route('/clear/<string:id>',methods=['GET','POST'])
def clear(id):
    try:
        con=sqlite3.connect("data2.db")
        cur=con.cursor()
        cur.execute("delete from item1 where pid=?",(id))
        con.commit()
        flash("Record Deleted successfully","success")
    except:
        flash("Record Deleted Error","danger")
    finally:
        return redirect(url_for('pro'))
        con.close()
#--------------------------------------------------------------------------------------------
@app.route('/view')
def view():
    con=sqlite3.connect('data2.db')
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select  * from customers")
    data=cur.fetchall()
    con.close()
    return render_template('view.html',data=data)
#--------------------------------------------------------------------------------------------
@app.route('/farmer',methods=['GET','POST'])
def farmer():
    if request.method=='POST':
        try:
            product=request.form['product']
            regdate=request.form['regdate']
            qty=request.form['qty']
            name=request.form['name']
            price=request.form['price']
            con=sqlite3.connect("data2.db")
            con.execute("""create table if not exists item1(pid integer primary key,
            Name text,products text,Day date,quantity text,price int)""")
            cur=con.cursor()
            cur.execute("""insert into item1 (Name,products,Day,quantity,price)values
            (?,?,?,?,?)""",(name,product,regdate,qty,price))
            con.commit()
            flash("Product Added Successfully","success")
        except:
            flash("Product Doesn't Added","danger")
        finally:
            return redirect(url_for('farmer'))
            con.close()
    return render_template('farmer.html')
#--------------------------------------------------------------------------------------------
@app.route('/modify/<string:id>',methods=['GET','POST'])
def modify(id):
    con=sqlite3.connect("data2.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from item1 where pid=?",(id))
    data=cur.fetchone()
    con.close()
    if request.method=='POST':
        try:
            product=request.form['product']
            regdate=request.form['regdate']
            qty=request.form['qty']
            name=request.form['name']
            price=request.form['price']
            con=sqlite3.connect("data2.db")
           
            cur=con.cursor()
            cur.execute("""update  item1 set Name=?,products=?,Day=?,quantity=?,price=? where pid=?""",
            (name,product,regdate,qty,price,id))
            con.commit()
            flash("Product Added Successfully","success")
        except:
            flash("Product Doesn't Added","danger")
        finally:
            return redirect(url_for('pro'))
            con.close()
    return render_template('modify.html',data=data)
#--------------------------------------------------------------------------------------------
@app.route('/pro')
def pro():
    con=sqlite3.connect('data2.db')
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select  * from item1")
    data=cur.fetchall()
    con.close()
    return render_template('pro.html',data=data)
#--------------------------------------------------------------------------------------------
@app.route('/logout')
def logout():
    return render_template('home.html')
if __name__=='__main__':
    app.run(debug=True)
