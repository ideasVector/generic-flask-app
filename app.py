from datetime import datetime
from flask import Flask, render_template, request, redirect, jsonify
import os
from models import *


app = Flask(__name__)

servername = '(localdb)\MSSQLLocalDB'
dbname = 'CarSales'
# cstr = os.environ.get('SQLAZURECONNSTR_WWIF',"mssql+pyodbc://@(localdb)\MSSQLLocalDB/CarSales?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server")
cstr = os.environ.get('SQLAZURECONNSTR_WWIF',"mssql+pyodbc://ideasvector:S$g3M1l3s108987@ideasvector.database.windows.net:1433/GenericSQLDatabase?driver=ODBC+Driver+17+for+SQL+Server")
# 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:ideasvector.database.windows.net,1433;Database=GenericSQLDatabase;Uid=ideasvector;Pwd=S@g3M1l3s108};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
app.config['SQLALCHEMY_DATABASE_URI'] = cstr
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
db.create_all()

@app.route('/')
def index():
    cars = Cars.query.all()
    sales_people = SalesPeople.query.all()
    return render_template("carslist.html", cars=cars, sales_people=sales_people)


@app.route("/addcar", methods=['GET', 'POST'])
def addcar():
    if request.method == 'GET':
        return render_template("addcar.html", car={})
    if request.method == 'POST':
        name = request.form["name"]
        year = int(request.form["year"])
        price = float(request.form["price"])
        newcar = Cars(name=name, year=year, price=price)
        db.session.add(newcar)
        db.session.commit()
        return redirect('/')


@app.route('/updatecar/<int:id>', methods=['GET', 'POST'])
def updatecar(id):
    if request.method == 'GET':
        car = Cars.query.filter_by(id=id).first()
        return render_template("addcar.html", car=car)
    if request.method == 'POST':
        name = str(request.form["name"])
        year = int(request.form["year"])
        price = float(request.form["price"])
        car = Cars.query.filter_by(id=id).first()
        car.name = name
        car.year = year
        car.price = price
        db.session.commit()
        return redirect('/')


@app.route('/deletecar/<int:id>')
def deletecar(id):
    Cars.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/')


@app.route('/addsale', methods=['GET', 'POST'])
def addsale():
    new_car_id = request.form.get('salescar_id')
    new_salesperson_id = request.form.get('salesperson_id')
    new_price = request.form.get('actual_price')
    new_sale = CarSales(car_id=new_car_id, salesperson_id=new_salesperson_id, price=new_price)
    db.session.add(new_sale)
    db.session.commit()
    total_sales = db.session.execute('select sum(price) as sales from car_sales where salesperson_id = %s' % new_salesperson_id)
    for row in total_sales:
        total = row['sales']
    return jsonify({'result': 'Added', 'total': total})


if __name__ == '__main__':
   app.run()