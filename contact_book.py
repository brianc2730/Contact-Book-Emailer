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
        editTab = qtw.QWidget()
        edit_layout = qtw.QFormLayout()

        edit_title = qtw.QLabel("Edit a Contact")
        edit_title.setFont(g.QFont('Comic Sans', 20))
        
        edit_instructions = qtw.QLabel("Type in the name of the contact you want to edit.")
        edit_instructions.setFont(g.QFont('Comic Sans', 15))

        name_label = qtw.QLabel("Name")
        name = qtw.QLineEdit()    

        edit_button = qtw.QPushButton("Edit", clicked = lambda: edit_Database())

        phone_number_edit_label = qtw.QLabel("Phone Number")
        phone_number_edit_label.setHidden(True)
        phone_number_edit = qtw.QLineEdit("")
        phone_number_edit.setHidden(True)

        email_address_edit_label = qtw.QLabel("Email Address")
        email_address_edit_label.setHidden(True)
        email_address_edit = qtw.QLineEdit("")
        email_address_edit.setHidden(True)

        edit_confirm_button = qtw.QPushButton("Confirm", clicked = lambda: confirm_edit_database())
        edit_confirm_button.setHidden(True)

        edit_layout.addRow(edit_title)
        edit_layout.addRow(edit_instructions)
        edit_layout.addRow(name_label, name)
        edit_layout.addRow(edit_button)
        edit_layout.addRow(phone_number_edit_label, phone_number_edit)
        edit_layout.addRow(email_address_edit_label, email_address_edit)
        edit_layout.addRow(edit_confirm_button)

        editTab.setLayout(edit_layout)

        conn = sqlite3.connect("contact_book.db")
        c = conn.cursor()

        def edit_Database():

            c.execute("CREATE TABLE if not exists contact_book (id integer PRIMARY KEY, name text NOT NULL, email_address text NOT NULL, phone_number text NOT NULL)")

            edit_message_box = qtw.QMessageBox()
            edit_message_box.setIcon(qtw.QMessageBox.Information)

            c.execute("SELECT * FROM contact_book WHERE name = ?",[name.text()])
            current_selection = c.fetchone()

            if name.text() == "" or not current_selection:
                edit_message_box.setText("Failed to find contact from contact book. Name field is empty or doesn't match contacts")
                run_message_box = edit_message_box.exec_()

            else:
                phone_number_edit_label.setHidden(False)
                phone_number_edit.setHidden(False)
                phone_number_edit.setText(current_selection[3])

                email_address_edit_label.setHidden(False)
                email_address_edit.setHidden(False)
                email_address_edit.setText(current_selection[2])

                edit_confirm_button.setHidden(False)

        def confirm_edit_database():
            edit_message_confirm_box = qtw.QMessageBox()
            edit_message_confirm_box.setIcon(qtw.QMessageBox.Information)

            if phone_number_edit.text() == "" or email_address_edit.text() == "":
                edit_message_confirm_box.setText("Please provide the edited credentials")

            else:
                c.execute("UPDATE contact_book SET phone_number = ?, email_address = ?", [phone_number_edit.text(), email_address_edit.text()])
                edit_message_confirm_box.setText("Successfully edited Contact Book! Please restart contact book to see the changes.")

                conn.commit()
                conn.close()

            run_message_confirm_box = edit_message_confirm_box.exec_()

        return editTab


application = qtw.QApplication(sys.argv)
mw = MainWindow()
mw.show()
sys.exit(application.exec_())