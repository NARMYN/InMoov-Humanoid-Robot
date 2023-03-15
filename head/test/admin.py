# Import necessary packages
import os
import cv2
import shutil
import numpy as np
import pandas as pd
from PIL import Image
from unicodedata import numeric


# Function to display program's title
def title():
    # Title of the program
    print("***********************************")
    print("****** NUST Robotics and AI *******")
    print("***********************************")


# Function to display main menu
def main_menu():
    title()
    print(10 * "-", "MAIN MENU", 10 * "-")
    print("[1] Check Camera")
    print("[2] View all members")
    print("[3] Add a member")
    print("[4] Remove a member")
    print("[5] Quit")

    while True:
        try:
            choice = int(input("Enter Choice: "))

            if choice == 1:
                check_camera()
                break
            elif choice == 2:
                view_members()
                break
            elif choice == 3:
                add_member()
                break
            elif choice == 4:
                remove_member()
                break
            elif choice == 5:
                print("Thank you")
                break
            else:
                print("Invalid Choice. Try Again")
                main_menu()
        except ValueError:
            print("Invalid Choice. Try Again")
    exit()


# Function to check camera
def check_camera():
    # Load the cascade
    face_detector = cv2.CascadeClassifier('data/facial_recognition/haarcascade_frontalface_default.xml')

    # To capture video from camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("There was an issue while opening the camera")

    while cap.isOpened():
        # Read the frame
        ret, img = cap.read()
        if ret:
            # Flips the original frame about y-axis
            img = cv2.flip(img, 1)

            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Detect the faces
            faces = face_detector.detectMultiScale(gray, 1.3, 5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

            # Draw the rectangle around each face
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (10, 159, 255), 2)

            # Display
            cv2.imshow('Camera Check', img)

            # Stop if escape key or 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    # Release the video capture object & destroy all windows
    cap.release()
    cv2.destroyAllWindows()
    key = input("Enter any key to return to main menu ")
    main_menu()


# Function to check if input is a valid number
def is_number(string: str):
    try:
        float(string)
        return True
    except ValueError:
        pass

    try:
        numeric(string)
        return True
    except (TypeError, ValueError):
        pass


# Function to return training images and labels
def imgs_and_labels(path: str):
    # Create empty list for faces
    faces = []
    # Create empty list for CMS IDs
    cms_ids = []
    # Obtain a list of directories & files available inside the path
    _, directories, _ = next(os.walk(path))
    for directory in directories:
        # Obtain a list of files available within the subdirectory
        _, _, files = next(os.walk(path + '/' + directory))
        # Loop through each file within the subdirectory
        for file in files:
            # Load the image and convert it to gray scale
            pill_img = Image.open(path + '/' + directory + '/' + file).convert('L')
            # Convert the PIL image into numpy array
            np_img = np.array(pill_img, 'uint8')
            # Get the CMS ID
            cms_id = int(directory.split("_")[-1])
            # Append the face to faces list
            faces.append(np_img)
            # Append the cms_id to CMS ids list
            cms_ids.append(cms_id)
    return faces, cms_ids


# Function to view all members
def view_members():
    if os.path.isfile("data/facial_recognition/member_details.csv"):
        member_details = pd.read_csv("data/facial_recognition/member_details.csv")
        if not member_details.empty:
            print(member_details)
        else:
            print("No members have been added yet.")
    else:
        print("No members have been added yet.")

    key = input("Enter any key to return ")
    main_menu()


# Function to add a member
def add_member():
    cms_id = input("CMS ID: ")
    while not is_number(cms_id):
        print("Please enter valid CMS ID")
        cms_id = input("CMS ID: ")

    name = input("Name: ")

    print("Capturing the face...")
    # Make a folder for the member if it doesnot exist
    member = name.replace(" ", "_") + "_" + cms_id
    if not os.path.isdir("data/facial_recognition/faces/" + member):
        os.mkdir("data/facial_recognition/faces/" + member)

    # Load the cascade
    face_detector = cv2.CascadeClassifier("data/facial_recognition/haarcascade_frontalface_default.xml")

    # To capture video from camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("There was an issue while opening the camera")

    sample_num = 0

    while cap.isOpened():
        # Read the frame
        ret, img = cap.read()
        if ret:
            # Flips the original frame about y-axis
            img = cv2.flip(img, 1)

            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Detect the faces
            faces = face_detector.detectMultiScale(gray, 1.3, 5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

            for (x, y, w, h) in faces:
                # Increment the sample number
                sample_num += 1
                # Draw the rectangle around the face
                cv2.rectangle(img, (x, y), (x + w, y + h), (10, 159, 255), 2)
                # Save the captured face
                cv2.imwrite("data/facial_recognition/faces/" + member + "/" +
                            str(sample_num) + ".jpg", gray[y:y + h, x:x + w])
                # Display the frame
                cv2.imshow(member, img)

            # Stop after 100 milliseconds or if 'q' is pressed
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # Exit if the number of samples is greater or equal to 100
            elif sample_num >= 100:
                break
        else:
            break
    # Release the video capture object & destroy all windows
    cap.release()
    cv2.destroyAllWindows()

    # Save the member details
    if os.path.isfile("data/facial_recognition/member_details.csv"):
        member_details = pd.read_csv("data/facial_recognition/member_details.csv")
        member_details = pd.concat([member_details, pd.DataFrame({'CMS ID': [cms_id], 'Name': [name]})],
                                    ignore_index=True,
                                    axis=0)
        member_details.drop_duplicates(subset=['CMS ID'], inplace=True)
        member_details.to_csv('data/facial_recognition/member_details.csv', index=False)
    else:
        member_details = pd.DataFrame(data={'CMS ID': [cms_id], 'Name': [name]})
        member_details.to_csv('data/facial_recognition/member_details.csv', index=False)

    print("Training the model")
    # Train on the images & save the model
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    faces, cms_ids = imgs_and_labels("data/facial_recognition/faces")
    recognizer.train(faces, np.array(cms_ids))
    recognizer.save("data/facial_recognition/model.yml")

    print("Member Added!")
    key = input("Enter any key to return ")
    main_menu()


# Function to remove a member
def remove_member():
    print("Enter CMS ID of the member to be removed")
    cms_id = input("CMS ID: ")
    while not is_number(cms_id):
        print("Please enter valid CMS ID \n")
        cms_id = input("CMS ID: ")
    # Read the member details
    members = pd.read_csv("data/facial_recognition/member_details.csv")
    # If the member exists
    if not members[members['CMS ID'] == int(cms_id)].empty:
        # Get the member's name
        name = members.loc[members['CMS ID'] == int(cms_id)]['Name'].values[0]

        # Remove member's data from member_details.csv
        members.drop(index=members[members["CMS ID"] == int(cms_id)].index, inplace=True)
        members.to_csv("data/facial_recognition/member_details.csv", index=False)

        # Remove member's pictures
        try:
            shutil.rmtree("data/facial_recognition/faces/" + name.replace(" ", "_") + "_" + cms_id)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

        # Retrain the model
        faces, cms_ids = imgs_and_labels("data/facial_recognition/faces")
        if len(faces) != 0 and len(cms_ids) != 0:
            recognizer = cv2.face_LBPHFaceRecognizer.create()
            recognizer.train(faces, np.array(cms_ids))
            recognizer.save("data/facial_recognition/model.yml")

        print("Member Removed!")
    else:
        print("Member not found")

    key = input("Enter any key to return ")
    main_menu()


if __name__ == "__main__":
    main_menu()
