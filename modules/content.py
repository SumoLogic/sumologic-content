from qtpy import QtCore, QtGui, QtWidgets, uic
import os
import sys
import pathlib
import json
from logzero import logger
from modules.sumologic import SumoLogic
from modules.dialogs import findReplaceCopyDialog

class content_tab(QtWidgets.QWidget):

    def __init__(self, mainwindow):

        super(content_tab, self).__init__()
        self.mainwindow = mainwindow
       

        scheduled_view_widget_ui = os.path.join(self.mainwindow.basedir, 'data/content.ui')
        uic.loadUi(scheduled_view_widget_ui, self)

        # Load icons used in the listviews
        self.load_icons()
        # set up some variables to identify the content list widgets. This is read by some of the content methods
        # to determine proper course of action
        self.contentListWidgetLeft.side = 'left'
        self.contentListWidgetRight.side = 'right'

        # Content Pane Signals
        # Left Side
        self.pushButtonUpdateContentLeft.clicked.connect(lambda: self.updatecontentlist(
            self.contentListWidgetLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text()),
            self.buttonGroupContentLeft.checkedId(),
            self.contentCurrentDirLabelLeft
        ))

        self.contentListWidgetLeft.itemDoubleClicked.connect(lambda item: self.doubleclickedcontentlist(
            item,
            self.contentListWidgetLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text()),
            self.buttonGroupContentLeft.checkedId(),
            self.contentCurrentDirLabelLeft
        ))

        self.pushButtonParentDirContentLeft.clicked.connect(lambda: self.parentdircontentlist(
            self.contentListWidgetLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text()),
            self.buttonGroupContentLeft.checkedId(),
            self.contentCurrentDirLabelLeft
        ))

        self.buttonGroupContentLeft.buttonClicked.connect(lambda: self.contentradiobuttonchanged(
            self.contentListWidgetLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text()),
            self.buttonGroupContentLeft.checkedId(),
            self.contentCurrentDirLabelLeft,
            self.pushButtonContentDeleteLeft
        ))

        self.pushButtonContentNewFolderLeft.clicked.connect(lambda: self.create_folder(
            self.contentListWidgetLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text()),
            self.buttonGroupContentLeft.checkedId(),
            self.contentCurrentDirLabelLeft
        ))

        self.pushButtonContentDeleteLeft.clicked.connect(lambda: self.delete_content(
            self.contentListWidgetLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text()),
            self.buttonGroupContentLeft.checkedId(),
            self.contentCurrentDirLabelLeft
        ))

        self.pushButtonContentCopyLeftToRight.clicked.connect(lambda: self.copycontent(
            self.contentListWidgetLeft,
            self.contentListWidgetRight,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text()),
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text()),
            self.buttonGroupContentLeft.checkedId(),
            self.buttonGroupContentRight.checkedId(),
            self.contentCurrentDirLabelRight
        ))

        self.pushButtonContentFindReplaceCopyLeftToRight.clicked.connect(lambda: self.findreplacecopycontent(
            self.contentListWidgetLeft,
            self.contentListWidgetRight,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text()),
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text()),
            self.buttonGroupContentLeft.checkedId(),
            self.buttonGroupContentRight.checkedId(),
            self.contentCurrentDirLabelRight
        ))

        # Right Side
        self.pushButtonUpdateContentRight.clicked.connect(lambda: self.updatecontentlist(
            self.contentListWidgetRight,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text()),
            self.buttonGroupContentRight.checkedId(),
            self.contentCurrentDirLabelRight
        ))

        self.contentListWidgetRight.itemDoubleClicked.connect(lambda item: self.doubleclickedcontentlist(
            item,
            self.contentListWidgetRight,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text()),
            self.buttonGroupContentRight.checkedId(),
            self.contentCurrentDirLabelRight
        ))

        self.pushButtonParentDirContentRight.clicked.connect(lambda: self.parentdircontentlist(
            self.contentListWidgetRight,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text()),
            self.buttonGroupContentRight.checkedId(),
            self.contentCurrentDirLabelRight
        ))

        self.buttonGroupContentRight.buttonClicked.connect(lambda: self.contentradiobuttonchanged(
            self.contentListWidgetRight,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text()),
            self.buttonGroupContentRight.checkedId(),
            self.contentCurrentDirLabelRight,
            self.pushButtonContentDeleteRight
        ))

        self.pushButtonContentNewFolderRight.clicked.connect(lambda: self.create_folder(
            self.contentListWidgetRight,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text()),
            self.buttonGroupContentRight.checkedId(),
            self.contentCurrentDirLabelRight
        ))

        self.pushButtonContentDeleteRight.clicked.connect(lambda: self.delete_content(
            self.contentListWidgetRight,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text()),
            self.buttonGroupContentRight.checkedId(),
            self.contentCurrentDirLabelRight
        ))

        self.pushButtonContentCopyRightToLeft.clicked.connect(lambda: self.copycontent(
            self.contentListWidgetRight,
            self.contentListWidgetLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text()),
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text()),
            self.buttonGroupContentRight.checkedId(),
            self.buttonGroupContentLeft.checkedId(),
            self.contentCurrentDirLabelLeft
        ))

        self.pushButtonContentFindReplaceCopyRightToLeft.clicked.connect(lambda: self.findreplacecopycontent(
            self.contentListWidgetRight,
            self.contentListWidgetLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text()),
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text()),
            self.buttonGroupContentRight.checkedId(),
            self.buttonGroupContentLeft.checkedId(),
            self.contentCurrentDirLabelLeft
        ))

        self.pushButtonContentBackupLeft.clicked.connect(lambda: self.backupcontent(
            self.contentListWidgetLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text()),
            self.buttonGroupContentLeft.checkedId()
        ))

        self.pushButtonContentBackupRight.clicked.connect(lambda: self.backupcontent(
            self.contentListWidgetRight,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text()),
            self.buttonGroupContentRight.checkedId()
        ))

        self.pushButtonContentRestoreLeft.clicked.connect(lambda: self.restorecontent(
            self.contentListWidgetLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text()),
            self.buttonGroupContentLeft.checkedId(),
            self.contentCurrentDirLabelLeft
        ))

        self.pushButtonContentRestoreRight.clicked.connect(lambda: self.restorecontent(
            self.contentListWidgetRight,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text()),
            self.buttonGroupContentRight.checkedId(),
            self.contentCurrentDirLabelRight
        ))
        
    def reset_stateful_objects(self, side='both'):

        if side == 'both':
            left = True
            right = True
        if side == 'left':
            left = True
            right = False
        if side == 'right':
            left = False
            right = True

        if left:
            self.contentListWidgetLeft.clear()
            self.contentListWidgetLeft.currentcontent = {}
            self.contentListWidgetLeft.currentdirlist = []
            self.contentListWidgetLeft.updated = False


        if right:
            self.contentListWidgetRight.clear()
            self.contentListWidgetRight.currentcontent = {}
            self.contentListWidgetRight.currentdirlist = []
            self.contentListWidgetRight.updated = False

    def load_icons(self):

        self.icons = {}
        iconpath = str(pathlib.Path(self.mainwindow.basedir + '/data/folder.svg'))
        self.icons['Folder'] = QtGui.QIcon(iconpath)
        iconpath = str(pathlib.Path(self.mainwindow.basedir + '/data/dashboard.svg'))
        self.icons['Dashboard'] = QtGui.QIcon(iconpath)
        iconpath = str(pathlib.Path(self.mainwindow.basedir + '/data/logsearch.svg'))
        self.icons['Search'] = QtGui.QIcon(iconpath)
        iconpath = str(pathlib.Path(self.mainwindow.basedir + '/data/scheduledsearch.svg'))
        self.icons['scheduledsearch'] = QtGui.QIcon(iconpath)
        iconpath = str(pathlib.Path(self.mainwindow.basedir + '/data/correlationrules.svg'))
        self.icons['Rule'] = QtGui.QIcon(iconpath)
        iconpath = str(pathlib.Path(self.mainwindow.basedir + '/data/informationmodel.svg'))
        self.icons['Model'] = QtGui.QIcon(iconpath)
        iconpath = str(pathlib.Path(self.mainwindow.basedir + '/data/lookuptable.svg'))
        self.icons['Lookups'] = QtGui.QIcon(iconpath)
        iconpath = str(pathlib.Path(self.mainwindow.basedir + '/data/parser.svg'))
        self.icons['Parser'] = QtGui.QIcon(iconpath)
        return

    # Start methods for Content Tab

    def findreplacecopycontent(self, ContentListWidgetFrom, ContentListWidgetTo, fromurl, fromid, fromkey, tourl,
                               toid, tokey,
                               fromradioselected, toradioselected, todirectorylabel):

        logger.info("Copying Content")

        selecteditemsfrom = ContentListWidgetFrom.selectedItems()
        if toradioselected == -3 or toradioselected == -4:  # Admin or Global folders selected
            toadminmode = True
        else:
            toadminmode = False
        if fromradioselected == -3 or fromradioselected == -4:  # Admin or Global folders selected
            fromadminmode = True
        else:
            fromadminmode = False
        if len(selecteditemsfrom) > 0:  # make sure something was selected
            try:
                exportsuccessful = False
                fromsumo = SumoLogic(fromid, fromkey, endpoint=fromurl)
                tosumo = SumoLogic(toid, tokey, endpoint=tourl)

                contents = []
                for selecteditem in selecteditemsfrom:
                    for child in ContentListWidgetFrom.currentcontent['children']:
                        if child['name'] == str(selecteditem.text()):
                            item_id = child['id']
                            contents.append(fromsumo.export_content_job_sync(item_id, adminmode=fromadminmode))
                            exportsuccessful = True
            except Exception as e:
                logger.exception(e)
                self.mainwindow.errorbox('Something went wrong with the Source:\n\n' + str(e))
                return
            if exportsuccessful:
                categoriesfrom = []
                for content in contents:
                    contentstring = json.dumps(content)
                    categoriesfrom = categoriesfrom + re.findall(r'\"_sourceCategory\s*=\s*\\?\"?([^\s\\|]*)',
                                                                 contentstring)
                uniquecategoriesfrom = list(set(categoriesfrom))  # dedupe the list
                try:
                    fromtime = str(QtCore.QDateTime.currentDateTime().addSecs(-3600).toString(QtCore.Qt.ISODate))
                    totime = str(QtCore.QDateTime.currentDateTime().toString(QtCore.Qt.ISODate))

                    query = r'* | count by _sourceCategory | fields _sourceCategory'
                    searchresults = tosumo.search_job_records_sync(query, fromTime=fromtime, toTime=totime,
                                                                   timeZone='UTC', byReceiptTime='false')
                    categoriesto = []
                    for record in searchresults:
                        categoriesto.append(record['map']['_sourcecategory'])
                    uniquecategoriesto = list(set(categoriesto))

                except Exception as e:
                    logger.exception(e)
                    self.mainwindow.errorbox('Something went wrong with the Destination:\n\n' + str(e))
                    return
                dialog = findReplaceCopyDialog(uniquecategoriesfrom, uniquecategoriesto)
                dialog.exec()
                dialog.show()
                if str(dialog.result()) == '1':
                    replacelist = dialog.getresults()
                    logger.info(replacelist)
                    if len(replacelist) > 0:
                        newcontents = []
                        for content in contents:
                            for entry in replacelist:
                                contentstring = json.dumps(content)
                                contentstring = contentstring.replace(str(entry['from']), str(entry['to']))
                                logger.info(contentstring)
                                newcontents.append(json.loads(contentstring))
                    else:
                        newcontents = contents

                    try:
                        tofolderid = ContentListWidgetTo.currentcontent['id']
                        for newcontent in newcontents:
                            status = tosumo.import_content_job_sync(tofolderid, newcontent, adminmode=toadminmode)
                        self.updatecontentlist(ContentListWidgetTo, tourl, toid, tokey, toradioselected,
                                               todirectorylabel)
                        return
                    except Exception as e:
                        logger.exception(e)
                        self.mainwindow.errorbox('Something went wrong with the Destination:\n\n' + str(e))
                        return
                else:
                    return



        else:
            self.mainwindow.errorbox('You have not made any selections.')
            return
        return

    def copycontent(self, ContentListWidgetFrom, ContentListWidgetTo, fromurl, fromid, fromkey, tourl, toid, tokey,
                    fromradioselected, toradioselected, todirectorylabel):
        logger.info("Copying Content")
        if toradioselected == -3 or toradioselected == -4:  # Admin or Global folders selected
            toadminmode = True
        else:
            toadminmode = False
        if fromradioselected == -3 or fromradioselected == -4:  # Admin or Global folders selected
            fromadminmode = True
        else:
            fromadminmode = False

        try:
            selecteditems = ContentListWidgetFrom.selectedItems()
            if len(selecteditems) > 0:  # make sure something was selected
                fromsumo = SumoLogic(fromid, fromkey, endpoint=fromurl)
                tosumo = SumoLogic(toid, tokey, endpoint=tourl)
                currentdir = ContentListWidgetTo.currentdirlist[-1]
                tofolderid = ContentListWidgetTo.currentcontent['id']
                for selecteditem in selecteditems:
                    for child in ContentListWidgetFrom.currentcontent['children']:
                        if child['name'] == str(selecteditem.text()):
                            item_id = child['id']
                            content = fromsumo.export_content_job_sync(item_id, adminmode=fromadminmode)
                            status = tosumo.import_content_job_sync(tofolderid, content, adminmode=toadminmode)
                            self.updatecontentlist(ContentListWidgetTo, tourl, toid, tokey, toradioselected,
                                                   todirectorylabel)
                return

            else:
                self.mainwindow.errorbox('You have not made any selections.')
                return

        except Exception as e:
            logger.exception(e)
            self.mainwindow.errorbox('Something went wrong:\n\n' + str(e))
        return

    def create_folder(self, ContentListWidget, url, id, key, radioselected, directorylabel):
        if ContentListWidget.updated == True:
            if radioselected == -3 or radioselected == -4:  # Admin or Global folders selected
                adminmode = True
            else:
                adminmode = False

            message = '''
        Please enter the name of the folder you wish to create:

                        '''
            text, result = QtWidgets.QInputDialog.getText(self, 'Create Folder...', message)
            if result:
                for item in ContentListWidget.currentcontent['children']:
                    if item['name'] == str(text):
                        self.mainwindow.errorbox('That Directory Name Already Exists!')
                        return
                try:

                    logger.info("Creating New Folder in Personal Folder Tree")
                    sumo = SumoLogic(id, key, endpoint=url)
                    error = sumo.create_folder(str(text), str(ContentListWidget.currentcontent['id']),
                                               adminmode=adminmode)

                    self.updatecontentlist(ContentListWidget, url, id, key, radioselected, directorylabel)
                    return

                except Exception as e:
                    logger.exception(e)
                    self.mainwindow.errorbox('Something went wrong:\n\n' + str(e))

        else:
            self.mainwindow.errorbox("Please update the directory list before trying to create a new folder.")
        return

    def delete_content(self, ContentListWidget, url, id, key, radioselected, directorylabel):
        logger.info("Deleting Content")
        if radioselected == -3 or radioselected == -4:  # Admin or Global folders selected
            adminmode = True
        else:
            adminmode = False

        selecteditems = ContentListWidget.selectedItems()
        if len(selecteditems) > 0:  # make sure something was selected
            message = "You are about to delete the following item(s):\n\n"
            for selecteditem in selecteditems:
                message = message + str(selecteditem.text()) + "\n"
            message = message + '''
This is exceedingly DANGEROUS!!!! 
Please be VERY, VERY, VERY sure you want to do this!
You could lose quite a bit of work if you delete the wrong thing(s).

If you are absolutely sure, type "DELETE" in the box below.

                    '''
            text, result = QtWidgets.QInputDialog.getText(self, 'Warning!!', message)
            if (result and (str(text) == 'DELETE')):
                try:
                    sumo = SumoLogic(id, key, endpoint=url)
                    for selecteditem in selecteditems:

                        for child in ContentListWidget.currentcontent['children']:
                            if child['name'] == str(selecteditem.text()):
                                item_id = child['id']

                        result = sumo.delete_content_job_sync(item_id, adminmode=adminmode)

                    self.updatecontentlist(ContentListWidget, url, id, key, radioselected, directorylabel)
                    return


                except Exception as e:
                    logger.exception(e)
                    self.mainwindow.errorbox('Something went wrong:\n\n' + str(e))

        else:
            self.mainwindow.errorbox('You need to select something before you can delete it.')
        return

    def contentradiobuttonchanged(self, ContentListWidget, url, id, key, radioselected, directorylabel,
                                  pushButtonContentDelete):
        ContentListWidget.currentdirlist = []
        self.updatecontentlist(ContentListWidget, url, id, key, radioselected, directorylabel)
        return

    def togglecontentbuttons(self, side, state):
        if side == 'left':
            self.pushButtonContentCopyRightToLeft.setEnabled(state)
            self.pushButtonContentFindReplaceCopyRightToLeft.setEnabled(state)
            self.pushButtonContentNewFolderLeft.setEnabled(state)
            self.pushButtonContentDeleteLeft.setEnabled(state)
            self.pushButtonContentBackupLeft.setEnabled(state)
            self.pushButtonContentRestoreLeft.setEnabled(state)
        elif side == 'right':
            self.pushButtonContentCopyLeftToRight.setEnabled(state)
            self.pushButtonContentFindReplaceCopyLeftToRight.setEnabled(state)
            self.pushButtonContentNewFolderRight.setEnabled(state)
            self.pushButtonContentDeleteRight.setEnabled(state)
            self.pushButtonContentBackupRight.setEnabled(state)
            self.pushButtonContentRestoreRight.setEnabled(state)

    def updatecontentlist(self, ContentListWidget, url, id, key, radioselected, directorylabel):
        sumo = SumoLogic(id, key, endpoint=url)
        if ContentListWidget.currentdirlist:
            currentdir = ContentListWidget.currentdirlist[-1]
        else:
            currentdir = {'name': None, 'id': 'TOP'}

        try:
            if (not ContentListWidget.currentcontent) or (currentdir['id'] == 'TOP'):
                if radioselected == -2:  # if "Personal Folder" radio button is selected
                    logger.info("Updating Personal Folder List")
                    ContentListWidget.currentcontent = sumo.get_personal_folder()

                    ContentListWidget.currentdirlist = []
                    dir = {'name': 'Personal Folder', 'id': 'TOP'}
                    ContentListWidget.currentdirlist.append(dir)
                    if 'children' in ContentListWidget.currentcontent:
                        self.updatecontentlistwidget(ContentListWidget, url, id, key, radioselected, directorylabel)

                    else:
                        self.mainwindow.errorbox('Incorrect Credentials or Wrong Endpoint.')

                elif radioselected == -3:  # if "Global Folders" radio button is selected
                    logger.info("Updating Global Folder List")
                    ContentListWidget.currentcontent = sumo.get_global_folder_sync(adminmode=True)

                    # Rename dict key from "data" to "children" for consistency
                    ContentListWidget.currentcontent['children'] = ContentListWidget.currentcontent.pop('data')
                    ContentListWidget.currentdirlist = []
                    dir = {'name': 'Global Folders', 'id': 'TOP'}
                    ContentListWidget.currentdirlist.append(dir)
                    if 'children' in ContentListWidget.currentcontent:
                        self.updatecontentlistwidget(ContentListWidget, url, id, key, radioselected, directorylabel)

                    else:
                        self.mainwindow.errorbox('Incorrect Credentials or Wrong Endpoint.')

                else:  # "Admin Folders" must be selected
                    logger.info("Updating Admin Folder List")
                    ContentListWidget.currentcontent = sumo.get_admin_folder_sync(adminmode=False)

                    ContentListWidget.currentdirlist = []
                    dir = {'name': 'Admin Recommended', 'id': 'TOP'}
                    ContentListWidget.currentdirlist.append(dir)
                    if 'children' in ContentListWidget.currentcontent:
                        self.updatecontentlistwidget(ContentListWidget, url, id, key, radioselected, directorylabel)

                    else:
                        self.mainwindow.errorbox('Incorrect Credentials or Wrong Endpoint.')



            else:
                ContentListWidget.currentcontent = sumo.get_folder(currentdir['id'])
                self.updatecontentlistwidget(ContentListWidget, url, id, key, radioselected, directorylabel)



        except Exception as e:
            logger.exception(e)
            self.mainwindow.errorbox('Something went wrong:\n\n' + str(e))
            return

        return

    def doubleclickedcontentlist(self, item, ContentListWidget, url, id, key, radioselected, directorylabel):
        logger.info("Going Down One Content Folder")
        sumo = SumoLogic(id, key, endpoint=url)
        currentdir = ContentListWidget.currentdirlist[-1]
        if radioselected == -3:
            adminmode = True
        else:
            adminmode = False
        try:
            for child in ContentListWidget.currentcontent['children']:
                if (child['name'] == item.text()) and (child['itemType'] == 'Folder'):
                    ContentListWidget.currentcontent = sumo.get_folder(child['id'], adminmode=adminmode)

                    dir = {'name': item.text(), 'id': child['id']}
                    ContentListWidget.currentdirlist.append(dir)

        except Exception as e:
            logger.exception(e)
            self.mainwindow.errorbox('Something went wrong:\n\n' + str(e))
        self.updatecontentlistwidget(ContentListWidget, url, id, key, radioselected, directorylabel)

    def parentdircontentlist(self, ContentListWidget, url, id, key, radioselected, directorylabel):
        if ContentListWidget.updated:
            logger.info("Going Up One Content Folder")
            sumo = SumoLogic(id, key, endpoint=url)
            currentdir = ContentListWidget.currentdirlist[-1]
            if currentdir['id'] != 'TOP':
                parentdir = ContentListWidget.currentdirlist[-2]
            else:
                return
            try:

                if parentdir['id'] == 'TOP':
                    ContentListWidget.currentdirlist = []
                    self.updatecontentlist(ContentListWidget, url, id, key, radioselected, directorylabel)
                    return

                else:
                    ContentListWidget.currentdirlist.pop()
                    ContentListWidget.currentcontent = sumo.get_folder(parentdir['id'])

                    self.updatecontentlist(ContentListWidget, url, id, key, radioselected, directorylabel)
                    return
            except Exception as e:
                logger.exception(e)
                self.mainwindow.errorbox('Something went wrong:\n\n' + str(e))

            return

    def updatecontentlistwidget(self, ContentListWidget, url, id, key, radioselected, directorylabel):
        try:
            ContentListWidget.clear()
            sumo = SumoLogic(id, key, endpoint=url)
            for object in ContentListWidget.currentcontent['children']:
                item_name = ''
                # if radioselected == -3:
                #     logger.info("Getting User info for Global Folder")
                #     user_info = sumo.get_user(object['createdBy'])
                #     item_name = '[' + user_info['firstName'] + ' ' + user_info['lastName'] + ']'
                item_name = item_name + object['name']
                if object['itemType'] == 'Folder':
                    item = QtWidgets.QListWidgetItem(self.icons['Folder'], item_name)
                    item.setIcon(self.icons['Folder'])
                    ContentListWidget.addItem(item)  # populate the list widget in the GUI
                elif object['itemType'] == 'Search':
                    item = QtWidgets.QListWidgetItem(self.icons['Search'], item_name)
                    item.setIcon(self.icons['Search'])
                    ContentListWidget.addItem(item)  # populate the list widget in the GUI
                elif object['itemType'] == 'Dashboard':
                    item = QtWidgets.QListWidgetItem(self.icons['Dashboard'], item_name)
                    item.setIcon(self.icons['Dashboard'])
                    ContentListWidget.addItem(item)  # populate the list widget in the GUI
                elif object['itemType'] == 'Lookups':
                    item = QtWidgets.QListWidgetItem(self.icons['Dashboard'], item_name)
                    item.setIcon(self.icons['Lookups'])
                    ContentListWidget.addItem(item)  # populate the list widget in the GUI
                else:
                    ContentListWidget.addItem(
                        item_name)  # populate the list widget in the GUI with no icon (fallthrough)

            dirname = ''
            for dir in ContentListWidget.currentdirlist:
                dirname = dirname + '/' + dir['name']
            directorylabel.setText(dirname)
            ContentListWidget.updated = True
            # if we are in the root (Top) of the global folders then we can't manipulate stuff as the entries are actually users, not content
            # so turn off the buttons until we change folder type or move down a level
            currentdir = ContentListWidget.currentdirlist[-1]
            if currentdir['id'] == 'TOP' and radioselected == -3:
                self.togglecontentbuttons(ContentListWidget.side, False)
            else:
                self.togglecontentbuttons(ContentListWidget.side, True)

        except Exception as e:
            logger.exception(e)
        return

    def backupcontent(self, ContentListWidget, url, id, key, radioselected):
        logger.info("Backing Up Content")
        if radioselected == -3 or radioselected == -4:  # Admin or Global folders selected
            adminmode = True
        else:
            adminmode = False
        selecteditems = ContentListWidget.selectedItems()
        if len(selecteditems) > 0:  # make sure something was selected
            savepath = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Backup Directory"))
            if os.access(savepath, os.W_OK):
                message = ''
                sumo = SumoLogic(id, key, endpoint=url)
                for selecteditem in selecteditems:
                    for child in ContentListWidget.currentcontent['children']:
                        if child['name'] == str(selecteditem.text()):
                            item_id = child['id']
                            try:
                                content = sumo.export_content_job_sync(item_id, adminmode=adminmode)
                                savefilepath = pathlib.Path(savepath + r'/' + str(selecteditem.text()) + r'.json')
                                if savefilepath:
                                    with savefilepath.open(mode='w') as filepointer:
                                        json.dump(content, filepointer)
                                    message = message + str(selecteditem.text()) + r'.json' + '\n'
                            except Exception as e:
                                logger.exception(e)
                                self.mainwindow.errorbox('Something went wrong:\n\n' + str(e))
                                return
                self.mainwindow.infobox('Wrote files: \n\n' + message)
            else:
                self.mainwindow.errorbox("You don't have permissions to write to that directory")

        else:
            self.mainwindow.errorbox('No content selected.')
        return

    def restorecontent(self, ContentListWidget, url, id, key, radioselected, directorylabel):
        logger.info("Restoring Content")
        if ContentListWidget.updated == True:
            if 'id' in ContentListWidget.currentcontent:  # make sure the current folder has a folder id
                filter = "JSON (*.json)"
                filelist, status = QtWidgets.QFileDialog.getOpenFileNames(self, "Open file(s)...", os.getcwd(),
                                                                          filter)
                if len(filelist) > 0:
                    sumo = SumoLogic(id, key, endpoint=url)
                    for file in filelist:
                        try:
                            with open(file) as filepointer:
                                content = json.load(filepointer)


                        except Exception as e:
                            logger.exception(e)
                            self.mainwindow.errorbox(
                                "Something went wrong reading the file. Do you have the right file permissions? Does it contain valid JSON?")
                            return
                        try:
                            folder_id = ContentListWidget.currentcontent['id']
                            if radioselected == -4 or radioselected == -3:  # Admin Recommended Folders or Global folders Selected
                                adminmode = True
                            else:
                                adminmode = False
                            sumo.import_content_job_sync(folder_id, content, adminmode=adminmode)
                        except Exception as e:
                            logger.exception(e)
                            self.mainwindow.errorbox('Something went wrong:\n\n' + str(e))
                            return
                    self.updatecontentlist(ContentListWidget, url, id, key, radioselected, directorylabel)


            else:
                self.mainwindow.errorbox("You can't restore content to this folder. Does it belong to another user?")
                return
        else:
            self.mainwindow.errorbox("Please update the directory list before restoring content")
        return