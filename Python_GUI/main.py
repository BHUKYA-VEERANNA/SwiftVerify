import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QLabel
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtMultimedia import QSound
from PyQt5.QtGui import QMovie
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage
import mysql.connector
import os
import barcode, pyttsx3
import cv2
from pyzbar.pyzbar import decode
from barcode.writer import ImageWriter
import pandas as pd
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QTimer
from datetime import datetime, timedelta

class HomePage(QMainWindow):
    def __init__(self):
        super(HomePage, self).__init__()
        loadUi('C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/Python_GUI/UI_Files/home.ui', self)
        #C:\Users\bveer\Dropbox\4-2 B.Tech\Major Project\Code\Python_GUI\UI_Files
        # Connect button clicks to actions
        self.pushButton_3.clicked.connect(self.openLogin)
        self.pushButton_4.clicked.connect(self.openSignup)
        self.pushButton_2.clicked.connect(self.close)
        self.pushButton.clicked.connect(self.markAttedance)

    def openLogin(self):
        # Close the current frame
        self.hide()
        
        login_page = LoginPage(self)
        login_page.show()

    def openSignup(self):
        # Close the current frame
        self.hide()
        
        signup_page = SignupPage(self)
        signup_page.show()

    def markAttedance(self):
        self.hide()
        mark_Attedance=markAttedance(self)
        mark_Attedance.show()

class LoginPage(QDialog):
    def __init__(self, parent=None):
        super(LoginPage, self).__init__(parent)
        loadUi('C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/Python_GUI/UI_Files/login.ui', self)

        # Connect back button click to action
        self.pushButton_2.clicked.connect(self.goBack)

        # Connect login button click to action
        self.pushButton.clicked.connect(self.loginUser)

    def goBack(self):
        # Show the previous frame
        self.parent().show()
        self.close()

    def loginUser(self):
        # Get user input from the form
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        # Check if any field is empty
        if not username or not password:
            QMessageBox.warning(self, 'Warning', 'All fields must be filled!')
            return

        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(
                host="localhost",  # Replace with your database host
                user="root",       # Replace with your database username
                password="",       # Replace with your database password
                database="faculty registration"  # Replace with your database name
            )

            # Create a cursor object
            cursor = conn.cursor()

            # Check if the entered credentials are valid
            cursor.execute('SELECT * FROM `log db` WHERE Username=%s AND password=%s', (username, password))
            result = cursor.fetchone()

            if result:
                # Valid credentials
                #QMessageBox.information(self, 'Success', 'Login successful!')
                # Open the dashboard page upon successful login
                self.hide()
                dashboard_page = DashboardPage(self)
                dashboard_page.show()
            else:
                # Invalid credentials
                QMessageBox.warning(self, 'Warning', 'Invalid username or password!')

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error: {str(e)}')

        finally:
            conn.close()

