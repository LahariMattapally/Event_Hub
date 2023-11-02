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


    def show_login_page(self):
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add login form elements
        label = tkinter.Label(self.tkn, text="Welcome to Login", font=("Helvetica", 20))
        label.configure(bg="white")
        label.pack(pady=20)

        # Email (Gmail ID) entry
        self.email_entry = tkinter.Label(self.tkn, text="Enter Email ID :")
        self.email_entry.configure(bg="white")
        self.email_entry.pack()

        self.email_entry = tkinter.Entry(self.tkn)
        self.configure_entry(self.email_entry)
        self.email_entry.pack()

        # Send OTP button
        self.send_otp_button = tkinter.Button(self.tkn, text="Send OTP", command=self.verifyUser)
        self.configure_button(self.send_otp_button)  # Apply custom button styling
        self.send_otp_button.pack(pady=20)

        # Placeholder for OTP entry
        self.otp_label = tkinter.Label(self.tkn, text="Enter OTP:")
        self.otp_label.configure(bg="white")
        self.otp_label.pack()
        self.otp_entry = tkinter.Entry(self.tkn, state="disabled")  # Initially disabled
        self.configure_entry(self.otp_entry)
        self.otp_entry.pack()

        # Login button (disabled until OTP is entered)
        self.login_button = tkinter.Button(self.tkn, text="Login", command=self.loginUser, state="disabled")
        self.configure_button(self.login_button)  # Apply custom button styling
        self.login_button.pack(pady=20)

        # Register button
        self.register_button = tkinter.Button(self.tkn, text="Register", command=self.show_register_page)
        self.configure_button(self.register_button)  # Apply custom button styling
        self.register_button.pack(pady=10)

        # Back button to return to the welcome page
        self.back_button = tkinter.Button(self.tkn, text="Back to Welcome", command=self.show_welcome_page)
        self.configure_button(self.back_button)  # Apply custom button styling
        self.back_button.pack(pady=10)



    def show_register_page(self):
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add registration form elements
        label = tkinter.Label(self.tkn, text="Register here for Event hub", font=("Helvetica", 20))
        label.configure(bg="white")
        label.pack(pady=20)

        # First Name entry
        self.first_name_label = tkinter.Label(self.tkn, text="First Name:")
        self.configure_label(self.first_name_label)
        self.first_name_label.pack()
        self.first_name_entry = tkinter.Entry(self.tkn)
        self.configure_entry(self.first_name_entry)
        self.first_name_entry.pack()

        # Last Name entry
        self.last_name_label = tkinter.Label(self.tkn, text="Last Name:")
        self.configure_label(self.last_name_label)
        self.last_name_label.pack()
        self.last_name_entry = tkinter.Entry(self.tkn)
        self.configure_entry(self.last_name_entry)
        self.last_name_entry.pack()

        # Email (Gmail ID) entry
        self.email_entry = tkinter.Label(self.tkn, text="Email (Gmail ID):")
        self.configure_label(self.email_entry)
        self.email_entry.pack()
        self.email_entry = tkinter.Entry(self.tkn)
        self.configure_entry(self.email_entry)
        self.email_entry.pack()

        # Password entry
        self.password_label = tkinter.Label(self.tkn, text="Password:")
        self.configure_label(self.password_label)
        self.password_label.pack()
        self.password_entry = tkinter.Entry(self.tkn,show="*")
        self.configure_entry(self.password_entry)
        self.password_entry.pack()

        # Register button
        self.register_button = tkinter.Button(self.tkn, text="Register", command=self.registerUser)
        self.configure_button(self.register_button)
        self.register_button.pack(pady=20)

        # Back button to return to the welcome page
        self.back_button = tkinter.Button(self.tkn, text="Back to Welcome", command=self.show_welcome_page)
        self.configure_button(self.back_button)
        self.back_button.pack(pady=10)


    def admin_dashboard(self):
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add admin dashboard elements
        label = tkinter.Label(self.tkn, text="Admin Dashboard", font=("Helvetica", 20))
        label.configure(bg="white")
        label.pack(pady=20)

        #search bar to search events from treeview
        search_label = tkinter.Label(self.tkn, text="Search Event Name :")
        self.configure_label(search_label)
        search_label.pack()
        self.search_entry = tkinter.Entry(self.tkn)
        self.configure_entry(self.search_entry)
        self.search_entry.pack()

        #treeview of events 
        # Create a Treeview widget to display events
        event_tree = ttk.Treeview(self.tkn, columns=(
        "Event Name", "Event Date", "Event Time", "Event Location", "Event Description"), show="headings")
        event_tree.heading("#1", text="Event Name")
        event_tree.column("#1", width=150)
        event_tree.heading("#2", text="Event Date")
        event_tree.column("#2", width=150)
        event_tree.heading("#3", text="Event Time")
        event_tree.column("#3", width=150)
        event_tree.heading("#4", text="Event Location")
        event_tree.column("#4", width=150)
        event_tree.heading("#5", text="Event Description")
        event_tree.column("#5", width=150)

        # Connect to the 'events.db' database and retrieve event data from mysql   
        query = "SELECT * FROM eventhub.event"
        try:
            self.cursor.execute(query)
            events = self.cursor.fetchall()
        except mysql.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")
            return
        
        # Populate the Treeview with event data
        for event in events:
            event_tree.insert("", "end", values=event)
        
        event_tree.pack()

        # Add buttons to navigate to different views
        event_button = tkinter.Button(self.tkn, text="Add Event", command=self.show_admin_event_page)
        self.configure_button(event_button)
        event_button.pack(pady=20)

        logout_button = tkinter.Button(self.tkn, text="Logout", command=self.show_welcome_page)
        self.configure_button(logout_button)
        logout_button.pack(pady=10)

        
    def show_admin_event_page(self):
        self.tkn.geometry("800x500")
        for widget in self.tkn.winfo_children():
            widget.destroy()

        # Add event form elements
        label = tkinter.Label(self.tkn, text="Admin Event Page", font=("Helvetica", 20))
        label.configure(bg="white")
        label.pack(pady=20)

        # Event Name entry
        self.event_name_label = tkinter.Label(self.tkn, text="Event Name:")
        self.configure_label(self.event_name_label)
        self.event_name_label.pack()

        self.event_name_entry = tkinter.Entry(self.tkn)
        self.configure_entry(self.event_name_entry)
        self.event_name_entry.pack()

        # Event Date entry
        self.event_date_label = tkinter.Label(self.tkn, text="Event Date:")
        self.configure_label(self.event_date_label)
        self.event_date_label.pack()
        self.event_date_entry = DateEntry(self.tkn,width=15,background="darkblue", foreground="white", date_pattern="MM/dd/yyyy", font=("Arial", 15))
        # self.configure_entry(self.event_date_entry)
        self.event_date_entry.pack()

        # Event Time entry
        self.event_time_label = tkinter.Label(self.tkn, text="Event Time: HH:MM AM/PM")
        self.configure_label(self.event_time_label)
        self.event_time_label.pack()
        self.event_time_entry = tkinter.Entry(self.tkn)
        self.configure_entry(self.event_time_entry)
        self.event_time_entry.pack()

        # Event Location entry
        self.event_location_label = tkinter.Label(self.tkn, text="Event Location:")
        self.configure_label(self.event_location_label)
        self.event_location_label.pack()
        self.event_location_entry = tkinter.Entry(self.tkn)
        self.configure_entry(self.event_location_entry)
        self.event_location_entry.pack()

        # Event Description entry
        self.event_description_label = tkinter.Label(self.tkn, text="Event Description:")
        self.configure_label(self.event_description_label)
        self.event_description_label.pack()
        self.event_description_entry = tkinter.Entry(self.tkn)
        self.configure_entry(self.event_description_entry)
        self.event_description_entry.pack()

        # Register button
        self.register_button = tkinter.Button(self.tkn, text="Register", command=self.registerEvent)
        self.configure_button(self.register_button)
        self.register_button.pack(pady=10)

        #back to admin dashboard button
        self.back_button = tkinter.Button(self.tkn, text="Back to Admin Dashboard", command=self.admin_dashboard)
        self.configure_button(self.back_button)
        self.back_button.pack(pady=10)




