import requests
import random
import time
from flask import Flask, render_template, request

app = Flask(__name__)
'''for i in range(5):
    data = {"ph_value": random.randint(0,14), 'turbidity':random.randint(0,5),'conductivity': random.randint(15, 80) }
    response = requests.post('http://127.0.0.1:5000/api/postdata', json=data)
    time.sleep(5)'''
'''reuest le getpost easy banauxa... hareko data ko dict banako cha... post garyo (fist arg url, data)
post api thavayena vane http libraay ma postdata?phvalueamp= get request handle garna lai get
request.query.get
.'''
@app.route('/getData')
def getData():
		data={"ph_value":request.args.get('PH'), "conductivity":request.args.get('CONDUCT')}
		response=requests.post('http://127.0.0.1:5000/api/postdata', json=data)
		time.seep(5)


