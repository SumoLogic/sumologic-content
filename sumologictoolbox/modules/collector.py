from qtpy import QtCore, QtGui, QtWidgets, uic
import os
import sys
import pathlib
import json
import re
from logzero import logger
from modules.sumologic import SumoLogic
from modules.dialogs import restoreSourcesDialog

class collector_tab(QtWidgets.QWidget):

    def __init__(self, mainwindow):

        super(collector_tab, self).__init__()
        self.mainwindow = mainwindow

        collector_ui = os.path.join(self.mainwindow.basedir, 'data/collector.ui')
        uic.loadUi(collector_ui, self)

        self.font = "Waree"
        self.font_size = 12

        # UI Buttons for Collection API tab

        # Setup the search bars to work and to clear when update button is pushed
        self.lineEditCollectorSearchLeft.textChanged.connect(lambda: self.set_listwidget_filter(
            self.listWidgetCollectorsLeft,
            self.lineEditCollectorSearchLeft.text()
        ))

        self.lineEditCollectorSearchRight.textChanged.connect(lambda: self.set_listwidget_filter(
            self.listWidgetCollectorsRight,
            self.lineEditCollectorSearchRight.text()
        ))

        self.pushButtonUpdateListLeft.clicked.connect(self.lineEditCollectorSearchLeft.clear)
        self.pushButtonUpdateListRight.clicked.connect(self.lineEditCollectorSearchRight.clear)

        #

        self.pushButtonUpdateListLeft.clicked.connect(lambda: self.updatecollectorlist(
            self.listWidgetCollectorsLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text())
        ))

        self.pushButtonUpdateListRight.clicked.connect(lambda: self.updatecollectorlist(
            self.listWidgetCollectorsRight,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text())
        ))

        self.pushButtonCopySourcesLeftToRight.clicked.connect(lambda: self.copysources(
            self.listWidgetCollectorsLeft,
            self.listWidgetCollectorsRight,
            self.listWidgetSourcesLeft,
            self.listWidgetSourcesRight,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text()),
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text())
        ))

        self.pushButtonCopySourcesRightToLeft.clicked.connect(lambda: self.copysources(
            self.listWidgetCollectorsRight,
            self.listWidgetCollectorsLeft,
            self.listWidgetSourcesRight,
            self.listWidgetSourcesLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text()),
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text())
        ))

        self.pushButtonBackupCollectorLeft.clicked.connect(lambda: self.backupcollector(
            self.listWidgetCollectorsLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text())
        ))

        self.pushButtonBackupCollectorRight.clicked.connect(lambda: self.backupcollector(
            self.listWidgetCollectorsRight,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text())
        ))

        self.pushButtonDeleteCollectorLeft.clicked.connect(lambda: self.deletecollectors(
            self.listWidgetCollectorsLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text())
        ))

        self.pushButtonDeleteCollectorRight.clicked.connect(lambda: self.deletecollectors(
            self.listWidgetCollectorsRight,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text())
        ))

        self.pushButtonDeleteSourcesLeft.clicked.connect(lambda: self.deletesources(
            self.listWidgetCollectorsLeft,
            self.listWidgetSourcesLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text())
        ))

        self.pushButtonDeleteSourcesRight.clicked.connect(lambda: self.deletesources(
            self.listWidgetCollectorsRight,
            self.listWidgetSourcesRight,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text())
        ))

        self.pushButtonRestoreSourcesLeft.clicked.connect(lambda: self.restoresources(
            self.listWidgetCollectorsLeft,
            self.listWidgetSourcesLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text())
        ))

        self.pushButtonRestoreSourcesRight.clicked.connect(lambda: self.restoresources(
            self.listWidgetCollectorsRight,
            self.listWidgetSourcesRight,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionRight.currentText())],
            str(self.mainwindow.lineEditUserNameRight.text()),
            str(self.mainwindow.lineEditPasswordRight.text())

        ))

        # set up a signal to update the source list if a new collector is set
        self.listWidgetCollectorsLeft.itemSelectionChanged.connect(lambda: self.updatesourcelist(
            self.listWidgetCollectorsLeft,
            self.listWidgetSourcesLeft,
            self.mainwindow.loadedapiurls[str(self.mainwindow.comboBoxRegionLeft.currentText())],
            str(self.mainwindow.lineEditUserNameLeft.text()),
            str(self.mainwindow.lineEditPasswordLeft.text())
        ))

        self.listWidgetCollectorsRight.itemSelectionChanged.connect(lambda: self.updatesourcelist(
            self.listWidgetCollectorsRight,
            self.listWidgetSourcesRight,
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
            self.listWidgetCollectorsLeft.clear()
            self.listWidgetSourcesLeft.clear()

        if right:
            self.listWidgetCollectorsRight.clear()
            self.listWidgetSourcesRight.clear()

    def set_listwidget_filter(self, ListWidget, filtertext):
        for row in range(ListWidget.count()):
            item = ListWidget.item(row)
            widget = ListWidget.itemWidget(item)
            if filtertext:
                item.setHidden(not filtertext in item.text())
            else:
                item.setHidden(False)

    def getcollectorid(self, collectorname, url, id, key):
        logger.info("Getting Collector IDs")
        sumo = SumoLogic(id, key, endpoint=url)
        try:
            sumocollectors = sumo.get_collectors_sync()

            for sumocollector in sumocollectors:
                if sumocollector['name'] == collectorname:
                    return sumocollector['id']
        except Exception as e:
            logger.exception(e)
        return

    def getsourceid(self, collectorid, sourcename, url, id, key):
        logger.info("Getting Source IDs")
        sumo = SumoLogic(id, key, endpoint=url)
        try:
            sumosources = sumo.sources(collectorid)

            for sumosource in sumosources:
                if sumosource['name'] == sourcename:
                    return sumosource['id']
            return False
        except Exception as e:
            logger.exception(e)
        return

    def updatecollectorlist(self, CollectorListWidget, url, id, key):
        logger.info("Updating Collector List")
        CollectorListWidget.clear()  # clear the list first since it might already be populated
        regexprog = re.compile(r'\S+')  # make sure username and password have something in them
        if (re.match(regexprog, id) != None) and (re.match(regexprog, key) != None):
            # access the API with provided credentials
            sumo = SumoLogic(id, key, endpoint=url)
            try:
                collectors = sumo.get_collectors_sync()  # get list of collectors

                for collector in collectors:
                    item = CollectorListWidget.addItem(collector['name'])  # populate the list widget in the GUI
                    items = CollectorListWidget.findItems(collector['name'], QtCore.Qt.MatchExactly)
                    if collector['collectorType'] == 'Hosted':
                        items[0].setData(6, QtGui.QFont(self.font, pointSize=self.font_size, weight=600))
                    if collector['alive'] == False:
                        items[0].setData(6, QtGui.QFont(self.font, pointSize=self.font_size, italic=True))

            except Exception as e:
                logger.exception(e)
                self.mainwindow.errorbox('Something went wrong:\n\n' + str(e))

        else:
            self.mainwindow.errorbox('No user and/or password.')
        return

    def updatesourcelist(self, CollectorListWidget, SourceListWidget, url, id, key):
        logger.info("Updating Source List")
        SourceListWidget.clear()  # clear the list first since it might already be populated
        collectors = CollectorListWidget.selectedItems()
        if (len(collectors) > 1) or (len(collectors) < 1):
            return
        else:
            collector = self.getcollectorid(collectors[0].text(), url, id, key)
            sumo = SumoLogic(id, key, endpoint=url)
            # populate the list of sources
            sources = sumo.sources(collector)
            for source in sources:
                SourceListWidget.addItem(source['name'])  # populate the display with sources
        return

    def copysources(self, CollectorListWidgetFrom, CollectorListWidgetTo, SourceListWidgetFrom, SourceListWidgetTo,
                    fromurl, fromid, fromkey, tourl, toid, tokey):
        logger.info("Copying Sources")
        try:
            fromsumo = SumoLogic(fromid, fromkey, endpoint=fromurl)
            sourcecollectorlist = CollectorListWidgetFrom.selectedItems()  # get the selected source collector
            if len(sourcecollectorlist) == 1:  # make sure there is a collector selected, otherwise bail
                sourcecollector = sourcecollectorlist[0].text()  # qstring to string conversion
                sourcecollectorid = self.getcollectorid(sourcecollector, fromurl, fromid, fromkey)
                destinationcollectorlist = CollectorListWidgetTo.selectedItems()  # get the selected dest collector
                if len(destinationcollectorlist) > 0:  # make sure there is a collector selected, otherwise bail
                    fromsources = SourceListWidgetFrom.selectedItems()  # get the selected sources
                    if len(fromsources) > 0:  # make sure at least one source is selected
                        fromsourcelist = []
                        for fromsource in fromsources:  # iterate through source names to build a warning message
                            fromsourcelist.append(fromsource.text())
                    else:
                        self.mainwindow.errorbox('No Sources Selected.')
                        return
                    destinationcollectorstring = ''
                    for destinationcollector in destinationcollectorlist:
                        destinationcollectorstring = destinationcollectorstring + destinationcollector.text() + ", "
                    message = "You are about to copy the following sources from collector \"" + sourcecollector + "\" to \"" + destinationcollectorstring + "\". Is this correct? \n\n"
                    for source in fromsourcelist:
                        message = message + source + "\n"
                    result = QtWidgets.QMessageBox.question(self, 'Really Copy?', message,
                                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                            QtWidgets.QMessageBox.No)  # bring up the copy dialog
                    if result:  # If they clicked "OK" rather than cancel
                        tosumo = SumoLogic(toid, tokey, endpoint=tourl)
                        for destinationcollector in destinationcollectorlist:
                            destinationcollectorname = destinationcollector.text()
                            destinationcollectorid = self.getcollectorid(destinationcollectorname, tourl, toid,
                                                                         tokey)  # qstring to string conversion
                            sumosources = fromsumo.sources(sourcecollectorid)
                            for source in fromsourcelist:  # iterate through the selected sources and copy them
                                for sumosource in sumosources:
                                    if sumosource['name'] == source:
                                        if 'id' in sumosource:  # the API creates an ID so this must be deleted before sending
                                            del sumosource['id']
                                        if 'alive' in sumosource:
                                            del sumosource[
                                                'alive']  # the API sets this itself so this must be deleted before sending
                                        template = {}
                                        template[
                                            'source'] = sumosource  # the API expects a dict with a key called 'source'
                                        notduplicate = True
                                        sumotosourcelist = tosumo.sources(destinationcollectorid)
                                        for sumotosource in sumotosourcelist:
                                            if sumotosource[
                                                'name'] == source:  # make sure the source doesn't already exist in the destination
                                                notduplicate = False
                                        if notduplicate:  # finally lets copy this thing
                                            tosumo.create_source(destinationcollectorid, template)
                                        else:
                                            self.mainwindow.errorbox(source + ' already exists, skipping.')
                        # call the update method for the dest collector since they have changed after the copy
                        if len(destinationcollectorlist) > 1:
                            self.mainwindow.infobox(
                                "Copy Complete. Please select an individual destination collector to see an updated source list.")

                        else:
                            self.updatesourcelist(CollectorListWidgetTo, SourceListWidgetTo, tourl, toid, tokey)


                else:
                    self.mainwindow.errorbox('You Must Select at Least 1 target.')
            else:
                self.mainwindow.errorbox('No Source Collector Selected.')
        except Exception as e:
            self.mainwindow.errorbox('Encountered a bug. Check the console output.')
            logger.exception(e)
        return

    def backupcollector(self, CollectorListWidget, url, id, key):
        logger.info("Backing Up Collector")
        collectornamesqstring = CollectorListWidget.selectedItems()  # get collectors sources have been selected
        if len(collectornamesqstring) > 0:  # make sure something was selected
            savepath = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Backup Directory"))
            if os.access(savepath, os.W_OK):
                message = ''
                sumo = SumoLogic(id, key, endpoint=url)
                for collectornameqstring in collectornamesqstring:
                    collectorid = self.getcollectorid(str(collectornameqstring.text()), url, id, key)
                    savefilepath = pathlib.Path(savepath + r'/' + str(collectornameqstring.text()) + r'.json')
                    savefilesourcespath = pathlib.Path(
                        savepath + r'/' + str(collectornameqstring.text()) + r'_sources' + r'.json')

                    if savefilepath:
                        with savefilepath.open(mode='w') as filepointer:
                            json.dump(sumo.collector(collectorid), filepointer)
                    if savefilesourcespath:
                        with savefilesourcespath.open(mode='w') as filepointer:
                            json.dump(sumo.sources(collectorid), filepointer)
                    message = message + str(collectornameqstring.text()) + ' '
                self.mainwindow.infobox('Wrote files ' + message)
            else:
                self.mainwindow.errorbox("You don't have permissions to write to that directory")

        else:
            self.mainwindow.errorbox('No Source Collector Selected.')
        return

    def deletecollectors(self, CollectorListWidget, url, id, key):
        logger.info("Deleting Collectors")
        collectornamesqstring = CollectorListWidget.selectedItems()
        if len(collectornamesqstring) > 0:  # make sure something was selected
            message = "You are about to delete the following collector(s):\n\n"
            for collectornameqstring in collectornamesqstring:
                message = message + str(collectornameqstring.text()) + "\n"
            message = message + '''
This is exceedingly DANGEROUS!!!! 
Please be VERY, VERY, VERY sure you want to do this!
Even if you have backed up your collectors to file you CANNOT
restore installed collectors using this tool or the Sumo Logic API.

If you are absolutely sure, type "DELETE" in the box below.

            '''
            text, result = QtWidgets.QInputDialog.getText(self, 'Warning!!', message)
            if (result and (str(text) == 'DELETE')):
                sumo = SumoLogic(id, key, endpoint=url)
                for collectornameqstring in collectornamesqstring:
                    try:
                        collectorid = self.getcollectorid(str(collectornameqstring.text()), url, id, key)
                        sumo.delete_collector(collectorid)
                    except Exception as e:
                        self.mainwindow.errorbox('Failed to delete collector: ' + str(collectornamesqstring.text()))
                        logger.exception(e)
                self.updatecollectorlist(CollectorListWidget, url, id, key)

        else:
            self.mainwindow.errorbox('No Collector Selected')
        return

    def restoresources(self, CollectorListWidget, SourceListWidget, url, id, key):
        destinationcollectors = CollectorListWidget.selectedItems()
        if len(destinationcollectors) == 1:
            destinationcollectorqstring = destinationcollectors[0].text()
            destinationcollector = str(destinationcollectorqstring)
            destinationcollectorid = self.getcollectorid(destinationcollector, url, id, key)
            filter = "JSON (*.json)"
            restorefile, status = QtWidgets.QFileDialog.getOpenFileName(self, "Open file(s)...", os.getcwd(),
                                                                        filter)

            sources = None
            try:
                with open(restorefile) as data_file:
                    sources = json.load(data_file)
            except Exception as e:
                self.mainwindow.errorbox('Failed to load JSON file.')
                logger.exception(e)

            if sources:
                dialog = restoreSourcesDialog(sources)
                dialog.exec()
                dialog.show()
                if str(dialog.result()) == '1':
                    selectedsources = dialog.getresults()
                else:
                    return
                if len(selectedsources) > 0:
                    sumo = SumoLogic(id, key, endpoint=url)
                    for selectedsource in selectedsources:
                        for sumosource in sources:
                            if sumosource['name'] == str(selectedsource):
                                if 'id' in sumosource:
                                    del sumosource['id']
                                if 'alive' in sumosource:
                                    del sumosource['alive']
                                template = {}
                                template['source'] = sumosource
                                sumo.create_source(
                                    destinationcollectorid, template)
                    self.updatesourcelist(CollectorListWidget, SourceListWidget, url, id, key)
                else:
                    self.mainwindow.errorbox('No sources selected for import.')
        else:
            self.mainwindow.errorbox('Please select 1 and only 1 collector to restore sources to.')
        return

    def deletesources(self, CollectorListWidget, SourceListWidget, url, id, key):
        logger.info("Deleting Sources")
        collectornamesqstring = CollectorListWidget.selectedItems()
        if len(collectornamesqstring) == 1:  # make sure something was selected
            collectorid = self.getcollectorid(str(collectornamesqstring[0].text()), url, id, key)
            sourcenamesqstring = SourceListWidget.selectedItems()
            if len(sourcenamesqstring) > 0:  # make sure something was selected
                message = "You are about to delete the following source(s):\n\n"
                for sourcenameqstring in sourcenamesqstring:
                    message = message + str(sourcenameqstring.text()) + "\n"
                message = message + '''
This could be exceedingly DANGEROUS!!!! 
Please be VERY, VERY, VERY sure you want to do this!

If you are absolutely sure, type "DELETE" in the box below.

                        '''
                text, result = QtWidgets.QInputDialog.getText(self, 'Warning!!', message)
                if (result and (str(text) == 'DELETE')):
                    sumo = SumoLogic(id, key, endpoint=url)
                    for sourcenameqstring in sourcenamesqstring:
                        try:
                            sourceid = self.getsourceid(collectorid, str(sourcenameqstring.text()), url, id, key)
                            sumo.delete_source(collectorid, sourceid)
                        except Exception as e:
                            self.mainwindow.errorbox('Failed to delete source: ' + str(sourcenameqstring.text()))
                            logger.exception(e)
                    self.updatesourcelist(CollectorListWidget, SourceListWidget, url, id, key)

            else:
                self.mainwindow.errorbox('No Source(s) Selected')
        else:
            self.mainwindow.errorbox('You must select 1 and only 1 collector.')
        return
