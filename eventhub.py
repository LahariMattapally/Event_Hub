import tkinter
from tkinter import messagebox
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import mysql.connector as mysql
import random
import smtplib
from tkcalendar import Calendar, DateEntry


class Eventhub():
    def __init__(self):
        super().__init__()
        self.tkn = tkinter.Tk()
        self.tkn.title("Event Hub")
        self.tkn.geometry("800x500")
        self.show_welcome_page()


        database = {
            'user': 'root',
            'password': 'Lucky',
            'host': 'localhost',
            'port': 3306,
            'database': 'eventhub'
        }


        self.database= mysql.connect(**database)
        self.cursor = self.database.cursor()

        # Create the database tables
        self.createUserTable()
        self.createEventTable()
        self.createEventRegistrationTable()
        self.createEventCommentTable()

    def createUserTable(self):
        # SQL statement for creating the 'user' table
        create_user_table = """
        CREATE TABLE IF NOT EXISTS user (
            userID INT AUTO_INCREMENT PRIMARY KEY,
            firstName VARCHAR(255) NOT NULL,
            lastName VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        );
        """
        self.cursor.execute(create_user_table)
        self.database.commit()


    def createEventTable(self):
        # SQL statement for creating the 'event' table
        create_event_table = """
        CREATE TABLE IF NOT EXISTS event (
            eventID INT AUTO_INCREMENT PRIMARY KEY,
            eventName VARCHAR(255) NOT NULL,
            eventDate VARCHAR(255) NOT NULL,
            eventTime VARCHAR(255) NOT NULL,
            eventLocation VARCHAR(255) NOT NULL,
            eventDescription TEXT NOT NULL
        );
        """
        self.cursor.execute(create_event_table)
        self.database.commit()

    def createEventRegistrationTable(self):
        # SQL statement for creating the 'eventRegistration' table
        create_event_registration_table = """
        CREATE TABLE IF NOT EXISTS eventRegistration (
            eventRegistrationID INT AUTO_INCREMENT PRIMARY KEY,
            eventID INT NOT NULL,
            userID INT NOT NULL,
            FOREIGN KEY (eventID) REFERENCES event (eventID),
            FOREIGN KEY (userID) REFERENCES user (userID)
        );
        """
        self.cursor.execute(create_event_registration_table)
        self.database.commit()


    def createEventCommentTable(self):
        # SQL statement for creating the 'eventComment' table
        create_event_comment_table = """
        CREATE TABLE IF NOT EXISTS eventComment (
            eventCommentID INT AUTO_INCREMENT PRIMARY KEY,
            eventID INT NOT NULL,
            userID INT NOT NULL,
            comment TEXT NOT NULL,
            FOREIGN KEY (eventID) REFERENCES event (eventID),
            FOREIGN KEY (userID) REFERENCES user (userID)
        );
        """
        self.cursor.execute(create_event_comment_table)

        # Commit the changes to the database
        self.database.commit()

    def __del__(self):
        # Close the database connection
        self.cursor.close()
        self.database.close()


    def configure_button(self, button):
        #curver border
        button.configure(bg="#0078d4", fg="white", font=("Verdana", 12), relief="raised")
        #button rounded border
        button.configure(borderwidth=3, highlightthickness=3, width=20, height=1)



    def configure_entry(self, entry_widget):
        entry_widget.config(
            font=("Arial", 12),  # Font and font size
            bd=2,  # Border width
            relief="ridge",  # Border style
            fg="black",  # Text color
            bg="white",  # Background color
            selectbackground="lightblue",  # Background color when selected
            selectforeground="black",  # Text color when selected
            insertbackground="black",  # Cursor color
            insertwidth=2,  # Cursor width
            highlightcolor="blue",  # Highlight color when focused
            highlightthickness=1,  # Highlight thickness
            highlightbackground="black",  # Highlight background color
            disabledbackground="lightgray",  # Background color when disabled
            disabledforeground="gray"  # Text color when disabled
        )
    def configure_label(self, label_widget):
        label_widget.config(
            font=("Helvetica", 12),  # Font and font size
            fg="black",  # Text color (foreground color)
            bg="white",  # Background color
            padx=5,  # Padding on the x-axis
            pady=5,  # Padding on the y-axis
            anchor="center",  # Text alignment (centered)
        )


    def show_welcome_page(self):
        self.tkn.geometry("850x600")  # Slightly increase the height for a more dynamic look

        #background color to white
        self.tkn.configure(bg="white")


        for widget in self.tkn.winfo_children():
            widget.destroy()


        #welcome to event hub label
        welcome_label = tkinter.Label(self.tkn, text="Welcome to Event Hub", font=("Helvetica", 20))
        welcome_label.pack(pady=0)
        #label background color to white
        welcome_label.configure(bg="white")


        #display the image in images/welcome.jpg 900x600
        welcome_image_path = Image.open("images/welcome.jpg")
        welcome_image = ImageTk.PhotoImage(welcome_image_path)        
        welcome_image_label = tkinter.Label(self.tkn, image=welcome_image)
        welcome_image_label.photo = welcome_image
        welcome_image_label.pack(pady=0)

        #display text and button upon the image
        #this happens after creating a frame and displaying the text and button on the frame
        #welcome frame
        welcome_frame = tkinter.Frame(self.tkn)
        welcome_frame.pack(pady=10)


        # introduce about the event hub
        label = tkinter.Label(self.tkn, text="Event Hub is a platform for event organizers to create and promote their events, and for users to discover and register for events.", font=("Helvetica", 10))
        label.configure(bg="white")
        label.pack(pady=10)


        #button to main page    
        #let's get started button
        get_started_button = tkinter.Button(self.tkn, text="Let's Get Started", command=self.show_main_page)
        self.configure_button(get_started_button)
        get_started_button.pack(pady=20)


       
    def show_main_page(self):
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Create a frame for the main page content
        main_frame = tkinter.Frame(self.tkn)
        main_frame.configure(bg="white")
        main_frame.pack(expand=True)

        # Add a title label
        title_label = tkinter.Label(main_frame, text="EVENT HUB", font=("Helvetica", 20))
        title_label.configure(bg="white")
        title_label.pack(pady=20)

        # Create a grid for the buttons
        button_frame = tkinter.Frame(main_frame)
        button_frame.configure(bg="white")
        button_frame.pack(expand=True)

        # Add buttons to navigate to different views
        welcome_button = tkinter.Button(button_frame, text="Back to Welcome Page", command=self.show_welcome_page)
        login_button = tkinter.Button(button_frame, text="Login", command=self.show_login_page)
        register_button = tkinter.Button(button_frame, text="Register", command=self.show_register_page)

        # Configure button appearance
        self.configure_button(welcome_button)
        self.configure_button(login_button)
        self.configure_button(register_button)

        # Pack the buttons in a grid layout
        welcome_button.grid(row=2, column=0, padx=10, pady=10)
        login_button.grid(row=0, column=0, padx=10, pady=10)
        register_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)



