import tensorflow as tf
import numpy as np
from keras.applications import imagenet_utils
from tensorflow.keras.preprocessing import image

import os
from os import listdir

key = []
def function(filename):

    img=image.load_img(filename,target_size=(224,224))

    mobile =tf.keras.applications.mobilenet.MobileNet()
        
    resized_img=image.img_to_array(img)
    final_image=np.expand_dims(resized_img,axis=0)
    final_image=tf.keras.applications.mobilenet.preprocess_input(final_image)
    pred=mobile.predict(final_image)
    #print(pred)
    result=imagenet_utils.decode_predictions(pred)
    flag=0
    count=0
    for i in range(len(result[0])):
        if i not in key:
            key.append(result[0][i][1])





# get the path/directory
# import the modules
import os
from os import listdir

# get the path/directory
folder_dir = "./onroad"
for images in os.listdir(folder_dir):

	# check if the image ends with png
	if (images.endswith(".jpg") or images.endswith(".png")):
		function(folder_dir+"/"+images)


print(key)
