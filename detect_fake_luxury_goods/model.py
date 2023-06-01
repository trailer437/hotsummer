import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Set the paths to your labeled dataset
train_dir = 'path_to_train_dataset'
valid_dir = 'path_to_validation_dataset'
test_dir = 'path_to_test_dataset'

# Set the parameters for data preprocessing and augmentation
batch_size = 32
image_size = (224, 224)  # Adjust according to your input size requirements

# Create data generators for training, validation, and testing
train_datagen = ImageDataGenerator(
    rescale=1./255,  # Normalize pixel values to the range [0, 1]
    rotation_range=20,  # Randomly rotate images
    width_shift_range=0.2,  # Randomly shift images horizontally
    height_shift_range=0.2,  # Randomly shift images vertically
    horizontal_flip=True,  # Randomly flip images horizontally
    validation_split=0.2  # Split the training data for validation
)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='binary',
    subset='training'  # Use a subset of the training data
)

valid_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='binary',
    subset='validation'  # Use a subset of the training data for validation
)

test_datagen = ImageDataGenerator(rescale=1./255)  # Only rescale pixel values for testing

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='binary'
)

# Define the model architecture
model = tf.keras.models.Sequential([
    tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet'),
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Set the number of training and validation steps per epoch
train_steps = train_generator.samples // batch_size
valid_steps = valid_generator.samples // batch_size

# Train the model
model.fit(
    train_generator,
    steps_per_epoch=train_steps,
    validation_data=valid_generator,
    validation_steps=valid_steps,
    epochs=10  # Adjust the number of epochs based on your dataset size and convergence
)

# Evaluate the model on the test set
test_loss, test_accuracy = model.evaluate(test_generator, steps=len(test_generator))
print('Test Loss:', test_loss)
print('Test Accuracy:', test_accuracy)

# Save the trained model for later use
model.save('fake_goods_detection_model.h5')
