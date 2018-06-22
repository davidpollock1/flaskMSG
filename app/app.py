from flask import Flask, render_template, flash
from wtforms import StringField, IntegerField
from wtforms.widgets import TextArea
from twilio.rest import Client
from credentials import account_sid, auth_token, my_phone, my_twilio
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost/learningflask'
db = SQLAlchemy(app)


# if form validates, calls to send_sms function 
@app.route('/form', methods=['GET', 'POST'])
def form():
	form = sendForm()
	if form.validate_on_submit():
		results = send_sms(form.message.data, form.contactNum.data)
		addDB = add(form.message.data, form.contactNum.data)
	return render_template('form.html', form=form)

	

# class for database model
class smsInfo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	message = db.Column(db.String)
	contactNum = db.Column(db.BigInteger)



# add to database and commit
def add(message,contactNum):
	info = smsInfo(message=message,contactNum=contactNum) #testing 
	db.session.add(info)
	db.session.commit()



# wtform web form
class sendForm(FlaskForm):
	message = StringField('Message', widget=TextArea())
	contactNum = IntegerField('Contact Number')



# function that actually sends message
def send_sms(message, contactNum):
	client = Client(account_sid, auth_token)
	return client.messages.create(
                            to=contactNum,
                            from_='+12486174847',
                            body=message)



if __name__ == '__main__':
	app.run(debug=True)