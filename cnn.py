# Importing libraries 
import matplotlib.pyplot as plt 
import tensorflow as tf 
import keras

from pathlib import Path

# Count total images in all sets
image_count = len(list(Path("new-data/train/").glob('*/*'))) + \
              len(list(Path("new-data/validation/").glob('*/*')))
print(image_count) 

# Training dataset
train_ds = keras.utils.image_dataset_from_directory( 
    Path("new-data/train/"), 
    seed=123, 
    image_size=(180, 180), 
    batch_size=32) 

# Validation dataset
val_ds = keras.utils.image_dataset_from_directory( 
    Path("new-data/validation/"), 
    seed=123, 
    image_size=(180,180), 
    batch_size=32)

class_names = train_ds.class_names 
print(class_names)

num_classes = len(class_names) 

model = keras.models.Sequential([ 
    keras.layers.Rescaling(1./255), 
    keras.layers.Conv2D(16, 3, padding='same', activation='relu'), 
    keras.layers.MaxPooling2D(), 
    keras.layers.Conv2D(32, 3, padding='same', activation='relu'), 
    keras.layers.MaxPooling2D(), 
    keras.layers.Conv2D(64, 3, padding='same', activation='relu'), 
    keras.layers.MaxPooling2D(), 
    keras.layers.Flatten(), 
    keras.layers.Dense(128, activation='relu'), 
    keras.layers.Dense(num_classes) 
]) 

model.compile(optimizer='adam', 
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), 
              metrics=['accuracy']) 

epochs = 25
history = model.fit( 
  train_ds, 
  validation_data=val_ds,
  epochs=epochs 
) 

# Accuracy 
acc = history.history['accuracy'] 
val_acc = history.history['val_accuracy'] 

# Loss 
loss = history.history['loss'] 
val_loss = history.history['val_loss'] 

model.save("models/model.keras")