import os
import pandas as pd
import Image
from PIL import ImageFilter
from pytesseract import image_to_string

# process based on tesseract
data = []
for fle in os.listdir('./test'):
    try:
        data.append([fle, image_to_string(Image.open("/home/cjv/Documents/relatix.io/test/{0}".format(fle)).convert('LA'))])
    except:
        continue

# remove all bad characters
for line in data:
    line[1] = ''.join(list(filter(lambda char: char.isdigit() or char.isalpha() or char in ['\n',' '], line[1])))

# remove all short
data = list(filter(lambda line: len(line[1]) > 20 ,data))

df = pd.DataFrame(data, columns=["files", "text"])
df.to_csv("test.csv",index=False, encoding ='utf-8')