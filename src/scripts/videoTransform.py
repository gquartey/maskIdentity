import numpy as np 
import cv2 as ocv
import os 
from scipy import spatial

def detectAndBlur(image):
    '''
    input: 
        image - numpy array
    output: 
        numpy array
    '''
    cwd = os.getcwd()
    face_cascade = ocv.CascadeClassifier(cwd + '/scripts/models/' + 'haarcascade_frontalface_default.xml')
    new_image = image.copy()

    # convert the image to grayscale for the detection of faces
    gray = ocv.cvtColor(image, ocv.COLOR_BGR2GRAY)
    # detects all the faces in the image
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # kernel we'll use for averaging pixel values 
    kernel = np.ones((50,50),np.float32)/2500
    # iterate for each face in faces
    for (x, y, w, h) in faces:
        # now we'll blur each face in the image
        new_image[y:y+h,x:x+w,:] = ocv.filter2D(new_image[y:y+h,x:x+w,:],-1,kernel)
        # cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    return new_image

def serverVideoTransform(videoFile,outputFile):
    cap = ocv.VideoCapture(videoFile)

    fps = cap.get(ocv.CAP_PROP_FPS)
    width  = cap.get(ocv.CAP_PROP_FRAME_WIDTH)  
    height = cap.get(ocv.CAP_PROP_FRAME_HEIGHT) 
    fourcc = ocv.VideoWriter_fourcc(*'XVID')
    out = ocv.VideoWriter(outputFile,fourcc, fps, (int(width),int(height)))

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            frame = detectAndBlur(frame)

            # write the flipped frame
            out.write(frame)
        else:
            break
    
    cap.release()
    out.release()