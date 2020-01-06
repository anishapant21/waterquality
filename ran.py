from flask import Flask, render_template, request
from datetime import datetime
from mongoengine import connect, Document, StringField, IntField, FloatField, DateTimeField
from pymongo import MongoClient


app = Flask(__name__)
app.config['SECRET_KEY'] = 'wanderlust'


connect('waterdata')

client=MongoClient()
db=client.waterdata

class WaterQuality(Document):
    ph_value = FloatField()
    turbidity = FloatField()
    conductivity = FloatField()
    record_date = DateTimeField()
    remedy = StringField()


@app.route('/')
def hello_world():
    db_datas = WaterQuality.objects.order_by('-record_date')
    #print(repr(db_datas[0].ph_value))
    return render_template('index.html', datas=db_datas, dateHere=datetime.now())

@app.route('/aboutus', methods=['GET','POST'])
def about():
    
    return render_template('aboutus.html')


@app.route('/api/postdata', methods=['GET','POST'])
def data_post_handler():

    #print(dir(request), request.json, request.values)
    #post_data = request.json 
    current_date= datetime.now()
    if float(request.args.get('PH'))<6.5:
        remedy="Sodium Hydroxide Injection"
    elif float(request.args.get('PH'))>7.8:
        remedy="Sodium Bicarbonate"
    else:
        remedy=""
    if float(request.args.get('CONDUCT'))>50:
        remedy=remedy+" and"+" Osmosis"


    
    
    print(current_date)
    '''db_cursor = WaterQuality(ph_value=float(post_data.get('ph_value')),
                             turbidity = float(post_data.get('turbidity')),
                             conductivity= float(post_data.get('conductivity')),
                             record_date=current_date,
                             remedy=remedy
                             )'''
                             
    db_cursor = WaterQuality(ph_value=request.args.get('PH'),
                             conductivity=request.args.get('CONDUCT'),
                             record_date=current_date,
                             remedy=remedy
                             )                   
    db_cursor.save()
    return "Data saved"


@app.route('/erase', methods=['GET', 'POST'])
def erase():
    print("All values getting erased")

    if request.method=='POST':
        db.drop('waterdata')

    return render_template("index.html")

@app.route('/selectone', methods=['GET','POST'])
def selectone():
    if request.method=='POST':
        selection=request.form["parameters"]

        if selection=='allThree':
            allData = WaterQuality.objects.order_by('-record_date')
            return render_template('index.html', datas=allData)
        if selection=="phvalue":
            allData=WaterQuality.objects.only('record_date','ph_value')
            return render_template('selectPH.html', datas=allData, dateHere=datetime.now())


        if selection=="conductivity":
            allData=WaterQuality.objects.only('record_date', 'conductivity')
            return render_template('selectCONDUCTIVITY.html', datas=allData, dateHere=datetime.now())
            
        

if __name__ == '__main__':
    app.run(debug=True)