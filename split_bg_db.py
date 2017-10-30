from PIL import Image
import numpy as np
import os
import random

#os.rename("test/bg/1.jpg", "test2/bg")

bg_db = os.listdir('MERGED_BACKGROUND/')
for i in range(10):
    bg_pic = random.shuffle(bg_db)
    print(bg_pic)