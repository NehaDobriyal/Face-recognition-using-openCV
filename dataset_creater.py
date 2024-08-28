import cv2
import numpy as np
import sqlite3

faceDetect = cv2.CascadeClassifier("haarcascade_frontalface_default (2).xml")
cam = cv2.VideoCapture(0)

# Function to create the 'STUDENTS' table if it doesn't exist
def create_table():
    conn = sqlite3.connect("sqlite.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS STUDENTS
             (ID INT PRIMARY KEY     NOT NULL,
             NAME           TEXT    NOT NULL,
             AGE            INT     NOT NULL);''')
    conn.close()

# Function to insert or update values into the 'STUDENTS' table
def insert_or_update(Id, Name, age):
    conn = sqlite3.connect("sqlite.db")
    cursor = conn.execute("SELECT * FROM STUDENTS WHERE ID=?", (Id,))
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if isRecordExist == 1:
        conn.execute("UPDATE STUDENTS SET NAME=? WHERE ID=?", (Name, Id))
        conn.execute("UPDATE STUDENTS SET AGE=? WHERE ID=?", (age, Id))
    else:
        conn.execute("INSERT INTO STUDENTS (ID, NAME, AGE) VALUES (?, ?, ?)", (Id, Name, age))
    conn.commit()
    conn.close()

# Create the 'STUDENTS' table
create_table()

# Insert user-defined values into the 'STUDENTS' table
Id = input('Enter User Id : ')
Name = input('Enter User Name : ')
age = input('Enter User Age : ')
insert_or_update(Id, Name, age)

# Detect face in web camera coding
sampleNum = 0
while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        sampleNum += 1
        cv2.imwrite("dataset/user." + str(Id) + "." + str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.waitKey(100)
    cv2.imshow("Face", img)
    cv2.waitKey(1)
    if sampleNum > 20:
        break
cam.release()
cv2.destroyAllWindows()