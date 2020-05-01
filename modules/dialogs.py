__author__ = 'Tim MacDonald'
# Copyright 2019 Timothy MacDonald
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from PyQt5 import QtCore, QtGui, QtWidgets
import re

class findReplaceCopyDialog(QtWidgets.QDialog):

    def __init__(self, fromcategories, tocategories, parent=None):
        super(findReplaceCopyDialog, self).__init__(parent)
        self.objectlist = []
        self.setupUi(self, fromcategories, tocategories)

    def setupUi(self, frcd, fromcategories, tocategories):

        # setup static elements
        frcd.setObjectName("FindReplaceCopy")
        frcd.resize(1150, 640)
        self.buttonBox = QtWidgets.QDialogButtonBox(frcd)
        self.buttonBox.setGeometry(QtCore.QRect(10, 600, 1130, 35))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBoxOkCancel")
        self.label = QtWidgets.QLabel(frcd)
        self.label.setGeometry(QtCore.QRect(20, 10, 1120, 140))
        self.label.setWordWrap(True)
        self.label.setObjectName("labelInstructions")
        self.scrollArea = QtWidgets.QScrollArea(frcd)
        self.scrollArea.setGeometry(QtCore.QRect(10, 150, 1130, 440))
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidget = QtWidgets.QWidget()
        self.scrollAreaWidgetContents = QtWidgets.QFormLayout()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        # set up the list of destination categories to populate into the comboboxes
        itemmodel = QtGui.QStandardItemModel()
        for tocategory in tocategories:
            text_item = QtGui.QStandardItem(str(tocategory))
            itemmodel.appendRow(text_item)
        itemmodel.sort(0)

        # Create 1 set of (checkbox, label, combobox per fromcategory


        for index, fromcategory in enumerate(fromcategories):

            objectdict = {'checkbox': None, 'label': None, 'combobox': None}
            layout = QtWidgets.QHBoxLayout()
            objectdict['checkbox'] = QtWidgets.QCheckBox()
            objectdict['checkbox'].setGeometry(QtCore.QRect(0, 0, 20, 20))
            objectdict['checkbox'].setText("")
            objectdict['checkbox'].setObjectName("checkBox" + str(index))
            layout.addWidget(objectdict['checkbox'])
            objectdict['label']= QtWidgets.QLabel()
            objectdict['label'].setGeometry(QtCore.QRect(0, 0, 480, 25))
            objectdict['label'].setObjectName("comboBox" + str(index))
            objectdict['label'].setText(fromcategory)
            layout.addWidget(objectdict['label'])
            objectdict['combobox'] = QtWidgets.QComboBox()
            objectdict['combobox'].setGeometry(QtCore.QRect(550, 0, 485, 25))
            objectdict['combobox'].setObjectName("comboBox" + str(index))
            objectdict['combobox'].setModel(itemmodel)
            objectdict['combobox'].setEditable(True)
            layout.addWidget(objectdict['combobox'])
            self.objectlist.append(objectdict)
            self.scrollAreaWidgetContents.addRow(layout)

        self.scrollAreaWidget.setLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidget)
        self.scrollArea.show()


        self.retranslateUi(frcd)
        self.buttonBox.accepted.connect(frcd.accept)
        self.buttonBox.rejected.connect(frcd.reject)
        QtCore.QMetaObject.connectSlotsByName(frcd)

    def retranslateUi(self, FindReplaceCopy):
        _translate = QtCore.QCoreApplication.translate
        FindReplaceCopy.setWindowTitle(_translate("FindReplaceCopy", "Dialog"))
        self.label.setText(_translate("FindReplaceCopy",
                                      "<html><head/><body><p>Each entry on the left is one of the source categories present in your content. </p><p>From the drop downs on the right select the source categories you want to replace them with or type your own. These have been populated from your destination org/tenant. </p><p>Checked items will be replaced, unchecked items will not be modified. </p><p>Note: The query that populates the destination dropdowns only searches for source categories that have ingested something in the last hour. If you are sporadically ingesting data then some source categories may not show up. You can type those in manually.</p></body></html>"))

    def getresults(self):
        results = []
        for object in self.objectlist:
            if str(object['checkbox'].checkState()) == '2':
                objectdata = { 'from': str(object['label'].text()), 'to': str(object['combobox'].currentText())}
                results.append(objectdata)
        return results

