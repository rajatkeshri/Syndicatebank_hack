import os
import face_recognition
import cv2

def facialrecognition(input_image,folder_to_compare):
    
    images = os.listdir(folder_to_compare)
    image_to_be_matched = cv2.imread(input_image)
    if len(face_recognition.face_encodings(image_to_be_matched))!=0:
        image_to_be_matched_encoded = face_recognition.face_encodings(image_to_be_matched)[0]
    else:
        return("face not detected")

    x=""
    # iterate over each image
    for i in images:
        temp=os.listdir(folder_to_compare+"/"+i)
        number=len(temp)
        count=0
        
        for j in temp:
            current_image = face_recognition.load_image_file(folder_to_compare+"/" + i+"/"+j)
            current_image_encoded = face_recognition.face_encodings(current_image)[0]
            result = face_recognition.compare_faces([image_to_be_matched_encoded], current_image_encoded)
            if result[0] == True:
                count+=1

        if count==number:
            return(i)
        
    return("none")


input_image="iron_1.jpeg" 
folder_to_compare='image_to_compare'
facialrecognition(input_image,folder_to_compare)
