print("Testing Tensorflow Validity", flush = True)
import tensorflow as tf

print("[TensorFlow] version:", tf.__version__)
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
print(tf.config.list_physical_devices('GPU'))