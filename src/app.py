from flask import Flask,render_template,redirect,request,session
import json
from web3 import Web3, HTTPProvider

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

@app.route('/')
def homepage():
    return render_template('index.html')

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

if (__name__=="__main__"):
    app.run(debug=True,host='0.0.0.0',port=5001)