class NewPasswordDialog(QtWidgets.QDialog):

    def __init__(self):
        super(NewPasswordDialog, self).__init__()
        self.objectlist = []
        self.setupUi(self)

    def setupUi(self, Dialog):

        Dialog.setObjectName("EnterNewPassword")
        Dialog.resize(320, 366)
        self.setWindowTitle('Enter new password...')
        self.okbutton = QtWidgets.QPushButton(Dialog)
        self.okbutton.setText('OK')
        self.okbutton.setGeometry(250, 320, 50, 32)
        self.okbutton.setEnabled(False)

        self.cancelbutton = QtWidgets.QPushButton(Dialog)
        self.cancelbutton.setText('Cancel')
        self.cancelbutton.setGeometry(190, 320, 50, 32)
        self.cancelbutton.setEnabled(True)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(17, 7, 281, 81))
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        self.lineEditPassword1 = QtWidgets.QLineEdit(Dialog)
        self.lineEditPassword1.setGeometry(QtCore.QRect(20, 240, 281, 31))
        self.lineEditPassword1.setObjectName("lineEditPassword1")
        self.lineEditPassword1.setEchoMode(2)
        self.lineEditPassword2 = QtWidgets.QLineEdit(Dialog)
        self.lineEditPassword2.setGeometry(QtCore.QRect(20, 280, 281, 34))
        self.lineEditPassword2.setObjectName("lineEditPassword2")
        self.lineEditPassword2.setEchoMode(2)
        self.labelCount = QtWidgets.QLabel(Dialog)
        self.labelCount.setGeometry(QtCore.QRect(20, 100, 281, 18))
        self.labelCount.setObjectName("labelCount")
        self.labelLowerCase = QtWidgets.QLabel(Dialog)
        self.labelLowerCase.setGeometry(QtCore.QRect(20, 120, 281, 18))
        self.labelLowerCase.setObjectName("labe1LowerCase")
        self.labelUpperCase = QtWidgets.QLabel(Dialog)
        self.labelUpperCase.setGeometry(QtCore.QRect(20, 140, 281, 18))
        self.labelUpperCase.setObjectName("labelUpperCase")
        self.labelNumeral = QtWidgets.QLabel(Dialog)
        self.labelNumeral.setGeometry(QtCore.QRect(20, 160, 281, 18))
        self.labelNumeral.setObjectName("labelNumeral")
        self.labelNonAlphaNumeric = QtWidgets.QLabel(Dialog)
        self.labelNonAlphaNumeric.setGeometry(QtCore.QRect(20, 180, 281, 18))
        self.labelNonAlphaNumeric.setObjectName("labelNonAlphaNumeric")
        self.labelMatch = QtWidgets.QLabel(Dialog)
        self.labelMatch.setGeometry(QtCore.QRect(20, 200, 281, 18))
        self.labelMatch.setObjectName("labelMatch")

        self.retranslateUi(Dialog)
        # self.buttonBox.accepted.connect(Dialog.accept)
        # self.buttonBox.rejected.connect(Dialog.reject)
        self.okbutton.clicked.connect(Dialog.accept)
        self.cancelbutton.clicked.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.lineEditPassword1.textEdited.connect(self.check_password)
        self.lineEditPassword2.textEdited.connect(self.check_password)
        self.labelCount.setStyleSheet('color: red')
        self.labelLowerCase.setStyleSheet('color: red')
        self.labelUpperCase.setStyleSheet('color: red')
        self.labelNumeral.setStyleSheet('color: red')
        self.labelNonAlphaNumeric.setStyleSheet('color: red')
        self.labelMatch.setStyleSheet('color: red')

    def check_password(self):
        password1 = self.lineEditPassword1.text()
        password2 = self.lineEditPassword2.text()
        if len(password1) > 9:
            self.labelCount.setStyleSheet('color: green')
            count = True
        else:
            self.labelCount.setStyleSheet('color: red')
            count = False

        if re.search(r'[a-z]', password1):
            self.labelLowerCase.setStyleSheet('color: green')
            lower = True
        else:
            self.labelLowerCase.setStyleSheet('color: red')
            lower = False

        if re.search(r'[A-Z]', password1):
            self.labelUpperCase.setStyleSheet('color: green')
            upper = True
        else:
            self.labelUpperCase.setStyleSheet('color: red')
            upper = False

        if re.search(r'[0-9]', password1):
            self.labelNumeral.setStyleSheet('color: green')
            numeral = True
        else:
            self.labelNumeral.setStyleSheet('color: red')
            numeral = False

        if re.search(r'[,\.!?#@$]', password1):
            self.labelNonAlphaNumeric.setStyleSheet('color: green')
            nonalpha = True
        else:
            self.labelNonAlphaNumeric.setStyleSheet('color: red')
            nonalpha = False

        if password1 == password2:
            self.labelMatch.setStyleSheet('color: green')
            match = True
        else:
            self.labelMatch.setStyleSheet('color: red')
            match = False

        if count and lower and upper and numeral and nonalpha and match:
            self.okbutton.setEnabled(True)
        else:
            self.okbutton.setEnabled(False)

    def getresults(self):
            return str(self.lineEditPassword1.text())

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Please enter a new password.\n"
"Once entered your password cannot\n"
"be retrieved. Remember it!\n"
"It must meet the following conditions:"))
        self.labelCount.setText(_translate("Dialog", "-Have 10 or more characters"))
        self.labelLowerCase.setText(_translate("Dialog", "-Contain at least 1 lowercase character"))
        self.labelUpperCase.setText(_translate("Dialog", "-Contain at least 1 uppercase character"))
        self.labelNumeral.setText(_translate("Dialog", "-Contain at least 1 numeral"))
        self.labelNonAlphaNumeric.setText(_translate("Dialog", "-Contain at least 1 of these ,.!?#@$"))
        self.labelMatch.setText(_translate("Dialog", "-Both entries must match"))


