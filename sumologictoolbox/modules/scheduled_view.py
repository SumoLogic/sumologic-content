from qtpy import QtWidgets, uic
import os
import sys
import pathlib
import json
from logzero import logger
from datetime import datetime, timezone
from modules.sumologic import SumoLogic

class scheduled_view_tab(QtWidgets.QWidget):

    def __init__(self, mainwindow):

        super(scheduled_view_tab, self).__init__()
        self.mainwindow = mainwindow

        scheduled_view_widget_ui = os.path.join(self.mainwindow.basedir, 'data/scheduled_view.ui')
        uic.loadUi(scheduled_view_widget_ui, self)

        self.pushButtonUpdateSVLeft.clicked.connect(lambda: self.update_SV_list(
            self.SVListWidgetLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text())
        ))

        self.pushButtonUpdateSVRight.clicked.connect(lambda: self.update_SV_list(
            self.SVListWidgetRight,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text())
        ))

        self.pushButtonSVDeleteLeft.clicked.connect(lambda: self.delete_scheduled_view(
            self.SVListWidgetLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text())
        ))

        self.pushButtonSVDeleteRight.clicked.connect(lambda: self.delete_scheduled_view(
            self.SVListWidgetRight,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text())
        ))

        self.pushButtonSVCopyLeftToRight.clicked.connect(lambda: self.copy_scheduled_view(
            self.SVListWidgetLeft,
            self.SVListWidgetRight,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text()),
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text())
        ))

        self.pushButtonSVCopyRightToLeft.clicked.connect(lambda: self.copy_scheduled_view(
            self.SVListWidgetRight,
            self.SVListWidgetLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text()),
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text())
        ))

        self.pushButtonSVBackupLeft.clicked.connect(lambda: self.backup_scheduled_view(
            self.SVListWidgetLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text())
        ))

        self.pushButtonSVBackupRight.clicked.connect(lambda: self.backup_scheduled_view(
            self.SVListWidgetRight,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text())
        ))

        self.pushButtonSVRestoreLeft.clicked.connect(lambda: self.restore_scheduled_view(
            self.SVListWidgetLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text())
        ))

        self.pushButtonSVRestoreRight.clicked.connect(lambda: self.restore_scheduled_view(
            self.SVListWidgetRight,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text())
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
            self.SVListWidgetLeft.clear()
            self.SVListWidgetLeft.currentcontent = {}


        if right:
            self.SVListWidgetRight.clear()
            self.SVListWidgetRight.currentcontent = {}
            
    def update_SV_list(self, SVListWidget, url, id, key):
        sumo = SumoLogic(id, key, endpoint=url)
        try:
            logger.info("Updating SV List")
            SVListWidget.currentcontent = sumo.get_scheduled_views_sync()
            SVListWidget.clear()
            if len(SVListWidget.currentcontent) > 0:
                self.update_SV_listwidget(SVListWidget)
                return
        except Exception as e:
            logger.exception(e)
            self.mainwindow.errorbox('Something went wrong:\n\n' + str(e))
            return

    def update_SV_listwidget(self, SVListWidget):
        try:
            SVListWidget.clear()
            SVListWidget.setSortingEnabled(True)
            for object in SVListWidget.currentcontent:
                item_name = object['indexName']
                SVListWidget.addItem(item_name)  # populate the list widget in the GUI
            SVListWidget.updated = True
        except Exception as e:
            logger.exception(e)
        return

    def delete_scheduled_view(self, SVListWidget, url, id, key):
        logger.info("Deleting SV(s)")
        selecteditems = SVListWidget.selectedItems()
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
                        print(SVListWidget.currentcontent)
                        for object in SVListWidget.currentcontent:
                            if object['indexName'] == str(selecteditem.text()):
                                item_id = object['id']

                        result = sumo.disable_scheduled_view(item_id)

                    self.update_SV_list(SVListWidget, url, id, key)
                    return


                except Exception as e:
                    logger.exception(e)
                    self.mainwindow.errorbox('Something went wrong:\n\n' + str(e))

        else:
            self.mainwindow.errorbox('You need to select something before you can delete it.')
        return

    def copy_scheduled_view(self, SVListWidgetFrom, SVListWidgetTo, fromurl, fromid, fromkey,
                  tourl, toid,
                  tokey):

        logger.info("Copying SV(s)")
        try:
            selecteditems = SVListWidgetFrom.selectedItems()
            if len(selecteditems) > 0:  # make sure something was selected
                fromsumo = SumoLogic(fromid, fromkey, endpoint=fromurl)
                tosumo = SumoLogic(toid, tokey, endpoint=tourl)
                for selecteditem in selecteditems:
                    for object in SVListWidgetFrom.currentcontent:
                        if object['indexName'] == str(selecteditem.text()):
                            item_id = object['id']
                            scheduled_views_export = fromsumo.get_scheduled_view(item_id)
                            local_time = datetime.now(timezone.utc).astimezone()
                            status = tosumo.create_scheduled_view(scheduled_views_export['indexName'], scheduled_views_export['query'], local_time.isoformat() )
                self.update_SV_list(SVListWidgetTo, tourl, toid, tokey)
                return

            else:
                self.mainwindow.errorbox('You have not made any selections.')
                return

        except Exception as e:
            logger.exception(e)
            self.mainwindow.errorbox('Something went wrong:' + str(e))
            self.update_SV_list(SVListWidgetTo, tourl, toid, tokey)
        return

    def backup_scheduled_view(self, SVListWidget, url, id, key):
        logger.info("Backing Up SV(s)")
        selecteditems = SVListWidget.selectedItems()
        if len(selecteditems) > 0:  # make sure something was selected
            savepath = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Backup Directory"))
            if os.access(savepath, os.W_OK):
                message = ''
                sumo = SumoLogic(id, key, endpoint=url)
                for selecteditem in selecteditems:
                    for object in SVListWidget.currentcontent:
                        if object['indexName'] == str(selecteditem.text()):
                            item_id = object['id']
                            try:
                                export = sumo.get_scheduled_view(item_id)

                                savefilepath = pathlib.Path(savepath + r'/' + str(selecteditem.text()) + r'.json')
                                if savefilepath:
                                    with savefilepath.open(mode='w') as filepointer:
                                        json.dump(export, filepointer)
                                    message = message + str(selecteditem.text()) + r'.json' + '\n'
                            except Exception as e:
                                logger.exception(e)
                                self.mainwindow.errorbox('Something went wrong:\n\n' + str(e))
                                return
                self.mainwindow.errorbox('Wrote files: \n\n' + message)
            else:
                self.mainwindow.errorbox("You don't have permissions to write to that directory")

        else:
            self.mainwindow.errorbox('No content selected.')
        return

    def restore_scheduled_view(self, SVListWidget, url, id, key):
        logger.info("Restoring SV(s)")
        if SVListWidget.updated == True:

            filter = "JSON (*.json)"
            filelist, status = QtWidgets.QFileDialog.getOpenFileNames(self, "Open file(s)...", os.getcwd(),
                                                                      filter)
            if len(filelist) > 0:
                sumo = SumoLogic(id, key, endpoint=url)
                for file in filelist:
                    try:
                        with open(file) as filepointer:
                            sv_backup = json.load(filepointer)
                    except Exception as e:
                        logger.exception(e)
                        self.mainwindow.errorbox(
                            "Something went wrong reading the file. Do you have the right file permissions? Does it contain valid JSON?")
                        return
                    try:
                        local_time = datetime.now(timezone.utc).astimezone()
                        status = sumo.create_scheduled_view(sv_backup['indexName'], sv_backup['query'], local_time.isoformat())

                    except Exception as e:
                        logger.exception(e)
                        self.mainwindow.errorbox('Something went wrong:\n\n' + str(e))
                        return
                self.update_SV_list(SVListWidget, url, id, key)


            else:
                self.mainwindow.errorbox("Please select at least one file to restore.")
                return
        else:
            self.mainwindow.errorbox("Please update the directory list before restoring content")
        return
