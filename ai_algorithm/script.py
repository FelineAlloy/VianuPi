from tensorflow import keras
from PIL import Image, ImageOps
import numpy as np
import os

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = keras.models.load_model('keras_model.h5', compile=False)

# Specify the folder path containing the images
folder_path = os.path.dirname(os.path.realpath(__file__)) + '/Date_AstroAGR/VianuPi'

# Get a list of all files in the folder
file_list = os.listdir(folder_path)

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

i = 0
with open('output.txt', 'w') as file:
    # Iterate over each file in the folder
    for file_name in file_list:
        # Check if the file is an image (you can add more file extensions if needed)
        if file_name.endswith(".jpg"):
            i = i + 1
            # Construct the full path to the image file
            image_path = os.path.join(folder_path, file_name)
            
            # Open the image
            image = Image.open(image_path)
            
            # Resize the image to a 224x224 with the same strategy as in TM2:
            # Resizing the image to be at least 224x224 and then cropping from the center
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.ANTIALIAS)

            # Turn the image into a numpy array
            image_array = np.asarray(image)

            # Normalize the image
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

            # Load the image into the array
            data[0] = normalized_image_array

            # Run the inference
            prediction = model.predict(data)
            type_of_cloud = np.argsort(prediction, axis=1)[:, ::-1][0]
            cloud1 = type_of_cloud[0]
            cloud2 = type_of_cloud[1]

            # Write the variable's value to the file
            file.write(str(i) + ' ' + str(cloud1) + ' ' + str(cloud2) + '\n')