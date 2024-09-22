import face_recognition
import cv2
import numpy as np
import os
import xlwt
from xlwt import Workbook
from datetime import date
import xlrd, xlwt
from xlutils.copy import copy as xl_copy

CurrentFolder = os.getcwd() #Read current folder path
image = CurrentFolder+'\\shreyas.png'
image2 = CurrentFolder+'\\sonu.png'
#image3 = CurrentFolder+'\\teju.png'
#image4 = CurrentFolder+'\\sreedhar.png'


video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
person1_name = "x" #add name 
person1_image = face_recognition.load_image_file(image) # add the Image of the student
person1_face_encoding = face_recognition.face_encodings(person1_image)[0]


person2_name = "y" #add name 
person2_image = face_recognition.load_image_file(image2)# add the Image of the student
person2_face_encoding = face_recognition.face_encodings(person2_image)[0]

person3_name = "z" #add name 
person3_image = face_recognition.load_image_file(image3)
person3_face_encoding = face_recognition.face_encodings(person3_image)[0]# add the Image of the student

person4_name = "w" #add name 
person4_image = face_recognition.load_image_file(image4)
person4_face_encoding = face_recognition.face_encodings(person4_image)[0]# add the Image of the student

known_face_encodings = [
    person1_face_encoding,
    person2_face_encoding,
    #person3_face_encoding,
    #person4_face_encoding
]
known_face_names = [
    person1_name,
    person2_name,
    #person3_name,
    #person4_name
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

rb = xlrd.open_workbook('attendence_excel.xls', formatting_info=True) 
wb = xl_copy(rb)
inp = input('Please give current subject lecture name')
sheet1 = wb.add_sheet(inp)
sheet1.write(0, 0, 'Name/Date')
sheet1.write(0, 1, str(date.today()))
row=1
col=0
already_attendence_taken = ""
while True:
            ret, frame = video_capture.read()

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            rgb_small_frame = small_frame[:, :, ::-1]

            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)
                    if((already_attendence_taken != name) and (name != "Unknown")):
                     sheet1.write(row, col, name )
                     col =col+1
                     sheet1.write(row, col, "Present" )
                     row = row+1
                     col = 0
                     print("attendence taken")
                     wb.save('attendence_excel.xls')
                     already_attendence_taken = name
                    else:
                     print("next student")
                        
            process_this_frame = not process_this_frame


            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
               
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xff==ord('q'):   
                print("data save")
                break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
