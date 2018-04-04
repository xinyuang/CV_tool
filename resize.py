
from PIL import Image
h = 448
foreground = Image.open('0.jpg')
foreground = foreground.resize((h,h),Image.ANTIALIAS)
foreground.save('smallestCLASS.jpg')


size = 299
pf = '/media/xigu/DensoML/combination_data/test_1000_per_class'
tf = '/media/xigu/DensoML/MDP_2018/1000_emo_test'
for class_folder in os.listdir(pf):
    tf_path = os.path.join(tf,class_folder)
    if not os.path.exists(tf_path):
        os.makedirs(tf_path)
    for img_file in os.listdir(os.path.join(pf,class_folder)):
        if img_file == '_face_position':
            continue
        img_path = os.path.join(pf,class_folder,img_file)
        print(img_path)
        img = cv2.imread(img_path)
        new_img = cv2.resize(img,(size,size))
        print(os.path.join(tf_path,img_file))
        cv2.imwrite(os.path.join(tf_path,img_file),new_img)
