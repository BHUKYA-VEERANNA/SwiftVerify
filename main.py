import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QLabel
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QMovie
from PyQt5.uic import loadUi
import mysql.connector
import os
import barcode
import cv2
from pyzbar.pyzbar import decode
from barcode.writer import ImageWriter
import pandas as pd
from PyQt5.QtWidgets import QFileDialog

class HomePage(QMainWindow):
    def __init__(self):
        super(HomePage, self).__init__()
        loadUi('C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/home.ui', self)

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
        loadUi('C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/login.ui', self)

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
        loadUi('C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/signup.ui', self)

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
        loadUi('C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/success.ui', self)

        # Load and play the GIF in the QLabel
        self.gifLabel = self.findChild(QLabel, 'label')  # Replace 'gifLabel' with the actual object name
        if self.gifLabel:
            self.playGif('C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/Icons/success.gif')  # Replace with the actual path to your GIF file

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
        loadUi('C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/mark_attedance.ui', self)    

        # Connect back button click to action
        self.pushButton_2.clicked.connect(self.goBack)
    
    def goBack(self):
        # Show the previous frame (HomePage)
        self.parent().show()
        self.close()


class DashboardPage(QMainWindow):
    def __init__(self, parent=None):
        super(DashboardPage, self).__init__(parent)
        loadUi('C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/dashboard.ui', self)

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
                table_students.setColumnCount(5)
                table_students.setHorizontalHeaderLabels(["ID", "Name", "Roll Number", "Branch", "Phone Number"])

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
            columns = ["ID", "Name", "Roll Number", "Branch", "Phone Number"]
            df_students = pd.DataFrame(students, columns=columns)

            # Specify the path where the file will be saved
            file_path = 'C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/AttendanceDetails.xlsx'

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
        loadUi('C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/add_student.ui', self)
        
        # Connect back button click to action
        self.pushButton.clicked.connect(self.goBack)
        
        # Connect the toolButton click to the method for generating BarCode and adding student
        self.toolButton.clicked.connect(self.generateBarcodeAndAddStudent)

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
                                ID INT AUTO_INCREMENT PRIMARY KEY,
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
            barcode_path = os.path.join('C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/BarCode', f'{roll_number}.png')
            ean.save(barcode_path)

            QMessageBox.information(self, 'Success', 'Student added successfully!\nBarcode generated and saved.')

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error: {str(e)}')

        finally:
            # Close the connection only if it's not None
            if conn:
                conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    home_page = HomePage()
    home_page.show()
    sys.exit(app.exec_())
