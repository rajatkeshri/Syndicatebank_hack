import cv2
import numpy as np
import pytesseract
from PIL import Image
from pytesseract import image_to_string
import os.path
import json
import os
import re
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')
import hashlib 

#extract names,number,email using nlp from a given text

def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]
#------------------------------------------------------------------------------------------------------
def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)
#------------------------------------------------------------------------------------------------------
def ie_preprocess(document):
    document = ' '.join([i for i in document.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences
#------------------------------------------------------------------------------------------------------
def extract_names(document):
    names = []
    sentences = ie_preprocess(document)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    return names

#------------------------------------------------------------------------------------------------------
def get_string(img_path):
    
    # Read image with opencv
    img = cv2.imread(img_path)
    #cv2.imshow("b",img)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Write image after removed noise
    cv2.imwrite("removed_noise.jpeg", img)

    #  Apply threshold to get image with only black and white
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    cv2.imwrite("thres.jpeg", img)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open("removed_noise.jpeg"))

    return result
#------------------------------------------------------------------------------------------------------

def extractdata(imagename):
    # Path of working folder on Disk
    #imagename="6.jpg"
    result= (get_string(imagename) )

    s=""
    x=[]
    for i in result:

        if i!="\n":
            s=s+i
        else:
            if s!='':
                x.append(s)
            s=""
    x.append(s)
    #print(x)


    # Initializing data variable
    names = None
    gender = None
    dob = None
    uid = None

    #----------------------------------------------------------------------------------------------
    
    #EXTRACTING NAMES USING NLP
    names = extract_names(result)
    names=str(names[0])
    #print(names)

    #find gender
    for i in x:
        temp_i=i.upper()
        if temp_i.find("FEMALE")>0 :#or i.find("EMALE")>0: 
            gender = "Female"
        elif temp_i.find("MALE")>0 :#or i.find("ALE")>0:
            gender = "Male"
    #print(gender)

    #find dob
    for i in x:
        temp=""
        temp_i=i.upper()
        if temp_i.find("DOB")>0 :
            index=temp_i.find("DOB") 
            for j in range(index+4,len(i)):
                temp=temp+str(i[j])
            dob=temp

        elif i.find("Year of Birth")>0:
            index=i.find("Year of Birth") 
            for j in range(index+16,len(i)):
                temp=temp+str(i[j])
            dob=temp
    #print(dob)

    #find uid
    for i in x:
        temp=""
        count=0
        for j in i:
            if j.isnumeric():
                temp=temp+str(j)
                count+=1
                if count==12:
                    break
        if count==12:
            uid=temp
            break
    #print(uid)

    #----------------------------------------------------------------------------------------------------
    # Making tuples of data
    data = {}
    data['Name'] = names
    data['Gender'] = gender
    data['DOB'] = dob
    data['Uid'] = uid
    
    #with open(os.path.basename(imagename).split('.')[0] +'.json', 'w') as fp:
    #    json.dump(data, fp)
    
    return(data)
#--------------------------------------------------------------------------


#def checkaadharnumber(x):
    
name_d={}

def newuser(count,image_path):
    
    name=input("enter name")
    gender=input("enter gender")
    dob=input("enter dob/year of birth")
    
    
    #name="Akshay Madhukar Deshmukh"
    #gender="Male"
    #dob="1992"
    
    data_entered={}
    data_entered["Name"]=name
    data_entered["Gender"]=gender
    data_entered["DOB"]=dob
    datastring=""

    #######################################################
    data_aadhar=extractdata(image_path)
    #print(data_aadhar)
    
    #checking if entered data matches with aadhar data
    for i in data_aadhar:
        if i in data_entered:
            if data_aadhar[i].lower()!=data_entered[i].lower():
                #print(data_aadhar[i],data_entered[i])
                print("invalid details")
                return(count)
    
    aadharnumber=data_aadhar["Uid"]
    
    ######################################################3
    
    jsonpath="C:/Anaconda codes/blockchain/json files"
    
    l=len(os.listdir(jsonpath))
    
    #CREATING THE BLOCKCHAIN
    if l==0:
        #IF THIS IS FIRST USER IN THE CHAIN
        f=open("temp.txt","w+")
        
        hashf=0
        hashf=str(hashf)
        data_entered["Hash"]=hashf
        
        fp=open(jsonpath+"/"+str(count)+name+".json","w+")
        json.dump(data_entered, fp)
        
        
        #SHA256 ALGO
        for i in data_entered:
            datastring=datastring+data_entered[i]
        
        result = hashlib.sha256(datastring.encode()) 
        result=result.hexdigest()
        result=str(result)
        
        f.write(result)
        f.close()
        datastring=""
        
        print("initial hash",hashf)
        print("calculated hash for "+str(count)+" "+name+" "+result)
    
    else:    
        
        #READING PREVIOUS HASH VALUE
        f=open("temp.txt","r+")
        x=f.read()
        f.close()
        
        hashf=str(x)
        data_entered["Hash"]=hashf
        fp=open(jsonpath+"/"+str(count)+name+".json","w+")
        json.dump(data_entered, fp)
        
        #SHA256 ALGO
        for i in data_entered:
            datastring=datastring+data_entered[i]
        #print(datastring)
        
        result = hashlib.sha256(datastring.encode()) 
        result=result.hexdigest()
        result=str(result)
        #print(result)
        
        f=open("temp.txt","w")
        f.write(result)
        f.close()
        
        print("calculated hash for "+str(count)+" "+name+" "+result)
        

    
    #hash map for mapping names to the json files for the users
    #using this hash map, the json files will be accessed by facial/voice recogntion
    name_d[name]=str(count)+name
    
    count+=1
    return count
#---------------------------------------------------


usercount=0

image_path="6.jpg" #aadhar card image
usercount=newuser(usercount,image_path)

image_path="4.jpg" #aadhar card image
usercount=newuser(usercount,image_path)

print("\n",name_d)
