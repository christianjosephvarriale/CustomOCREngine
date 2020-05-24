from tensorflow.keras import Input, Model
from tensorflow.keras.backend import ctc_batch_cost
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Reshape, Lambda, BatchNormalization, Bidirectional, LSTM

def ctc_lambda_func(args):
    y_pred, labels, input_length, label_length = args
    print(y_pred, labels, input_length, label_length)
    return ctc_batch_cost(labels, y_pred, input_length, label_length)

def prepare_model(training):
    ''' create the model '''

    input_shape = (img_w, img_h, 1)

    # The inputs
    labels = Input(name='the_labels', shape=[max_text_len], dtype='float32')
    input_length = Input(name='input_length', shape=[1], dtype='int64')
    label_length = Input(name='label_length', shape=[1], dtype='int64')
    inputs = Input(name='the_input', shape=input_shape, dtype='float32') 

    # Convolution layer (VGG)
    inner = Conv2D(16, (3, 3), activation='relu', padding='same', name='conv1', kernel_initializer='he_normal')(inputs)  # (None, 128, 64, 64)
    inner = BatchNormalization()(inner)
    inner = MaxPooling2D(pool_size=(2, 2), name='max1')(inner)

    inner = Conv2D(32, (3, 3), activation='relu', padding='same', name='conv2', kernel_initializer='he_normal')(inner)  # (None, 64, 32, 128)
    inner = BatchNormalization()(inner)
    inner = MaxPooling2D(pool_size=(2, 2), name='max2')(inner)

    inner = Conv2D(64, (3, 3), activation='relu', padding='same', name='conv3', kernel_initializer='he_normal')(inner)  # (None, 64, 32, 128)
    inner = BatchNormalization()(inner)

    inner = Conv2D(128, (3, 3), activation='relu', padding='same', name='conv4', kernel_initializer='he_normal')(inner)  # (None, 64, 32, 128)
    inner = BatchNormalization()(inner)
    

    inner = Conv2D(256, (3, 3), activation='relu', padding='same', name='conv5', kernel_initializer='he_normal')(inner)  # (None, 64, 32, 128)
    inner = BatchNormalization()(inner)

    # CNN to RNN
    inner = Reshape(target_shape=((1024, 512)), name='reshape')(inner)
    inner = Dense(512, activation='relu', kernel_initializer='he_normal', name='dense1')(inner)

    # RNN layer
    lstm_1 = Bidirectional(LSTM(256, return_sequences=True, kernel_initializer='he_normal', name='lstm1'))(inner)
    lstm_1 = BatchNormalization()(lstm_1)

    # RNN layer
    lstm_2 = Bidirectional(LSTM(256, return_sequences=True, kernel_initializer='he_normal', name='lstm2'))(lstm_1)
    lstm_2 = BatchNormalization()(lstm_2)

    # transforms RNN output to character activations:
    y_pred = Dense(num_classes, activation='softmax', kernel_initializer='he_normal',name='dense2')(lstm_2) 

    # Keras doesn't currently support loss funcs with extra parameters
    # so CTC loss is implemented in a lambda layer
    loss_out = Lambda(ctc_lambda_func, output_shape=(1,), name='ctc')([y_pred, labels, input_length, label_length]) 

    if training:
        return Model(inputs=[inputs, labels, input_length, label_length], outputs=loss_out)
    else:
        return Model(inputs=[inputs], outputs=y_pred)