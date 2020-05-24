from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# # Model description and training
model = prepare_model(training=True)

try:
    model.load_weights('LSTM+BN4--26--0.011.hdf5')
    print("...Previous weight data...")
except:
    print("...New weight data...")
    pass

train_file_path = 'train'
train_set = TextImageGenerator(train_file_path, img_w, img_h, batch_size, max_text_len, max_train_data_size, train_chunk_size)
train_set.build_data()

valid_file_path = 'test'
test_set = TextImageGenerator(valid_file_path, img_w, img_h, val_batch_size, max_text_len, max_test_data_size, test_chunk_size)
test_set.build_data()

# early_stop = EarlyStopping(monitor='loss', min_delta=0.001, patience=4, mode='min', verbose=0)
checkpoint = ModelCheckpoint(filepath='LSTM+BN5--{epoch:02d}--{val_loss:.3f}.hdf5', monitor='loss', verbose=0, mode='min', period=1)

model.compile(loss={'ctc': lambda y_true, y_pred: y_pred}, optimizer="Adadelta")

model.summary()

# captures output of softmax so we can decode the output during visualization
model.fit(  x=train_set.next_batch(),
            steps_per_epoch=int(train_set.data_points / batch_size),
            validation_data=test_set.next_batch(),
            epochs=30,
            callbacks=[checkpoint],
            validation_steps=int(test_set.data_points / val_batch_size)
        )