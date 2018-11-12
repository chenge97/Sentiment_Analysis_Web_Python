from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.validators import Length
import numpy as np
import pandas as pd
import re
from sklearn.externals import joblib
from nltk.corpus import stopwords


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
	
class ReusableForm(Form):
    message = StringField(validators=[Length(min =10, max=200)])
    button = SubmitField('Guess')

    

@app.route('/', methods=['GET', 'POST'])
def English():
	form = ReusableForm(request.form)
	if request.method == 'POST':
		message=request.form['message']
		print(message)
		if form.validate():
			filename = 'model.pkl' #Loading File
			loaded_model = joblib.load(filename)
			test = message
			delete = re.compile('[^a-zA-Z]')
			test = delete.sub(' ', test)
			test = test.lower()
			test= ' '.join([word for word in test.split()
			                   if word not in stopwords.words('english')])
			'''Applying a little filter to the message to get a better result such as  removing numbres, adding spaces ,
			putting everything into lowercase and removing stopwords'''
			result = loaded_model.predict([test]) #Testing it
			if(result == 1):
				flash(message + ' is a positive message')
			else:
				flash(message + ' is a negative message')

			form.message.data = '' #Removig the content in the textfield and aboiding a loop in the form with redirect
			return redirect(url_for('English')) 
		else:
			flash('Please introduce a message')
			form.message.data = ''
			return redirect(url_for('English'))

            
 
	return render_template("english.html", options =['English', 'Spanish'], form= form)



class ReusableForm2(Form):
    message = StringField(validators=[Length(min =10, max=200)])
    button = SubmitField('Adivinar')


@app.route('/spanish/', methods=['GET', 'POST'])
def Spanish():

	form = ReusableForm2(request.form)
	if request.method == 'POST':
		message=request.form['message']
		print(message)
		if form.validate():
			filename = 'model_spanish.pkl' #Loading File
			loaded_model = joblib.load(filename)
			test = message
			delete = re.compile('[^a-zA-Z]')
			test = delete.sub(' ', test)
			test = test.lower()
			test= ' '.join([word for word in test.split()
			                   if word not in stopwords.words('spanish')])
			'''Applying a little filter to the message to get a better result such as  removing numbres, adding spaces ,
			putting everything into lowercase and removing stopwords'''
			result = loaded_model.predict([test]) #Testing it
			if(result == 1):
				flash(message + ' es un mensaje positivo')
			else:
				flash(message + ' es un mensaje negativo')

			form.message.data = '' #Removig the content in the textfield and aboiding a loop in the form with redirect
			return redirect(url_for('Spanish')) 
		else:
			flash('Por favor llene el campo')
			form.message.data = ''
			return redirect(url_for('Spanish'))

	return render_template("spanish.html", options =['English', 'Spanish'] ,form = form)



if __name__ == '__main__':
	app.run(debug=True)