class SignupPage(QDialog):
    def __init__(self, parent=None):
        super(SignupPage, self).__init__(parent)
        loadUi('C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/Python_GUI/UI_Files/signup.ui', self)

        # Connect back button click to action
        self.pushButton_2.clicked.connect(self.goBack)

        # Connect toolButton click to open login.ui
        self.toolButton.clicked.connect(self.openLogin)

        # Connect register button click to action
        self.pushButton_6.clicked.connect(self.registerUser)

    def goBack(self):
        # Show the previous frame (HomePage)
        self.parent().show()
        self.close()

    def openLogin(self):
        # Hide the current frame (SignupPage)
        self.hide()

        # Create and show the login page
        login_page = LoginPage(self)
        login_page.show()

    def registerUser(self):
        # Get user input from the form
        name = self.lineEdit_4.text()
        username = self.lineEdit_5.text()
        email = self.lineEdit_3.text()
        password = self.lineEdit_6.text()
        confirm_password = self.lineEdit_7.text()

        # Check if any field is empty
        if not name or not username or not email or not password or not confirm_password:
            QMessageBox.warning(self, 'Warning', 'All fields must be filled!')
            return

        # Check password strength
        if (
            len(password) < 6
            or not any(char.isalpha() for char in password)
            or not any(char.isdigit() for char in password)
            or not any(char.isalnum() for char in password)
        ):
            QMessageBox.warning(
                self,
                'Warning',
                'Password must be a combination of letters, numbers, and special characters with a minimum length of 6.',
            )
            return

        # Check if password and confirm_password match
        if password != confirm_password:
            QMessageBox.warning(self, 'Warning', 'Password and Confirm Password do not match!')
            return

        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="faculty registration"
            )

            # Create a cursor object
            cursor = conn.cursor()

            # Check if the username already exists
            cursor.execute('SELECT * FROM `log db` WHERE Username=%s', (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                # Username already exists, show warning
                QMessageBox.warning(self, 'Warning', 'User already exists. Please Login.')
            else:
                # Insert user data into the database
                cursor.execute('INSERT INTO `log db` (Fullname, Username, Email, password) VALUES (%s, %s, %s, %s)',
                               (name, username, email, password))
                conn.commit()
                self.hide()
                # Show the SignupSuccessfulPage
                signup_successful_page = SuccessfulPage(self)
                signup_successful_page.show()

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error: {str(e)}')

        finally:
            conn.close()

class SuccessfulPage(QDialog):
    def __init__(self, parent=None):
        super(SuccessfulPage, self).__init__(parent)
        loadUi('C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/Python_GUI/UI_Files/success.ui', self)

        # Load and play the GIF in the QLabel
        self.gifLabel = self.findChild(QLabel, 'label')  # Replace 'gifLabel' with the actual object name
        if self.gifLabel:
            self.playGif("C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/Python_GUI/Icons/success.gif")  # Replace with the actual path to your GIF file
            #
        # Connect pushButton click to open LoginPage
        self.pushButton.clicked.connect(self.openLoginPage)

    def playGif(self, gif_path):
        movie = QMovie(gif_path)
        self.gifLabel.setMovie(movie)
        movie.start()

    def openLoginPage(self):
        # Hide the current frame (SignupSuccessfulPage)
        self.hide()

        # Show the LoginPage
        login_page = LoginPage(self.parent())
        login_page.show() 

class markAttedance(QMainWindow):
    def __init__(self, parent=None):
        super(markAttedance, self).__init__(parent)
        loadUi('C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/Python_GUI/UI_Files/mark_attedance.ui', self)

        # Connect back button click to action
        self.pushButton_2.clicked.connect(self.goBack)

        # Create a QTimer to capture frames periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.captureBarcode)
        self.timer.start(100)  # Set the interval in milliseconds

        # Initialize camera
        self.capture = cv2.VideoCapture(0)  # Change the camera index if needed

        # Create attendance database and table if not exists
        self.createAttendanceDatabase()

        # QLabel to display camera feed
        self.label_camera = self.findChild(QLabel, 'label')  

        # QLabel to display attendance status
        self.label_status = self.findChild(QLabel, 'label_2')


    def goBack(self):
        # Stop the timer and release the camera when going back
        self.timer.stop()
        self.capture.release()
        # Show the previous frame (HomePage)
        self.parent().show()
        self.close()

    def createAttendanceDatabase(self):
        try:
            # Connect to MySQL server
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password=""
            )

            # Create a cursor object
            cursor = conn.cursor()

            # Create the attendance_information database if it does not exist
            cursor.execute('CREATE DATABASE IF NOT EXISTS attendance_information')

            # Use the attendance_information database
            cursor.execute('USE attendance_information')

            # Create the attendance table if it does not exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                                Name VARCHAR(255),
                                RollNumber VARCHAR(50),
                                Time TIME
                            )''')

            conn.commit()

        except Exception as e:
            print(f'Error: {str(e)}')

        finally:
            conn.close()

    def captureBarcode(self):
        ret, frame = self.capture.read()
        if ret:
            # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Use pyzbar to decode barcodes
            barcodes = decode(gray)

            for barcode in barcodes:
                # Extract the data from the barcode
                barcode_data = barcode.data.decode('utf-8')
                #print(f"Detected Barcode: {barcode_data}")

                # Check the database for the student with the matching RollNumber
                student = self.checkStudent(barcode_data)

                if student:
                    # Mark attendance in the database
                    self.markAttendance(student)
                else:
                    self.label_status.setStyleSheet("QLabel { color: red; font-weight: bold; }")
                    self.label_status.setText(f'No existing data found with scanned barcode: {barcode_data}')
                    self.announce(f'No existing data found with scanned barcode')

            # Display the camera feed on the QLabel
            self.displayCameraFeed(frame)

    def displayCameraFeed(self, frame):
        # Convert the OpenCV frame to QImage
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Convert QImage to QPixmap
        pixmap = QPixmap.fromImage(q_image)

        # Update the QLabel with the QPixmap
        self.label_camera.setPixmap(pixmap)

    def checkStudent(self, roll_number):
        try:
            # Connect to MySQL server
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password=""
            )

            # Create a cursor object
            cursor = conn.cursor()

            # Use the students database
            cursor.execute('USE student_information')

            # Retrieve the student from the database based on RollNumber
            cursor.execute('SELECT * FROM students WHERE RollNumber=%s', (roll_number,))
            student = cursor.fetchone()

            return student

        except Exception as e:
            print(f'Error: {str(e)}')

        finally:
            conn.close()

    def markAttendance(self, student):
        try:
            # Connect to MySQL server
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password=""
            )

            # Create a cursor object
            cursor = conn.cursor()

            # Use the attendance database
            cursor.execute('USE attendance_information')

            # Check if the student has already been marked present in the last hour
            current_time = datetime.now().strftime('%H:%M:%S')
            last_hour = (datetime.now() - timedelta(hours=1)).strftime('%H:%M:%S')
            cursor.execute('SELECT * FROM attendance WHERE RollNumber=%s AND Time BETWEEN %s AND %s',
                           (student[1], last_hour, current_time))
            existing_attendance = cursor.fetchone()

            if not existing_attendance:
                # Insert attendance data into the database
                cursor.execute('INSERT INTO attendance (Name, RollNumber, Time) VALUES (%s, %s, %s)',
                               (student[0], student[1], current_time))
                conn.commit()
                
                # # Update the QLabel with the attendance status
                # self.label_status.setStyleSheet("QLabel { color: green; font-weight: bold; }")
                self.label_status.setText(f'Attendance marked for {student[0]} ({student[1]}) at {current_time}')
                self.announce(f"Attendance marked successfully for {student[0]} (at {current_time}")
                #print(f'Attendance marked for {student[0]} ({student[1]}) at {current_time}')

            else:
                # # Update the QLabel with the status if already marked
                # self.label_status.setStyleSheet("QLabel { color: red; font-weight: bold; }")
                self.label_status.setText(f'Marked attendance for {student[0]} ({student[1]}) at {current_time}')
                self.announce(f"Attendance marked successfully for {student[0]} ( at {current_time}")
                

        except Exception as e:
            print(f'Error: {str(e)}')

        finally:
            conn.close()
    
    def announce(self, message):
        # Speak the message using text-to-speech
        engine = pyttsx3.init()
        engine.say(message)
        engine.runAndWait()

        # Additionally, you can play a sound if needed
        if "success" in message.lower():
            QSound.play("success_sound.wav")  # Adjust the sound file path accordingly
        elif "error" in message.lower():
            QSound.play("error_sound.wav")


class DashboardPage(QMainWindow):
    def __init__(self, parent=None):
        super(DashboardPage, self).__init__(parent)
        loadUi('C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/Python_GUI/UI_Files/dashboard.ui', self)

        # Connect back button click to action
        self.pushButton.clicked.connect(self.addStudent)
        self.pushButton_2.clicked.connect(self.showStudents)
        self.pushButton_4.clicked.connect(self.goBack)
        self.pushButton_5.clicked.connect(self.close)

        # Connect the download button click to the downloadAttendance method in the __init__ function
        self.pushButton_3.clicked.connect(self.downloadAttendance)

    def addStudent(self):
        self.hide()
        add_Student=addStudent(self)
        add_Student.show()

    
    def goBack(self):
        # Show the previous frame (HomePage)
        self.parent().show()
        self.close()

    def showStudents(self):
        # Fetch student details from the database and display them in a table
        try:
            # Connect to MySQL server
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password=""
            )

            # Create a cursor object
            cursor = conn.cursor()

            # Use the students database
            cursor.execute('USE student_information')

            # Retrieve all students from the database
            cursor.execute('SELECT * FROM students')
            students = cursor.fetchall()

            # Assuming you have a QTableWidget named 'table_students' in your UI file
            table_students = self.findChild(QTableWidget, 'tableWidget')
            if table_students:
                # Set the column count and headers
                table_students.setColumnCount(4)
                table_students.setHorizontalHeaderLabels(["Name", "Roll Number", "Branch", "Phone Number"])

                # Set the row count based on the number of students
                table_students.setRowCount(len(students))

                # Populate the table with student details
                for row, student in enumerate(students):
                    for col, data in enumerate(student):
                        item = QTableWidgetItem(str(data))
                        table_students.setItem(row, col, item)

                # Resize the columns to content
                table_students.resizeColumnsToContents()
                # Set the horizontal header to stretch
                table_students.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error: {str(e)}')

        finally:
            conn.close()
    
    def downloadAttendance(self):
        try:
            # Fetch student details from the database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password=""
            )
            cursor = conn.cursor()
            cursor.execute('USE student_information')
            cursor.execute('SELECT * FROM students')
            students = cursor.fetchall()
            conn.close()

            # Create a DataFrame from the fetched data
            columns = ["Name", "Roll Number", "Branch", "Phone Number"]
            df_students = pd.DataFrame(students, columns=columns)

            # Specify the path where the file will be saved
            file_path = 'C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/Python_GUI/AttendanceDetails.xlsx'

            # Export the DataFrame to an Excel file
            df_students.to_excel(file_path, index=False)

            QMessageBox.information(self, 'Success', 'Student details exported successfully!')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error: {str(e)}')

    # Connect the download button click to the downloadAttendance method in the __init__ function
    #   self.pushButton_3.clicked.connect(self.downloadAttendance)

class addStudent(QDialog):
    def __init__(self, parent=None):
        super(addStudent, self).__init__(parent)
        loadUi('C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/Python_GUI/UI_Files/add_student.ui', self)
        
        # Connect back button click to action
        self.pushButton.clicked.connect(self.goBack)
        
        # Connect the toolButton click to the method for generating BarCode and adding student
        self.toolButton.clicked.connect(self.generateBarcodeAndAddStudent)

        self.toolButton_2.clicked.connect(self.openFaceDataset)

    def goBack(self):
        # Show the previous frame (HomePage)
        self.parent().show()
        self.close()

    def generateBarcodeAndAddStudent(self):
        # Get user input from the form
        name = self.lineEdit.text()
        roll_number = self.lineEdit_2.text()
        branch = self.lineEdit_3.text()
        phone_number = self.lineEdit_4.text()

        # Check if any field is empty
        if not name or not roll_number or not branch or not phone_number:
            QMessageBox.warning(self, 'Warning', 'All fields must be filled!')
            return

        conn = None  # Initialize conn to None

        try:
            # Connect to MySQL server without specifying a database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password=""
            )

            # Create a cursor object
            cursor = conn.cursor()

            # Create the students database if it does not exist
            cursor.execute('CREATE DATABASE IF NOT EXISTS student_information')
            cursor.execute('USE student_information')

            # Create the students table if it does not exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                                Name VARCHAR(255),
                                RollNumber VARCHAR(50),
                                Branch VARCHAR(50),
                                PhoneNumber VARCHAR(15)
                            )''')

            # Insert student data into the database
            cursor.execute('INSERT INTO students (Name, RollNumber, Branch, PhoneNumber) VALUES (%s, %s, %s, %s)',
                           (name, roll_number, branch, phone_number))
            conn.commit()

            # Generate barcode and save it
            ean = barcode.get('code128', roll_number, writer=ImageWriter())
            barcode_path = os.path.join('C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/Python_GUI/BarCode', f'{roll_number}.png')
            ean.save(barcode_path)

            QMessageBox.information(self, 'Success', 'Student added successfully!\nBarcode generated and saved.')

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error: {str(e)}')

        finally:
            # Close the connection only if it's not None
            if conn:
                conn.close()
                

    def openFaceDataset(self):
        # Create and show an instance of the Face_dataset frame
        self.hide()
        face_dataset_frame = FaceDatasetFrame(self)
        face_dataset_frame.show()

class FaceDatasetFrame(QDialog):
    def __init__(self, parent=None):
        super(FaceDatasetFrame, self).__init__(parent)
        loadUi('C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/Python_GUI/UI_Files/Face_dataset.ui', self)

        # Connect back button click to action
        self.pushButton_3.clicked.connect(self.goBack)

    def goBack(self):
        # Show the previous frame (addStudent)
        self.parent().show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    home_page = HomePage()
    home_page.show()
    sys.exit(app.exec_())
