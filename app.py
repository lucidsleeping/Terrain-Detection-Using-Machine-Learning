import re
from flask import *
import tensorflow as tf
import numpy as np
import os
from keras.applications import imagenet_utils
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['IMAGE_UPLOADS'] = UPLOAD_FOLDER


def detect(fname):
    filename= '.\\uploads\\'+fname
    result = []
    try:
        img=image.load_img(filename,target_size=(224,224))
        mobile =tf.keras.applications.mobilenet.MobileNet()
        resized_img=image.img_to_array(img)
        final_image=np.expand_dims(resized_img,axis=0)
        final_image=tf.keras.applications.mobilenet.preprocess_input(final_image)
        pred=mobile.predict(final_image)
        print(pred)
        result=imagenet_utils.decode_predictions(pred)
        return result
    except:
        return -1


    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def uploadimg():
    if request.method == "POST":
        if 'image' not in request.files:
            return redirect('/')
        
        file1 = request.files['image']
        path = os.path.join(app.config['IMAGE_UPLOADS'], file1.filename)
        try:
            file1.save(path)
            out = []
            
            out = detect(file1.filename)

            if out!=-1:
                for i in range(len(out[0])):
                    print(out[0][i][1])
                return render_template('result.html', results=out, n=len(out[0]))
            else:
                return redirect('/')
        except:
            return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)