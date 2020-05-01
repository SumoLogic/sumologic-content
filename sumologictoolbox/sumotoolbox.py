__author__ = 'Tim MacDonald'
__version__ = '0.6'
# Copyright 2015 Timothy MacDonald
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import sys
import json
import csv
import pytz
import os.path
from datetime import datetime
from tzlocal import get_localzone
from qtpy import QtCore, QtGui, QtWidgets, uic
import pathlib
import os
import logzero
from logzero import logger
import configparser
import shutil
import qtmodern.styles
import qtmodern.windows
import time
from modules.scheduled_view import scheduled_view_tab
from modules.field_extration_rule import field_extraction_rule_tab
from modules.content import content_tab
from modules.collector import collector_tab

#local imports
from modules.sumologic import SumoLogic
from modules.credentials import CredentialsDB
from modules.dialogs import *

# detect if in Pyinstaller package and build appropriate base directory path
if getattr(sys, 'frozen', False):
    basedir = sys._MEIPASS
else:
    basedir = os.path.dirname(os.path.abspath(__file__))
# Setup logging
logzero.logfile("sumotoolbox.log")
logzero.loglevel(level=20)  #  Info Logging
# Log messages
logger.info("SumoLogicToolBox started.")
# This script uses Qt Designer files to define the UI elements which must be loaded
qtMainWindowUI = os.path.join(basedir, 'data/sumotoolbox.ui')
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtMainWindowUI)

