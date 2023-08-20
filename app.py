import numpy as np
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import model_from_json
from scrape import tokenize_indic,one_hot_encoded,process
import numpy
import os,string


# Build and train your neural network using the Keras API within TensorFlow


finallang=['Bengali','Gujarati','Hindi','Kannada','Malyalam','Marathi','Oriya','Punjabi','Tamil','Telugu']
N_LANG=len(finallang)
ls=string.punctuation + '−।\u25AA\u0964'
global translate_table
translate_table=dict((ord(char),"") for char in ls)

app = Flask(__name__)
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("model.h5")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    input_data=request.form['input_data']
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
      mean[i]=round((mean[i]/lensent)*100,2)
      
    
    
    result=zip(finallang,mean)
    

    return render_template('result.html', result=result)



if __name__ == "__main__":
    app.run(debug=True)
