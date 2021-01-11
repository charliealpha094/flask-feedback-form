# Done by Carlos Amaral (2021/01/10)

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import sendmail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':  # Development\
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://carlos:0estupidita!@localhost/mitsubishi'
else: # Production
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://eclddoovzvcqnw:cfd2751668d741e8996831797b531664c7f4f98ee7761fdeae0d41b0489e02eb@ec2-54-235-158-17.compute-1.amazonaws.com:5432/d628p37gu90hh9'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    model = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, model, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.model = model
        self.rating = rating
        self.comments = comments

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST']) # Get data from Form
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        model = request.form['model']
        rating = request.form['rating']
        comments = request.form['comments']
        if customer == '' or dealer == '' or model == '':
            return render_template('index.html', message='Please, enter required fields')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, model, rating, comments)
            db.session.add(data)
            db.session.commit()
            sendmail(customer, dealer, model, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback.')
if __name__ == '__main__':
    app.run()
