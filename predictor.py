import numpy as np
import keras
from keras.preprocessing import image

# Load model once globally
model = keras.models.load_model("models/model.keras")

# Your known class names (keep in same order as training)
class_names = ['apple', 'banana', 'beetroot', 'bell pepper', 'cabbage',
               'capsicum', 'carrot', 'cauliflower', 'chilli pepper', 'corn', 'cucumber', 'eggplant', 'garlic',
               'ginger', 'grapes', 'jalapeno', 'kiwi', 'lemon',
               'lettuce', 'mango', 'onion', 'orange', 'paprika', 'pear', 'peas',
               'pineapple', 'pomegranate', 'potato', 'raddish', 'soy beans',
               'spinach', 'sweetcorn', 'sweetpotato', 'tomato', 'turnip', 'watermelon']

def predict_image(img_path):
    img = image.load_img(img_path, target_size=(180, 180))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    predicted_index = np.argmax(predictions)
    confidence = float(predictions[0][predicted_index])
    return class_names[predicted_index], confidence