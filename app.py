from flask import Flask,render_template,request,redirect,session
from flask_session import Session
from classes_and_functions.functions.login_test import test_login

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
        return render_template('/pages/main.html',css_file="main.css",js_file="main.js") 

@app.route('/main',methods=['GET'])
def main():
    if(request.method=='GET'):
        return render_template('/pages/main.html',css_file="main.css",js_file="main.js") 
    
if __name__ == '__main__':
    app.run(debug=True)