class restoreSourcesDialog(QtWidgets.QDialog):

    def __init__(self, sources_json, parent=None):
        super(restoreSourcesDialog, self).__init__(parent)
        self.objectlist = []
        self.setupUi(self, sources_json)

    def setupUi(self, rsd, sources_json):

        # setup static elements
        rsd.setObjectName("Restore Sources")
        rsd.resize(1150, 640)
        self.buttonBox = QtWidgets.QDialogButtonBox(rsd)
        self.buttonBox.setGeometry(QtCore.QRect(10, 600, 1130, 35))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBoxOkCancel")
        self.label = QtWidgets.QLabel(rsd)
        self.label.setGeometry(QtCore.QRect(20, 10, 1120, 140))
        self.label.setWordWrap(True)
        self.label.setObjectName("labelInstructions")
        self.scrollArea = QtWidgets.QScrollArea(rsd)
        self.scrollArea.setGeometry(QtCore.QRect(10, 150, 1130, 440))
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidget = QtWidgets.QWidget()
        self.scrollAreaWidgetContents = QtWidgets.QFormLayout()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")



        # Create 1 set of (checkbox, label, combobox per fromcategory


        for index, source in enumerate(sources_json):

            objectdict = {'checkbox': None, 'label': None}
            layout = QtWidgets.QHBoxLayout()
            objectdict['checkbox'] = QtWidgets.QCheckBox()
            objectdict['checkbox'].setGeometry(QtCore.QRect(0, 0, 20, 20))
            objectdict['checkbox'].setText("")
            objectdict['checkbox'].setObjectName("checkBox" + str(index))
            objectdict['checkbox'].setCheckState(2)
            layout.addWidget(objectdict['checkbox'])
            objectdict['label']= QtWidgets.QLabel()
            objectdict['label'].setGeometry(QtCore.QRect(0, 0, 480, 25))
            objectdict['label'].setObjectName("label" + str(index))
            objectdict['label'].setText(source['name'])
            layout.addWidget(objectdict['label'])

            self.objectlist.append(objectdict)
            self.scrollAreaWidgetContents.addRow(layout)

        self.scrollAreaWidget.setLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidget)
        self.scrollArea.show()


        self.retranslateUi(rsd)
        self.buttonBox.accepted.connect(rsd.accept)
        self.buttonBox.rejected.connect(rsd.reject)
        QtCore.QMetaObject.connectSlotsByName(rsd)

    def retranslateUi(self, restoreSourcesDialog):
        _translate = QtCore.QCoreApplication.translate
        restoreSourcesDialog.setWindowTitle(_translate("Restore Sources", "Dialog"))
        self.label.setText(_translate("Restore Sources",
                                      "<html><head/><body<p>Select the sources you wish to restore:</p></body></html>"))

    def getresults(self):
        results = []
        for object in self.objectlist:
            if str(object['checkbox'].checkState()) == '2':
                results.append(object['label'].text())
        return results