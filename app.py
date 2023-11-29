from flask import Flask,render_template,request,redirect,url_for,session
import requests
import sqlite3 as sql

app=Flask(__name__)
app.secret_key="maha"

url="https://api.mfapi.in/mf/"
# list1=[]

@app.route('/',methods=['POST',"GET"])
def home():
    list1=[]
    conn=sql.connect("account.db")
    cur=conn.cursor()
    cur.execute("select * from trans")
    data=cur.fetchall()
    for i in data:
        id=i[0]
        name=i[1]
        fund=i[2]
        invested=i[3]
        unit=i[4]
    
        user={}
        first=requests.get(url+str(fund))
        user.update({"name":name})
        user.update({"id":id})
        fund_house=first.json().get("meta").get("fund_house")
        user.update({"fund_house":fund_house})
        user.update({"invested":invested})
        user.update({"unit":unit})
        nav=first.json().get("data")[0].get("nav")
        user.update({"nav":nav})
        current=float(user.get("nav"))*int(user.get("invested"))
        user.update({"current":current})
        growth=float(user.get("current"))-int(user.get("unit"))
        user.update({"growth":growth})
        list1.append(user)
    return render_template("sample.html",datas=list1)


@app.route('/add',methods=['POST','GET'])
def add():
    if request.method=="POST":
        name=request.form.get("name")
        fund=request.form.get("fund")
        invested=request.form.get("invested")
        unit=request.form.get("unit")
        conn=sql.connect("account.db")
        conn.row_factory=sql.Row
        cur=conn.cursor()
        cur.execute("insert into trans (name,fund,invested,unit) values(?,?,?,?)"
                    ,(name,fund,invested,unit))
        conn.commit()
        return redirect(url_for("home"))
    return render_template("add.html")

@app.route('/login',methods=["POST","GET"])
def login():
    if request.method=="POST":
        name=request.form.get("name")
        password=request.form.get("password")
        conn=sql.connect("account.db")
        conn.row_factory=sql.Row
        cur=conn.cursor()
        cur.execute("select * from login where name=?",(name,))
        data=cur.fetchone()
        if data:
            if str(data["name"])==name and str(data["password"])==password:
                session["username"]=name
            return redirect(url_for("home"))
    return render_template("login.html")



@app.route('/logout',methods=["POST","GET"])
def logout():
    session.pop("username",None)
    return redirect(url_for("home"))


@app.route('/signin',methods=["POST","GET"])
def signin():
    if request.method=="POST":
        name=request.form.get("name")
        password=request.form.get("password")
        conn=sql.connect("account.db")
        conn.row_factory=sql.Row
        cur=conn.cursor()
        cur.execute("insert into signin (name,password) values(?,?)",(name,password))
        conn.commit()
        return redirect(url_for("home"))
    return render_template("signin.html")


@app.route('/edit/<int:id>',methods=["POST","GET"])
def edit(id):
     if request.method=="POST":
         
         name=request.form.get("name")
         fund=request.form.get("fund")
         invested=request.form.get("invested")
         unit=request.form.get("unit")
         conn=sql.connect("account.db")
         cur=conn.cursor()
         cur.execute("update  trans  set name=?,fund=?,invested=?,unit=? where id=?",
                    (name,fund,invested,unit,id))
         conn.commit()
         return redirect(url_for("home"))
     conn=sql.connect("account.db")
     conn.row_factory=sql.Row
     cur=conn.cursor()
     cur.execute("select * from trans where id=?",(id,))
     data=cur.fetchone()
     return render_template("edit.html",datas=data)


@app.route('/delete/<int:id>',methods=["GET"])
def delete(id):
    conn=sql.connect("account.db")
    conn.row_factory=sql.Row
    cur=conn.cursor()
    cur.execute("delete from trans where ID=?",(id,))
    conn.commit()
    return redirect(url_for("home"))
        



if __name__=="__main__":
    app.run(debug=True)






