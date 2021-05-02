#importing libraries
import cv2
import numpy as np
import os
from matplotlib import pyplot as plt    
import time
from gtts import gTTS
from gtts import gTTS

folder = r'C:\Users\raghu\OneDrive\Documents\RSIP project\saved_images\strip\\'

#function that captures the images asper the given time limit
def capturing_images(folder, value):
    cap = cv2.VideoCapture(0)
    i = 0 
    while(cap.isOpened()):
        ret, frame = cap.read()
        i += 1
        if(i<value):
            cv2.imwrite( folder + str(i) + '.jpg',frame)
        else:
            break

#time delay between images 
def delay(seconds):
    start = time.time()
    
    elapsed = 0
    while elapsed < seconds:
        elapsed = time.time() - start
        print(elapsed)
        time.sleep(1)  

#pre processing of images 
def loading_images(folder, images, keypoints, descriptors):
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        img = cv2.resize(img, (256,256))  # resizing images to 256*256*3 
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        #(thresh, img) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        sift = cv2.SIFT_create()
        kp, des = sift.detectAndCompute(img,None)  #keypoint detection
        keypoints.append(kp)
        descriptors.append(des)
        img=cv2.drawKeypoints(img,kp,  outImage = None)  # drawing the keypoints
        if img is not None:
            images.append(img)
    #return images



#defining the individual vertical segments of the map 
def individual_strip(images1, descript1, images, descriptors, matches, strip):
    img1 = images1
    des1 = descript1
    j=0
    strip.append(img1)
    for i in range(100):
        img2 = images[i]
        des2 = descriptors[i]
        bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
        matche = bf.match(des1,des2)
        matche = sorted(matche, key = lambda x:x.distance)
        no_of_matches = np.size(matche)
        #print(no_of_matches)
        matches.sort()
        matches.append(no_of_matches)
        if( j<=6):
            strip.append(images[i])
            j += 1
    matches.sort()
    print(matches)
    

if __name__ == "__main__":
    images_1 = []
    keypoints_1 = []
    descriptors_1 = []
    strip1 = []
    matches1 = []
    capturing_images(folder, 200)
    loading_images(folder, images_1, keypoints_1, descriptors_1)
    
    delay(5)
    
    #images_2 = []
    #keypoints_2 = []
    #descriptors_2 = []
    #strip2 = []
    #matches2 = []
    #capturing_images(folder, 200)
    #loading_images(folder, images_2, keypoints_2, descriptors_2)
    
    individual_strip(images_1[0], descriptors_1[0], images_1, descriptors_1, matches1, strip1)
    #individual_strip(images_2[0], descriptors_2[0], images_2, descriptors_2, matches2, strip2)



    final_img_1 = cv2.vconcat(strip1)
    #final_img_2 = cv2.vconcat(strip2)
    
    final_img_1 = cv2.resize(final_img_1,(256,1280))
    
    #final_img = cv2.hconcat(final_img_1, f,inal_img_2)
    #final_img = cv2.resize(final_img, (5000, 7000))
    #rows = 2
    #columns = 2

    
    plt.imshow( final_img_1)
    plt.show()

 




