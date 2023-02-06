from flask import Flask,render_template,redirect,request,session
import json

app=Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/registerForm',methods=['post'])
def registerForm():
    walletaddr=request.form['walletaddr']
    password=request.form['password']
    print(walletaddr,password)
    
    return render_template('index.html',res="Registered")

if (__name__=="__main__"):
    app.run(debug=True,host='0.0.0.0',port=5001)