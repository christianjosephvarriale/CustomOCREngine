# CRNN Neural Network 

### description
Extracts text from text conversations adapted from techniques outlined by [CRNN (CNN+RNN) for OCR using Keras / License Plate Recognition](https://github.com/qjadud1994/CRNN-Keras)

### files
1. `model.py` contains the model definition consisting of primarily Convolutional and Recurrent layers with a CTC loss function
2. `scrape_images.py` runs a selenium browser automation script to extract the highest quality available images from any query of choice
3. `image_gen.py` custom image generator which stores all the data in a `panadas` dataframe
4. `draw_bounding_box.py` allows a user to draw bounding boxes around text and see what the Tesseract OCR engine has extracted
if you'd like to use realistic data
5. `build_labels.py` extracts text from images using a brute force Tesseract approach
