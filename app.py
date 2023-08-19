'''
Creating Flask app for hosting and serving web app
1. Create Flask app.
2. Remember to create templates/index.html
'''

from flask import Flask, request, render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler

from src.pipeline.predict_pipeline import CustomData, PredictPipeline

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method=='GET':
        return render_template('home.html')
    else:
        #request is the object we get our data from the frontend in
        #form is the tag of html from which we are getting our data
        #get extracts the required value
        data=CustomData(
            gender=request.form.get('gender'), 
            race_ethnicity=request.form.get('race_ethnicity'), 
            parental_level_of_education=request.form.get('parental_level_of_education'), 
            lunch=request.form.get('lunch'), 
            test_preparation_course=request.form.get('test_preparation_course'), 
            reading_score=float(request.form.get('reading_score')), #typecasting
            writing_score=float(request.form.get('writing_score'))  #typecasting
        )

        pred_df=data.get_data_as_df()               #Convert data received to a dataframe. That func converts data to a dict then to df
        # pd.set_option('display.max_columns', None) #this was to display all columns in the console below 
        # print(pred_df.head())

        predict_pipeline=PredictPipeline()          #after getting datapoint in df, we can use predict pipeline
        res=predict_pipeline.predict(pred_df)

        return render_template('home.html', results=res[0])

'''
When we run our flask app, we go to the home page initially. There we only have index.html which is empty
We want to run predict endpoint so we go to 127.0.0.1:5000/predict  (default port is 5000)
It has home.html as is waiting for our input. When we enter all inputs and click Predict button, the form is submitted.
The form is submitted to /predict since that is what we have entered in url_form.
Since the method is post (look at home.html form action), we run the else part.
data object is populated with shown variables.
It is converted to df
then used for prediction after preprocessing in prediction_pipeline.py
'''

if __name__=="__main__":
    #maps to 127.0.0.1 which is our own IP
    app.run(host='0.0.0.0', debug=True)