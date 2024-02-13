from flask import Flask,render_template,request,redirect,session,jsonify
from flask_session import Session
from classes_and_functions.functions.login_test import test_login,update_data
from classes_and_functions.functions.read_data_csv import *

app =Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/',methods=['GET','POST'])
def login():
    if(session.get("token")=="connected"):
        return redirect("/main-salade", code=302)
    if(request.method=='GET'):
        return render_template('/pages/login.html',css_file="login.css",js_file="login.js") 
    else:
        email=request.form.get("email")
        password=request.form.get("password")
        if(test_login(email,password)):
            session["token"]="connected"
            return redirect("/main-salade", code=302)
        return render_template('/pages/login.html',css_file="login.css",js_file="login.js") 

@app.route('/main-salade',methods=['GET'])
def main_salade():
    if(session.get("token")=="connected"):
        return render_template('/pages/salade.html',css_file="main.css",js_file="main.js")
    return redirect("/", code=302) 

@app.route('/main-sandwich',methods=['GET'])
def main_sandwich():
    if(session.get("token")=="connected"):
        return render_template('/pages/sandwich.html',css_file="main.css",js_file="main.js")
    return redirect("/", code=302) 

@app.route('/main-vanoiserie',methods=['GET'])
def main_vanoiserie():
    if(session.get("token")=="connected"):
        return render_template('/pages/vanoiserie.html',css_file="main.css",js_file="main.js")
    return redirect("/", code=302) 

    
@app.route('/logout',methods=['GET'])
def logout():
    session.clear()
    return redirect("/", code=302)

@app.route('/update',methods=['POST'])
def update():
    email=request.args.email
    password=request.args.password
    data={
        "email":email,
        "password":password
    }
    update_data(data)
    session.clear()
    return redirect("/", code=302)


@app.route('/chart-data-salade',methods=['GET'])
def chart_salade():
    return get_data_by_column(["Date","Salade Thon","Salade Poulet"]) .to_json(orient='records') 

@app.route('/chart-data-sandwich',methods=['GET'])
def chart_sandwich():
    return get_data_by_column(["Date","Sandwiches poulet crudités","Sandwiches thon cruditès","Sandwiches végétarien","Sandwiches poulet mexicain","Sandwiches chèvre miel crudités","Sandwiches poulet curry","Sandwiches saumon","Panini 4 fromages","Panini poulet Kebab"]) .to_json(orient='records') 
 
@app.route('/chart-data-vanoiserie',methods=['GET'])
def chart_vanoiserie():
    return get_data_by_column(["Date","Pain au chocolat","Croissant","Pains suisses"]) .to_json(orient='records') 
 
 
if __name__ == '__main__':
    app.run(debug=True)