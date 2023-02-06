from flask import Flask,render_template,redirect,request,session
import json
from web3 import Web3, HTTPProvider
from werkzeug.utils import secure_filename
import os

def connect_with_register(acc):
    blockchain="http://127.0.0.1:7545"
    web3=Web3(HTTPProvider(blockchain))
    if acc==0:
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc
    artifact_path="../build/contracts/register.json"
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']
        contract_address=contract_json['networks']['5777']['address']
    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    return(contract,web3)


app=Flask(__name__)
app.secret_key='batch16sacet'
app.config["UPLOAD_FOLDER"] = "static/uploads/"

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/dashboard')
def dashboardpage():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session['username']=None
    return redirect('/')

@app.route('/loginForm',methods=['post'])
def loginForm():
    walletaddr=request.form['walletaddr']
    password=request.form['password']
    print(walletaddr,password)
    contract,web3=connect_with_register(0)
    status=contract.functions.loginUser(walletaddr,int(password)).call()
    if status==True:
        session['username']=walletaddr
        return redirect('/dashboard')
    else:
        return render_template('index.html',err2="Invalid Credentials")

@app.route('/registerForm',methods=['post'])
def registerForm():
    walletaddr=request.form['walletaddr']
    password=request.form['password']
    print(walletaddr,password)
    try:
        contract,web3=connect_with_register(0)
        tx_hash=contract.functions.registerUser(walletaddr,int(password)).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return render_template('index.html',res="Registered")
    except:
        return render_template('index.html',err="Already Registered")

@app.route('/uploadImage',methods=['post','get'])
def uploadImage():
    doc=request.files['chooseFile']
    if session['username'] not in os.listdir(app.config['UPLOAD_FOLDER']):
        os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], session['username']))
    doc1=secure_filename(doc.filename)
    doc.save(os.path.join(app.config['UPLOAD_FOLDER'], session['username']+'/'+doc1))
    return (render_template('dashboard.html',res='image uploaded'))

@app.route('/myImages')
def myimages():
    k=os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], session['username']))
    print(k)
    data=[]
    for i in k:
        dummy=[]
        dummy.append(os.path.join(app.config['UPLOAD_FOLDER'], session['username'])+'/'+i)
        data.append(dummy)
    print(data)
    return render_template('myimages.html',dashboard_data=data,len=len(data))

if (__name__=="__main__"):
    app.run(debug=True,host='0.0.0.0',port=5001)