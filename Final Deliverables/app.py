import pandas as pd
from flask import Flask, request, jsonify, render_template,redirect,url_for
import pickle

app = Flask(__name__,template_folder='Template')
model = pickle.load(open(r'C:\ProgramData\UAEP\Application Building\university.pkl', 'rb'))



@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict', methods=['GET','post'])
def predict():
	
	GRE_Score = int(request.form['GRE Score'])
	TOEFL_Score = int(request.form['TOEFL Score'])
	University_Rating = int(request.form['University Rating'])
	SOP = float(request.form['SOP'])
	LOR = float(request.form['LOR'])
	CGPA = float(request.form['CGPA'])
	Research = int(request.form['Research'])
	
	final_features = pd.DataFrame([[GRE_Score, TOEFL_Score, University_Rating, SOP, LOR, CGPA,Research]])
	predict=model.predict(final_features)
	
	output=predict[0]
	if output > 0.5:
		return redirect(url_for('chance', percent=output*100))	
	else:
		return redirect(url_for('no_chance', percent=output*100)) 
	
    
	
@app.route("/chance/<percent>")
def chance(percent):
    return render_template("chance.html", content=[percent])

@app.route("/nochance/<percent>")
def no_chance(percent):
    return render_template("noChance.html", content=[percent])	
	
if __name__ == "__main__":
	app.run(debug=True)