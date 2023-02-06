from flask import Flask,render_template,redirect,request,session
import json
from web3 import Web3, HTTPProvider
from werkzeug.utils import secure_filename
import os
import hashlib

def hash_file(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()

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

def connect_with_image(acc):
    blockchain="http://127.0.0.1:7545"
    web3=Web3(HTTPProvider(blockchain))
    if acc==0:
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc
    artifact_path="../build/contracts/image.json"
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
    hashid=hash_file(os.path.join(app.config['UPLOAD_FOLDER'], session['username']+'/'+doc1))
    print(hashid)
    try:
        contract,web3=connect_with_image(0)
        tx_hash=contract.functions.addImage(session['username'],os.path.join(app.config['UPLOAD_FOLDER'], session['username']+'/'+doc1),hashid).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return (render_template('dashboard.html',res='image uploaded'))
    except:
        return (render_template('dashboard.html',err='image already uploaded'))
        

@app.route('/myImages')
def myimages():
    try:
        k=os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], session['username']))
        print(k)
        data=[]
        for i in k:
            dummy=[]
            dummy.append(os.path.join(app.config['UPLOAD_FOLDER'], session['username'])+'/'+i)
            data.append(dummy)
        print(data)
    except:
        data=[]
    return render_template('myimages.html',dashboard_data=data,len=len(data))

@app.route('/shareImage')
def shareImage():
    data=[]
    data1=[]
    contract,web3=connect_with_register(0)
    _users,_passwords=contract.functions.viewUsers().call()
    for i in range(len(_users)):
        dummy=[]
        if(_users[i]!=session['username']):
            dummy.append(_users[i])
            data.append(dummy)
    try:
        k=os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], session['username']))
        print(k)
    except:
        k=[]
    for i in k:
        dummy=[]
        dummy.append(os.path.join(app.config['UPLOAD_FOLDER'], session['username'])+'/'+i)
        data1.append(dummy)
    return render_template('shareimage.html',dashboard_data=data,dashboard_data1=data1,len=len(data),len1=len(data1))

@app.route('/toShareBuddy',methods=['post'])
def toShareBuddy():
    flag=0
    userId=request.form['userId']
    docId=request.form['docID']
    #print(userId,docId)
    hashid=hash_file(docId)
    #print(hashid)
    contract,web3=connect_with_image(0)
    _users,_names,_images,_tokens=contract.functions.viewImages().call()
    #print(_users)
    print(_images)
    print(_tokens)
    try:
        for i in range(len(_images)):
            if(hashid==_images[i]):
                print('image found')
                if userId in _tokens[i]:
                    print('Occured')
                    flag=1
                    break
        if(flag==0):
            tx_hash=contract.functions.addToken(hashid,userId).transact()
            web3.eth.waitForTransactionReceipt(tx_hash)
    except:
        pass

    data=[]
    data1=[]
    contract,web3=connect_with_register(0)
    _users,_passwords=contract.functions.viewUsers().call()
    for i in range(len(_users)):
        dummy=[]
        if(_users[i]!=session['username']):
            dummy.append(_users[i])
            data.append(dummy)

    k=os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], session['username']))
    #print(k)
    for i in k:
        dummy=[]
        dummy.append(os.path.join(app.config['UPLOAD_FOLDER'], session['username'])+'/'+i)
        data1.append(dummy)
    if(flag==1):
        return(render_template('shareimage.html',err='Already Shared',dashboard_data=data,dashboard_data1=data1,len=len(data),len1=len(data1)))
    else:
        return(render_template('shareimage.html',res='Shared to Buddy',dashboard_data=data,dashboard_data1=data1,len=len(data),len1=len(data1)))

@app.route('/sharedImages')
def sharedImages():
    data=[]
    contract,web3=connect_with_image(0)
    _users,_names,_images,_tokens=contract.functions.viewImages().call()
    for i in range(len(_names)):
        if session['username'] in _tokens[i][1:]:
            dummy=[]
            dummy.append(_tokens[i][0])
            dummy.append(_names[i])
            data.append(dummy)
    return render_template('sharedimages.html',dashboard_data=data,len=len(data))

@app.route('/mysharedimages')
def mysharedimages():
    contract,web3=connect_with_image(0)
    _users,_names,_images,_tokens=contract.functions.viewImages().call()
    data=[]
    print(_tokens)
    for i in range(len(_names)):
        if(_users[i]==session['username']):
            for j in _tokens[i]:
                if j!=session['username'] and j!='0x0000000000000000000000000000000000000000':
                    dummy=[]
                    dummy.append(_names[i])
                    dummy.append(j)
                    data.append(dummy)

    return render_template('mysharedimages.html',dashboard_data=data,len=len(data))

@app.route('/cancel/static/uploads/<id1>/<id2>/<id3>')
def cancelImage(id1,id2,id3):
    print(id1,id2,id3)
    hashid=hash_file(os.path.join(app.config['UPLOAD_FOLDER']+id1+'/'+id2))
    contract,web3=connect_with_image(0)
    tx_hash=contract.functions.removeToken(hashid,id3).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/mysharedimages')

if (__name__=="__main__"):
    app.run(debug=True,host='0.0.0.0',port=5001)