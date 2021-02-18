import numpy as np
from flask import Flask, request, jsonify, render_template
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
from scrape import tokenize_indic,one_hot_encoded,process
import numpy
import os

finallang=['Bengali','Gujarati','Hindi','Kannada','Malyalam','Marathi','Oriya','Punjabi','Tamil','Telugu']

app = Flask(__name__)
json_file = open('/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("/model.h5")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    input_data=request.form.values()
    mean=np.zeros(N_LANG)
    input_data=input_data.translate(translate_table)
    lensent=len(tokenize_indic(input_data))
    for x in tokenize_indic(input_data):
      x=one_hot_encoded(process(x))
      x=np.reshape(x,(1,x.shape[0],x.shape[1]))
      pred = model.predict(x)
      for i in range(len(pred[0])):
        mean[i]+=pred[0][i]
        
    for i in range(len(mean)):
      mean[i]=mean[i]/lensent
    result='Language Percent Distribution\n'
    
    for i,j in zip(mean,finallang):
      result+= '{}: {}%\n'.format(j,round(100*i),2)

    return render_template('index.html', prediction_text=result)



if __name__ == "__main__":
    app.run(debug=True)