class sumotoolbox(QtWidgets.QMainWindow, Ui_MainWindow):



    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        # detect if we are running in a pyinstaller bundle and set the base directory for file loads"
        if getattr(sys, 'frozen', False):
            self.basedir = sys._MEIPASS
        else:
            self.basedir = os.path.dirname(os.path.abspath(__file__))

        self.setupUi(self)

        # initialize variable to hold whether we've authenticated the cred database
        self.cred_db_authenticated = False

        self.init_and_load_config_file()
        self.initModels()  # load all the comboboxes and such with values
        # Configure the menu actions
        self.setup_menus()
        # Initially set logging level to match what is checked in the logging menu
        self.change_logging_level()



        # Configure the creddb buttons according to the config file settings
        #self.initial_config_cred_db_buttons()
        self.set_creddbbuttons()

        # load additional Tabs from available modules
        self.collector = collector_tab(self)
        self.tabWidget.addTab(self.collector, "Collectors")
        self.content = content_tab(self)
        self.tabWidget.addTab(self.content, "Content")
        self.field_extraction_rule = field_extraction_rule_tab(self)
        self.tabWidget.addTab(self.field_extraction_rule, "Field Extraction Rules")
        self.scheduled_view = scheduled_view_tab(self)
        self.tabWidget.addTab(self.scheduled_view, "Scheduled Views")

        # disable right credential box because we always start on the search tab
        # which only uses the left credentials
        self.tabchange(0)

        # initial clear of all stateful objects
        self.reset_stateful_objects()

        # connect all of the UI button elements to their respective methods

        #Set up a signal if the tabs are clicked
        self.tabWidget.currentChanged.connect(self.tabchange)

        #UI Buttons for Credential Store

        self.pushButtonCreateCredentialDatabase.clicked.connect(self.createcredb)
        self.pushButtonLoadCredentialDatabase.clicked.connect(self.loadcreddb)
        self.pushButtonDeleteCredentialDatabase.clicked.connect(self.deletecreddb)

        # Left Preset Buttons

        self.pushButtonCreatePresetLeft.clicked.connect(lambda: self.create_preset(
            self.comboBoxRegionLeft,
            self.lineEditUserNameLeft,
            self.lineEditPasswordLeft,
            self.comboBoxPresetLeft,
            'left'
        ))

        self.comboBoxPresetLeft.currentIndexChanged.connect(lambda: self.load_preset(
            str(self.comboBoxPresetLeft.currentText()),
            self.comboBoxRegionLeft,
            self.lineEditUserNameLeft,
            self.lineEditPasswordLeft,
            self.comboBoxPresetLeft,
            'left'
        ))

        # This exists for an edge case. If there is only one entry in the preset list and the user edits/modifies
        # the cred text then clicking on the preset will not reload the cred because the index hasn't changed.
        # This solves this problem
        self.comboBoxPresetLeft.activated.connect(lambda: self.preset_activated(
            str(self.comboBoxPresetLeft.currentText()),
            self.comboBoxRegionLeft,
            self.lineEditUserNameLeft,
            self.lineEditPasswordLeft,
            self.comboBoxPresetLeft,
            'left'
        ))

        self.pushButtonDeletePresetLeft.clicked.connect(lambda: self.delete_preset(
            str(self.comboBoxPresetLeft.currentText()),
            self.comboBoxRegionLeft,
            self.lineEditUserNameLeft,
            self.lineEditPasswordLeft,
            self.comboBoxPresetLeft,
            'left'
        ))

        self.pushButtonUpdatePresetLeft.clicked.connect(lambda: self.update_preset(
            str(self.comboBoxPresetLeft.currentText()),
            str(self.comboBoxRegionLeft.currentText()),
            str(self.lineEditUserNameLeft.text()),
            str(self.lineEditPasswordLeft.text())
        ))

        # Right Preset Buttons

        self.pushButtonCreatePresetRight.clicked.connect(lambda: self.create_preset(
            self.comboBoxRegionRight,
            self.lineEditUserNameRight,
            self.lineEditPasswordRight,
            self.comboBoxPresetRight,
            'right'
        ))

        self.comboBoxPresetRight.currentIndexChanged.connect(lambda: self.load_preset(
            str(self.comboBoxPresetRight.currentText()),
            self.comboBoxRegionRight,
            self.lineEditUserNameRight,
            self.lineEditPasswordRight,
            self.comboBoxPresetRight,
            'right'
        ))

        # This exists for an edge case. If there is only one entry in the preset list and the user edits/modifies
        # the cred text then clicking on the preset will not reload the cred because the index hasn't changed.
        # This solves this problem
        self.comboBoxPresetRight.activated.connect(lambda: self.preset_activated(
            str(self.comboBoxPresetRight.currentText()),
            self.comboBoxRegionRight,
            self.lineEditUserNameRight,
            self.lineEditPasswordRight,
            self.comboBoxPresetRight,
            'Right'
        ))

        self.pushButtonDeletePresetRight.clicked.connect(lambda: self.delete_preset(
            str(self.comboBoxPresetRight.currentText()),
            self.comboBoxRegionRight,
            self.lineEditUserNameRight,
            self.lineEditPasswordRight,
            self.comboBoxPresetRight,
            'right'
        ))

        self.pushButtonUpdatePresetRight.clicked.connect(lambda: self.update_preset(
            str(self.comboBoxPresetRight.currentText()),
            str(self.comboBoxRegionRight.currentText()),
            str(self.lineEditUserNameRight.text()),
            str(self.lineEditPasswordRight.text())
        ))

        # UI Buttons for Search API Tab
        self.pushButtonStartSearch.clicked.connect(lambda: self.runsearch(
            self.loadedapiurls[str(self.comboBoxRegionLeft.currentText())],
            str(self.lineEditUserNameLeft.text()),
            str(self.lineEditPasswordLeft.text())
        ))

    # method to reset all objects that are dependent on creds (such as collectors and content lists)
    def reset_stateful_objects(self, side='both'):

        self.collector.reset_stateful_objects(side)
        self.content.reset_stateful_objects(side)
        self.scheduled_view.reset_stateful_objects(side)
        self.field_extraction_rule.reset_stateful_objects(side)
        return

    def clear_creds(self):
        self.lineEditUserNameLeft.clear()
        self.lineEditUserNameRight.clear()
        self.lineEditPasswordLeft.clear()
        self.lineEditPasswordRight.clear()
        self.comboBoxPresetLeft.clear()
        self.comboBoxPresetRight.clear()


    # Start methods for Credential Database

    def createcredb(self):
        logger.info('Creating credential store')
        #check to see if there is already a dbfile and ask if it should be removed to create a new one
        db_file = pathlib.Path('credentials.db')
        if db_file.is_file():
            message = "It looks like you already have a credential database. Do you want to delete it (and it's passwords) and create a new one? If so type 'DELETE' in the box below:"
            text, result = QtWidgets.QInputDialog.getText(self, 'Warning!!', message)
            if (result and (str(text) == 'DELETE')):
                os.remove('credentials.db')
            else:
                return
        # get the password that will be used for the new database
        dialog = NewPasswordDialog()
        dialog.exec()
        dialog.show()
        if str(dialog.result()) == '1':
            password = dialog.getresults()
            if password:
                try:
                    # We pass a username here (from the config file) just in case someone has written their own
                    # version of the CredentialDB class that requires both a username/id AND password
                    # however the version distributed with sumologictoolbox ignores the username.
                    self.credentialstore = CredentialsDB(password, username=self.config['Credential Store']['username'], create_new=True)
                    # restrict permissions on the db file to just the user. May not be effective on Windows
                    os.chmod(str(db_file), 0o600)
                    self.cred_db_authenticated = True
                except Exception as e:
                    logger.exception(e)
                    self.errorbox("Something went wrong\n\n" + str(e))
                self.set_creddbbuttons()
                return
            else:
                return
        return

    def loadcreddb(self):
        logger.info('Loading credential store')
        db_file = pathlib.Path('credentials.db')
        if db_file.is_file():
            message = "Please enter your credentials database password."
            password, result = QtWidgets.QInputDialog.getText(self, 'Enter password', message, QtWidgets.QLineEdit.Password)
            if result:
                try:
                    # create the cred store instance
                    self.credentialstore = CredentialsDB(password)
                    self.cred_db_authenticated = True
                    # turn on the UI buttons
                    self.set_creddbbuttons()
                    # populate the preset dropdowns
                    self.populate_presets()
                    preset = self.comboBoxPresetLeft.currentText()
                    # load the first preset in the list (if it's there)
                    if preset:
                        self.load_preset(
                            preset,
                            self.comboBoxRegionLeft,
                            self.lineEditUserNameLeft,
                            self.lineEditPasswordLeft,
                            self.comboBoxPresetLeft,
                            'left'
                        )
                        self.load_preset(
                            preset,
                            self.comboBoxRegionRight,
                            self.lineEditUserNameRight,
                            self.lineEditPasswordRight,
                            self.comboBoxPresetLeft,
                            'right'
                        )
                    self.set_creddbbuttons()

                        
                except Exception as e:
                    logger.exception(e)
                    self.errorbox(str(e))
                    self.cred_db_authenticated = False
                    if hasattr(self, 'credentialstore'):
                        print('deleting credstore var')
                        del self.credentialstore
                    self.set_creddbbuttons()
                    self.reset_stateful_objects()
                return
            else:
                return
        else:
            self.errorbox("You don't appear to have a credentials database. You must create one first.")
            return
        return

    def deletecreddb(self):
        db_file = pathlib.Path('credentials.db')
        if db_file.is_file():
            message = '''
Do you really want to delete your credential database? 
If so type 'DELETE' in the box below:"

'''
            text, result = QtWidgets.QInputDialog.getText(self, 'Warning!!', message)
            if (result and (str(text) == 'DELETE')):
                os.remove(str(db_file))
                self.cred_db_authenticated = False
                del self.credentialstore
                self.clear_creds()
                self.set_creddbbuttons()

    def populate_presets(self):
        logger.info('Populating presets')
        self.comboBoxPresetLeft.clear()
        self.comboBoxPresetRight.clear()
        try:
            names = self.credentialstore.list_names()
            names = sorted(names,  key=str.lower)
            for name in names:
                self.comboBoxPresetLeft.addItem(name.strip())
                self.comboBoxPresetRight.addItem(name.strip())
        except Exception as e:
            logger.exception(e)
            self.errorbox('Something went wrong\n\n' + str(e))
        return

    def add_preset_to_combobox(self, preset):
        self.comboBoxPresetLeft.addItem(preset)
        self.comboBoxPresetRight.addItem(preset)
        return

    def remove_preset_from_combobox(self, preset):
        index = self.comboBoxPresetLeft.findText(preset)
        self.comboBoxPresetLeft.removeItem(index)
        index = self.comboBoxPresetRight.findText(preset)
        self.comboBoxPresetRight.removeItem(index)
        if self.comboBoxPresetLeft.count() is 0:
            self.clear_creds()
        return

    # call this at startup or cred db is created, opened, or deleted to set all the buttons appropriately
    # (also looks config file settings and which tab is selected.)
    # this works but it's a mess. There's gotta be a better way.
    def set_creddbbuttons(self):
        db_file = pathlib.Path('credentials.db')
        if db_file.is_file():
            db_file_exists = True
        else:
            db_file_exists = False
        # The search tab only uses the left credentials, so don't enable the right ones if we are in the search tab
        tab = self.tabWidget.currentIndex()
        if tab is 2:  # Index 2 from the tab widget is the search tab
            disable_right_cred__buttons = True
        else:
            disable_right_cred__buttons = False

        config_value = self.config['Credential Store']['credential_store_implementation']

        # Turn the left and right create preset buttons on or off depending on
        # 1. What our config file says
        # 2. If we've authenticated against a credential store
        # 3. For the right sight, whether we are in the search tab
        if (config_value == 'built_in') and \
                (self.cred_db_authenticated is True):

            self.pushButtonCreatePresetLeft.setEnabled(True)
            if disable_right_cred__buttons:
                self.pushButtonCreatePresetRight.setEnabled(False)
            else:
                self.pushButtonCreatePresetRight.setEnabled(True)

        else:
            self.pushButtonCreatePresetLeft.setEnabled(False)
            self.pushButtonCreatePresetRight.setEnabled(False)

        # Turn the left and right update preset buttons on or off depending on
        # 1. What our config file says
        # 2. If we've authenticated against a credential store
        # 3. For the right sight, whether we are in the search tab
        if (config_value == 'built_in') and \
                (self.cred_db_authenticated is True):

            self.pushButtonUpdatePresetLeft.setEnabled(True)
            if disable_right_cred__buttons:
                self.pushButtonUpdatePresetRight.setEnabled(False)
            else:
                self.pushButtonUpdatePresetRight.setEnabled(True)

        else:
            self.pushButtonUpdatePresetLeft.setEnabled(False)
            self.pushButtonUpdatePresetRight.setEnabled(False)

        # Turn the left and right delete preset buttons on or off depending on
        # 1. What our config file says
        # 2. If we've authenticated against a credential store
        # 3. For the right sight, whether we are in the search tab
        if (config_value == 'built_in') and \
                (self.cred_db_authenticated is True):

            self.pushButtonDeletePresetLeft.setEnabled(True)
            if disable_right_cred__buttons:
                self.pushButtonDeletePresetRight.setEnabled(False)
            else:
                self.pushButtonDeletePresetRight.setEnabled(True)

        else:
            self.pushButtonDeletePresetLeft.setEnabled(False)
            self.pushButtonDeletePresetRight.setEnabled(False)

        # Turn the left and right preset dropdowns depending on
        # 1. What our config file says
        # 2. If we've authenticated against a credential store
        # 3. For the right sight, whether we are in the search tab
        if (self.cred_db_authenticated is True) and\
                (config_value != 'none'):
            self.comboBoxPresetLeft.setEnabled(True)
            if disable_right_cred__buttons:
                self.comboBoxPresetRight.setEnabled(False)
            else:
                self.comboBoxPresetRight.setEnabled(True)
        else:
            self.comboBoxPresetLeft.setEnabled(False)
            self.comboBoxPresetRight.setEnabled(False)

        # Turn the create and delete cred DB buttons depending on
        # 1. What the config file says
        # 2. if a credentials.db file exists
        if (config_value == 'built_in'):
            if db_file_exists:
                self.pushButtonCreateCredentialDatabase.setEnabled(False)
                self.pushButtonDeleteCredentialDatabase.setEnabled(True)
            else:
                self.pushButtonCreateCredentialDatabase.setEnabled(True)
                self.pushButtonDeleteCredentialDatabase.setEnabled(False)
        else:
            self.pushButtonCreateCredentialDatabase.setEnabled(False)
            self.pushButtonDeleteCredentialDatabase.setEnabled(False)

        if (db_file_exists and config_value == 'built_in') or (config_value == 'read_only'):
            self.pushButtonLoadCredentialDatabase.setEnabled(True)
        else:
            self.pushButtonLoadCredentialDatabase.setEnabled(False)

        if config_value == 'none':
            self.pushButtonCreateCredentialDatabase.setEnabled(False)
            self.pushButtonLoadCredentialDatabase.setEnabled(False)
            self.pushButtonDeleteCredentialDatabase.setEnabled(False)

        return

    # called when the create preset button is clicked
    def create_preset(self, comboBoxRegion, lineEditUserName, lineEditPassword, comboBoxPreset, side):
        logger.info('Creating preset in credential store.')
        sumoregion = str(comboBoxRegion.currentText())
        accesskeyid = str(lineEditUserName.text())
        accesskey = str(lineEditPassword.text())
        message = "Please type a name for the new preset."
        preset, result = QtWidgets.QInputDialog.getText(self, 'Enter preset name', message)
        if result:
            if self.credentialstore.name_exists(preset):
                self.errorbox('That name already exists in the credential database. Choose a new name or use "Update" to modify an existing entry.')
                return
            else:
                try:
                    self.credentialstore.add_creds(preset, sumoregion, accesskeyid, accesskey)
                    self.add_preset_to_combobox(preset)
                    # index = comboBoxRegion.findText(preset, QtCore.Qt.MatchFixedString)
                    # if index >= 0:
                    #     comboBoxRegion.setCurrentIndex(index)
                    self.load_preset(preset, comboBoxRegion, lineEditUserName, lineEditPassword, comboBoxPreset, side)
                except Exception as e:
                    logger.exception(e)
                return
        return

    # This exists for an edge case. If there is only one entry in the preset list and the user edits/modifies
    # the cred text then clicking on the preset will not reload the cred because the index hasn't changed.
    # This solves this problem
    # called when the user selects an item from the preset dropdown
    def preset_activated(self, preset, comboBoxRegion, lineEditUserName, lineEditPassword, comboBoxPreset, side):
        if comboBoxPreset.count() is 1:
            self.load_preset(preset, comboBoxRegion, lineEditUserName, lineEditPassword, comboBoxPreset, side)

    # called when the preset combobox index changes
    def load_preset(self, preset, comboBoxRegion, lineEditUserName, lineEditPassword, comboBoxPreset, side):
        logger.info('Loading preset from credential store.')
        # even though we're about to load a new preset we should still clear the boxes in the eventuality
        # that the last preset was deleted and we've got nothing to load
        lineEditUserName.clear()
        lineEditPassword.clear()
        if comboBoxPreset.count() > 0:
            try:
                if self.credentialstore.name_exists(preset):
                    creds = self.credentialstore.get_creds(preset)
                    index = comboBoxPreset.findText(preset, QtCore.Qt.MatchFixedString)
                    if index >=0:
                        comboBoxPreset.setCurrentIndex(index)
                    index = comboBoxRegion.findText(creds['sumoregion'], QtCore.Qt.MatchFixedString)
                    if index >=0:
                        comboBoxRegion.setCurrentIndex(index)
                    lineEditUserName.setText(creds['accesskeyid'])
                    lineEditPassword.setText(creds['accesskey'])
                    # since we've changed the preset all of the stateful tabs need to be reset
                    # otherwise they will still be showing items from the previous preset
                    self.reset_stateful_objects(side=side)
                else:
                    raise Exception('That preset is not in the database.')
            except Exception as e:
                logger.exception(e)
                self.errorbox('Something went wrong\n\n' + str(e))

    # called when the delete preset button is clicked
    def delete_preset(self, preset, comboBoxRegion, lineEditUserName, lineEditPassword, comboBoxPreset, side):
        logger.info('Deleting preset from credential store.')
        if preset:
            if self.credentialstore.name_exists(preset):
                try:
                    result = self.credentialstore.delete_creds(preset)
                    self.remove_preset_from_combobox(preset)
                    preset = comboBoxPreset.currentText()
                    # load the first preset in the list (if it's there)
                    if preset:
                        self.load_preset(
                            preset,
                            comboBoxRegion,
                            lineEditUserName,
                            lineEditPassword,
                            comboBoxPreset,
                            side
                        )

                except Exception as e:
                    logger.exception(e)
                    self.errorbox('Something went wrong\n\n' + str(e))
            else:
                self.errorbox('Something went wrong. That preset does not exist in the database.')


    # called when the update preset button is clicked
    def update_preset(self, preset, sumoregion, accesskeyid, accesskey):
        logger.info('Updating preset in credential store.')
        if preset:
            if self.credentialstore.name_exists(preset):
                try:
                    result = self.credentialstore.update_creds(preset, sumoregion, accesskeyid, accesskey)
                except Exception as e:
                    logger.exception(e)
                    self.errorbox('Something went wrong\n\n' + str(e))
            else:
                self.errorbox('Something went wrong. That preset does not exist in the database.')
        return

    # Start Methods for Search Tab
    def runsearch(self, url, id, key):
        logger.info("Running a Search")
        self.tableWidgetSearchResults.clear()
        selectedtimezone = str(self.comboBoxTimeZone.currentText())
        timezone = pytz.timezone(selectedtimezone)
        starttime = str(self.dateTimeEditSearchStartTime.dateTime().toString(QtCore.Qt.ISODate))
        endtime = str(self.dateTimeEditSearchEndTime.dateTime().toString(QtCore.Qt.ISODate))
        searchstring = str(self.plainTextEditSearch.toPlainText())
        regexprog = re.compile(r'\S+')
        jobsubmitted = False
        csvheaderwritten = False
        savetofile = self.checkBoxSaveSearch.isChecked()
        converttimefromepoch = self.checkBoxConvertTimeFromEpoch.isChecked()
        jobmessages = []
        jobrecords = []
        if savetofile:
            filenameqstring, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save CSV', '', filter='*.csv')
            filename = str(filenameqstring)
            savefilepath = pathlib.Path(filename)

        if (re.match(regexprog, id) != None) and (re.match(regexprog, key) != None):
            sumo = SumoLogic(id, key, endpoint=url)

            if (re.match(regexprog, searchstring)) != None:
                try:
                    searchjob = sumo.search_job(searchstring, starttime, endtime, selectedtimezone)
                    jobsubmitted = True
                except Exception as e:
                    self.errorbox("Failed to submit search job. Check credentials, endpoint, and query.")
                    logger.exception(e)
                    return
                if jobsubmitted:
                    try:
                        self.labelSearchResultCount.setText('0')
                        jobstatus = sumo.search_job_status(searchjob)
                        nummessages = jobstatus['messageCount']
                        numrecords = jobstatus['recordCount']
                        self.labelSearchResultCount.setText(str(nummessages))
                        while jobstatus['state'] == 'GATHERING RESULTS':
                            jobstatus = sumo.search_job_status(searchjob)
                            numrecords = jobstatus['recordCount']
                            nummessages = jobstatus['messageCount']
                            self.labelSearchResultCount.setText(str(nummessages))
                        logger.info('Search Job finished. Downloading Results.')
                    except Exception as e:
                        logger.exception(e)
                        self.errorbox("Something went wrong\n\n" + str(e))
                    if nummessages is not 0:

                        # return messages
                        if self.buttonGroupOutputType.checkedId() == -2:
                            iterations = nummessages // 10000 + 1
                            try:
                                for iteration in range(1, iterations + 1):
                                    messages = sumo.search_job_messages(searchjob, limit=10000,
                                                                                   offset=((iteration - 1) * 10000))
                                    logger.info('Downloaded 1 block of messages.')
                                    if savetofile:
                                        logger.info('Saving messages to file.')
                                    for message in messages['messages']:
                                        if converttimefromepoch:
                                            converteddatetime = datetime.fromtimestamp(
                                                float(message['map']['_messagetime']) / 1000, timezone)
                                            timestring = str(converteddatetime.strftime('%Y-%m-%d %H:%M:%S'))
                                            message['map']['_messagetime'] = timestring
                                        if savetofile:  # If we save to file then append to output and let the messages
                                                        # variable get overwritten with the next batch of messages
                                                        # without saving them into the jobmessages variable
                                                        # So that we can conceptually download arbitrary amounts of data
                                                        # without running out of RAM
                                            if savefilepath:
                                                try:
                                                    with savefilepath.open(mode='a') as csvfile:
                                                        messagecsv = csv.DictWriter(csvfile,
                                                                                    message['map'].keys())
                                                        if csvheaderwritten == False:
                                                            messagecsv.writeheader()
                                                            csvheaderwritten = True
                                                        messagecsv.writerow(message['map'])
                                                except Exception as e:
                                                    self.errorbox("Failed writing. Check destination permissions.")
                                                    logger.exception(e)
                                                    return



                                        else:   # If we're not saving to file then keep the messages so that we can
                                                # display them in the table widget
                                            jobmessages.append(message)
                            except Exception as e:
                                logger.exception(e)
                                self.errorbox("Something went wrong\n\n" + str(e))
                            logger.info('Download complete.')
                            if savetofile:
                                self.infobox("Save to CSV complete.")
                                return
                            self.tableWidgetSearchResults.setRowCount(len(jobmessages))
                            self.tableWidgetSearchResults.setColumnCount(2)
                            self.tableWidgetSearchResults.setHorizontalHeaderLabels(['time', '_raw'])
                            index = 0
                            if len(jobmessages) > 0:
                                for message in jobmessages:
                                    self.tableWidgetSearchResults.setItem(index, 0, QtWidgets.QTableWidgetItem(
                                        message['map']['_messagetime']))
                                    self.tableWidgetSearchResults.setItem(index, 1,
                                                                          QtWidgets.QTableWidgetItem(message['map']['_raw']))
                                    index += 1
                                self.tableWidgetSearchResults.resizeRowsToContents()
                                self.tableWidgetSearchResults.resizeColumnsToContents()

                            else:
                                self.errorbox('Search did not return any messages.')
                                return
                        # return records
                        if self.buttonGroupOutputType.checkedId() == -3:
                            iterations = numrecords // 10000 + 1
                            try:
                                for iteration in range(1, iterations + 1):
                                    records = sumo.search_job_records(searchjob, limit=10000,
                                                                                 offset=((iteration - 1) * 10000))
                                    logger.info('Downloaded 1 block of records.')
                                    for record in records['records']:
                                         jobrecords.append(record)
                            except Exception as e:
                                logger.exception(e)
                                self.errorbox("Something went wrong\n\n" + str(e))
                            logger.info('Download complete.')
                            self.tableWidgetSearchResults.setRowCount(len(jobrecords))
                            numfields = len(records['fields'])
                            self.tableWidgetSearchResults.setColumnCount(numfields)
                            fieldnames = []
                            for field in records['fields']:
                                fieldnames.append(field['name'])
                            self.tableWidgetSearchResults.setHorizontalHeaderLabels(fieldnames)
                            index = 0
                            if len(jobrecords) > 0:
                                for record in jobrecords:
                                    columnnum = 0
                                    for fieldname in fieldnames:
                                        if converttimefromepoch and (fieldname == '_timeslice'):
                                            converteddatetime = datetime.fromtimestamp(
                                                float(record['map'][fieldname]) / 1000, timezone)
                                            timestring = str(converteddatetime.strftime('%Y-%m-%d %H:%M:%S'))
                                            record['map']['_timeslice'] = timestring
                                        self.tableWidgetSearchResults.setItem(index, columnnum, QtWidgets.QTableWidgetItem(
                                            record['map'][fieldname]))
                                        columnnum += 1
                                    index += 1
                                self.tableWidgetSearchResults.resizeRowsToContents()
                                self.tableWidgetSearchResults.resizeColumnsToContents()
                                if savetofile:
                                    logger.info('Saving records to file.')
                                    if savefilepath:
                                        try:
                                            with savefilepath.open(mode='w') as csvfile:
                                                recordcsv = csv.DictWriter(csvfile, jobrecords[0]['map'].keys())
                                                recordcsv.writeheader()
                                                for entry in jobrecords:
                                                    recordcsv.writerow(entry['map'])
                                        except Exception as e:
                                            self.errorbox("Failed writing. Check destination permissions.")
                                            logger.exception(e)
                                            return

                            else:
                                self.errorbox('Search did not return any records.')
                                return
                    else:
                        self.errorbox('Search did not return any messages.')
                        return

            else:
                self.errorbox('Please enter a search.')
                return
        else:
            self.errorbox('No user and/or password.')
        return


    # Start Methods for FER Tab
    

    # Start Misc/Utility Methods
    def tabchange(self, index):
        if index == 0:
            self.comboBoxRegionRight.setEnabled(False)
            self.lineEditUserNameRight.setEnabled(False)
            self.lineEditPasswordRight.setEnabled(False)
            self.pushButtonCreatePresetRight.setEnabled(False)
            self.pushButtonUpdatePresetRight.setEnabled(False)
            self.pushButtonDeletePresetRight.setEnabled(False)
            self.comboBoxPresetRight.setEnabled(False)

        else:
            self.comboBoxRegionRight.setEnabled(True)
            self.lineEditUserNameRight.setEnabled(True)
            self.lineEditPasswordRight.setEnabled(True)
            if self.cred_db_authenticated:
                self.pushButtonCreatePresetRight.setEnabled(True)
                self.pushButtonUpdatePresetRight.setEnabled(True)
                self.pushButtonDeletePresetRight.setEnabled(True)
                self.comboBoxPresetRight.setEnabled(True)
            else:
                self.pushButtonCreatePresetRight.setEnabled(False)
                self.pushButtonUpdatePresetRight.setEnabled(False)
                self.pushButtonDeletePresetRight.setEnabled(False)
                self.comboBoxPresetRight.setEnabled(False)
        return

    def errorbox(self, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle('Error')
        msgBox.setText(message)
        msgBox.addButton(QtWidgets.QPushButton('OK'), QtWidgets.QMessageBox.RejectRole)
        ret = msgBox.exec_()
        return

    def infobox(self, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle('Info')
        msgBox.setText(message)
        msgBox.addButton(QtWidgets.QPushButton('OK'), QtWidgets.QMessageBox.RejectRole)
        ret = msgBox.exec_()
        return

    def initModels(self):
        # Load API Endpoint List from file and create model for the comboboxes
        # The join/split trickery clears white space from the text before it's processed by json.loads
        # so that we don't get extra spacing and weirdness
        self.loadedapiurls = json.loads("".join(self.config['API']['api_endpoints'].split()))
        self.apiurlsmodel = QtGui.QStandardItemModel()
        for key in self.loadedapiurls:
            text_item = QtGui.QStandardItem(key)
            self.apiurlsmodel.appendRow(text_item)

        self.comboBoxRegionLeft.setModel(self.apiurlsmodel)
        self.comboBoxRegionRight.setModel(self.apiurlsmodel)

        # Load Timezones and create model for timezone combobox

        self.timezonemodel = QtGui.QStandardItemModel()
        for zone in pytz.common_timezones:
            text_item = QtGui.QStandardItem(zone)
            self.timezonemodel.appendRow(text_item)

        self.comboBoxTimeZone.setModel(self.timezonemodel)

        # set search start and endtimes to now-ish
        self.dateTimeEditSearchStartTime.setDateTime(QtCore.QDateTime.currentDateTime().addSecs(-900))
        self.dateTimeEditSearchEndTime.setDateTime(QtCore.QDateTime.currentDateTime())

        # set timezone combobox to local timezone
        localtimezone = str(get_localzone())
        index = self.comboBoxTimeZone.findText(localtimezone, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.comboBoxTimeZone.setCurrentIndex(index)
        return

    def init_and_load_config_file(self):

        config_file = pathlib.Path('sumotoolbox.ini')
        if not config_file.is_file():
            # If the config file doesn't exist then we need to create a new one. This should only happen
            # when running the pyinstaller executable version.
            # get the copy that's hidden inside the executable archive and copy it to the current dir
            source_file = pathlib.Path(self.basedir + '/data/sumotoolbox.ini')
            shutil.copy(str(source_file), str(config_file))
        self.config = configparser.ConfigParser()
        self.config.read(str(config_file))
        return


    def change_logging_level(self):
        level = self.loggingmenugroup.checkedAction()
        if level.text() == "Informational":
            logzero.loglevel(level=20)
        elif level.text() == "Debug":
            logzero.loglevel(level=10)

    def change_theme(self):
        theme = self.thememenugroup.checkedAction()
        if theme.text() == "Dark":
            qtmodern.styles.dark(QtWidgets.QApplication.instance())
        elif theme.text() == "Light":
            qtmodern.styles.light(QtWidgets.QApplication.instance())



    def setup_menus(self):

        # setup the logging level menu
        self.loggingmenugroup = QtWidgets.QActionGroup(self, exclusive=True)
        self.loggingmenugroup.addAction(self.actionInformational)
        self.loggingmenugroup.addAction(self.actionDebug)
        self.loggingmenugroup.triggered.connect(self.change_logging_level)
        # setup the theme selector
        self.thememenugroup = QtWidgets.QActionGroup(self, exclusive=True)
        self.thememenugroup.addAction(self.actionLight)
        self.thememenugroup.addAction(self.actionDark)
        self.thememenugroup.triggered.connect(self.change_theme)
        # setup the version menu
        self.actionVersion.triggered.connect(lambda: self.infobox("Version: " + __version__))

    # End Misc/Utility Methods

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    # This loads the splash screen
    start = time.time()
    splash_pix = QtGui.QPixmap(os.path.join(basedir, 'data/sumotoolbox_logo_small.png'))
    splash = QtWidgets.QSplashScreen(splash_pix)
    splash.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
    splash.show()
    # Wait a little bit to keep the splash screen up before closing it
    while time.time() - start < 1:
        time.sleep(0.001)
        app.processEvents()

    # Load the stylesheet to make the GUI pretty
    qtmodern.styles.dark(app)

    window = qtmodern.windows.ModernWindow(sumotoolbox())
    # Close the splash screen and transition to the main UI
    splash.finish(window)


    window.show()

    sys.exit(app.exec_())
