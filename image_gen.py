import cv2
import os, random
import numpy as np
import pandas as pd
import tensorflow as tf

# Input data generator
def labels_to_text(labels):     
    return ''.join(list(map(lambda x: letters[int(x)], labels)))

def text_to_labels(text):     
    return list(map(lambda x: letters.index(x) if x in letters else 0, text))

class TextImageGenerator:
    def __init__(self, img_dirpath, img_w, img_h,
                 batch_size, max_text_len, max_data_size, chunk_size):
      
        self.img_h = img_h
        self.img_w = img_w
        self.batch_size = batch_size
        self.max_text_len = max_text_len
        self.max_data_size = max_data_size
        self.img_dirpath = img_dirpath
        self.chunk_size = chunk_size
        self.data_points = 0
        self.cur_index = 0
        self.texts = []

        for df in pd.read_csv('{0}.csv'.format(self.img_dirpath),chunksize=chunk_size, iterator=True):
          print(f'processing rows: {self.data_points} : {self.data_points + chunk_size}' )
          if self.data_points == self.max_data_size:
            break
          for row in df.iterrows():
            self.data_points += 1

        print('done')

        self.imgs = np.zeros((self.data_points, self.img_h, self.img_w))

    def build_data(self):
        ''' formats the self fields into image data with labels '''    

        print('started building data')
        for chunk, df in enumerate(pd.read_csv('{0}.csv'.format(self.img_dirpath),chunksize=self.chunk_size, iterator=True)): # read in chunks
          if (chunk * self.chunk_size) == self.data_points:
            break
          print(f'processing rows: {self.chunk_size * chunk} : {self.chunk_size * (chunk + 1)}' )
          for row in df.iterrows():
            path = "./{0}/{1}".format(self.img_dirpath, row[1][0])
            try:
              img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
              img = cv2.resize(img, (self.img_w, self.img_h))
              img = img.astype(np.float32)
              img = (img / 255.0) * 2.0 - 1.0
              self.imgs[row[0], :, :] = img
              self.texts.append(row[1][1])
            except:
              continue 
        
        self.indexes = list(range(self.data_points))
          
    def next_sample(self):     
        self.cur_index += 1
        if self.cur_index >= self.data_points:
            self.cur_index = 0
            random.shuffle(self.indexes)
        return self.imgs[self.indexes[self.cur_index]], self.texts[self.indexes[self.cur_index]]

    
    def next_batch(self):   
        while True:
            X_data = np.ones([self.batch_size, self.img_w, self.img_h, 1])    
            Y_data = np.ones([self.batch_size, self.max_text_len])             
            input_length = np.ones((self.batch_size, 1)) * ((self.img_w * self.img_h) // 32)  
            label_length = np.zeros((self.batch_size, 1))          

            for i in range(self.batch_size):
                img, text = self.next_sample()
                img = img.T
                img = np.expand_dims(img, -1)
                X_data[i] = img
                Y_data[i][0:len(text)] = text_to_labels(text)
                label_length[i] = len(text)

            inputs = {
                'the_input': tf.convert_to_tensor(X_data), 
                'the_labels': tf.convert_to_tensor(Y_data), 
                'input_length': tf.convert_to_tensor(input_length),  
                'label_length': tf.convert_to_tensor(label_length)  
            }
            outputs = {'ctc': tf.convert_to_tensor(np.zeros([self.batch_size]))}   # (bs, 1) 
            yield (inputs, outputs)