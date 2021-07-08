# 3 Tabs: Contact, Emailer, Add Contact
# Add Contact is Form Layout
# Email is vertical layout
# Contact is vertical layout with buttons to click for more info

import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as g
import PyQt5.QtCore as qc
import sys
import sqlite3



class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Contact Book and Emailer")
        self.setLayout(qtw.QVBoxLayout())
        self.setGeometry(100,100,100,100)
        self.resize(300,300)

        tabs = qtw.QTabWidget()
        tabs.addTab(self.contactsTabUI(), "Contacts")
        tabs.addTab(self.addTabUI(), "Add")
        tabs.addTab(self.deleteTabUI(), "Delete")
        tabs.addTab(self.editTabUI(), "Edit")
        tabs.addTab(self.emailerTabUI(), "Emailer")
        self.layout().addWidget(tabs)

        
    def contactsTabUI(self):
        contactsTab = qtw.QWidget()

        contacts_layout = qtw.QGridLayout()

        contacts_label = qtw.QLabel("My Contacts")
        contacts_label.setFont(g.QFont('Comic Sans', 20))
        contacts_layout.addWidget(contacts_label,0,0)
        
        conn = sqlite3.connect("contact_book.db")
        c = conn.cursor()

        all_contacts = c.execute("SELECT * FROM contact_book ORDER BY name")
        num_row = 1
        num_col = 0
        
        for row in all_contacts:            
            if num_row < 3:
                num_row += 1
            else:
                num_col += 1
                num_row = 1

            previous_contact = row[1]

            contact_button = qtw.QPushButton(row[1] + "\nPhone Number: " + row[3] + "\nEmail Address: " + row[2])
            contact_button.setFont(g.QFont('Helvetica', 10))
            contact_button.setStyleSheet('QPushButton {background-color: #A3C1DA;}')
            contact_button.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
            contacts_layout.addWidget(contact_button, num_row, num_col)
        
        
        contactsTab.setLayout(contacts_layout)
        return contactsTab

    def emailerTabUI(self):
        emailerTab = qtw.QWidget()
        emailer_layout = qtw.QVBoxLayout()
        second_label = qtw.QLabel("Second Label")
        second_label.setFont(g.QFont('Comic Sans', 20))
        emailer_layout.addWidget(second_label)
        emailerTab.setLayout(emailer_layout)
        return emailerTab
    
    def addTabUI(self):
        addTab = qtw.QWidget()
        add_layout = qtw.QFormLayout()
        
        add_title = qtw.QLabel("Add a Contact")
        add_title.setFont(g.QFont('Comic Sans', 20))
        
        name_label = qtw.QLabel("Name")
        name = qtw.QLineEdit()

        phone_number_label = qtw.QLabel("Phone Number")
        phone_number = qtw.QLineEdit()

        email_address_label = qtw.QLabel("Email Address")
        email_address = qtw.QLineEdit()

        add_button = qtw.QPushButton("Add", clicked = lambda: add_Database())

        add_layout.addRow(add_title)
        add_layout.addRow(name_label, name)
        add_layout.addRow(phone_number_label, phone_number)
        add_layout.addRow(email_address_label, email_address)
        add_layout.addRow(add_button)

        addTab.setLayout(add_layout)

        def add_Database():
            conn = sqlite3.connect("contact_book.db")
            c = conn.cursor()

            c.execute("CREATE TABLE if not exists contact_book (id integer PRIMARY KEY, name text NOT NULL, email_address text NOT NULL, phone_number text NOT NULL)")

            add_message_box = qtw.QMessageBox()
            add_message_box.setIcon(qtw.QMessageBox.Information)

            if name.text() == "" or email_address.text() == "" or phone_number.text() == "":
                add_message_box.setText("Failed to add to contact book. One of the fields is empty.")

            else:
                c.execute("INSERT INTO contact_book (name, email_address, phone_number) VALUES (?,?,?)", (str(name.text()), str(email_address.text()), str(phone_number.text())))
                add_message_box.setText("Successfully Added to Contact Book! Please restart contact book to see the changes.")

            conn.commit()
            conn.close()

            run_message_box = add_message_box.exec_()
            sys.exit()
            
        return addTab

    def deleteTabUI(self):
        deleteTab = qtw.QWidget()
        delete_layout = qtw.QFormLayout()
        
        delete_title = qtw.QLabel("Delete a Contact")
        delete_title.setFont(g.QFont('Comic Sans', 20))
        
        delete_instructions = qtw.QLabel("Type in the name of the contact you want to delete.")
        delete_instructions.setFont(g.QFont('Comic Sans', 15))

        name_label = qtw.QLabel("Name")
        name = qtw.QLineEdit()    

        delete_button = qtw.QPushButton("Delete", clicked = lambda: delete_Database())

        delete_layout.addRow(delete_title)
        delete_layout.addRow(delete_instructions)
        delete_layout.addRow(name_label, name)
        delete_layout.addRow(delete_button)

        deleteTab.setLayout(delete_layout)

        def delete_Database():
            conn = sqlite3.connect("contact_book.db")
            c = conn.cursor()

            c.execute("CREATE TABLE if not exists contact_book (id integer PRIMARY KEY, name text NOT NULL, email_address text NOT NULL, phone_number text NOT NULL)")

            delete_message_box = qtw.QMessageBox()
            delete_message_box.setIcon(qtw.QMessageBox.Information)

            c.execute("SELECT * FROM contact_book WHERE name = ?",[name.text()])
            current_selection = c.fetchall()

            if name.text() == "" or not current_selection:
                delete_message_box.setText("Failed to delete from contact book. Name field is empty or doesn't match contacts")

            else:
                current_deletion = c.execute("DELETE FROM contact_book WHERE name = ?",[name.text()])
                delete_message_box.setText("Successfully deleted from Contact Book! Please restart contact book to see the changes.")

            conn.commit()
            conn.close()

            run_message_box = delete_message_box.exec_()

        return deleteTab

    def editTabUI(self):
        pass


application = qtw.QApplication(sys.argv)
mw = MainWindow()
mw.show()
sys.exit(application.exec_())