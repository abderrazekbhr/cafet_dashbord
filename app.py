from flask import Flask,render_template,request,redirect,session,jsonify
from flask_session import Session
from classes_and_functions.functions.login_test import test_login
from classes_and_functions.functions.read_data_csv import *

app =Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/',methods=['GET','POST'])
def login():
    if(session.get("token")=="connected"):
        return redirect("/main", code=302)
    if(request.method=='GET'):
        return render_template('/pages/login.html',css_file="login.css",js_file="login.js") 
    else:
        email=request.form.get("email")
        password=request.form.get("password")
        if(test_login(email,password)):
            session["token"]="connected"
            return redirect("/main", code=302)
        return render_template('/pages/login.html',css_file="login.css",js_file="login.js") 

@app.route('/main',methods=['GET'])
def main():
    if(session.get("token")=="connected"):
        return render_template('/pages/main.html',css_file="main.css",js_file="main.js")
    return redirect("/", code=302) 
    
@app.route('/logout',methods=['GET'])
def logout():
    session.clear()
    return redirect("/", code=302)

@app.route('/chart-data-salade',methods=['GET'])
def chart_data():
    rq_args=request.args
    return get_data_by_column(["Date","Salade Thon","Salade Poulet"]) .to_json(orient='records') 
 
if __name__ == '__main__':
    app.run(debug=True)