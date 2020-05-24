CHAR_VECTOR = ".?,':abcdefghijklnmopqrstuvwxyzABCDEFGHIJKLNMOPQRSTUVWXYZ0123456789\n"

letters = [letter for letter in CHAR_VECTOR]

num_classes = len(letters) + 1

# change these
img_w, img_h = 128, 256

# Network parameters
batch_size = 64
val_batch_size = 32
max_train_data_size = 50000
max_test_data_size = 5000
train_chunk_size = 10000
test_chunk_size = 1000
max_text_len = 512