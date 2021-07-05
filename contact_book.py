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
        self.resize(750,750)

        tabs = qtw.QTabWidget()
        tabs.addTab(self.contactsTabUI(), "Contacts")
        tabs.addTab(self.emailerTabUI(), "Emailer")
        tabs.addTab(self.addTabUI(), "Add")
        self.layout().addWidget(tabs)

        
    def contactsTabUI(self):
        contactsTab = qtw.QWidget()
        contacts_layout = qtw.QVBoxLayout()
        test_label = qtw.QLabel("First Label")
        test_label.setFont(g.QFont('Comic Sans', 20))
        contacts_layout.addWidget(test_label)
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
        
        third_label = qtw.QLabel("Add a Contact")
        third_label.setFont(g.QFont('Comic Sans', 20))
        third_label.setAlignment(qc.Qt.AlignCenter)
        add_layout.addWidget(third_label)

        addTab.setLayout(add_layout)

        return addTab


application = qtw.QApplication(sys.argv)
mw = MainWindow()
mw.show()
sys.exit(application.exec_())
