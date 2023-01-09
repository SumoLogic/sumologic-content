#!/usr/bin/python

import xml.etree.ElementTree as ET
import ConfigParser
import commands

import requests

import datetime


def login(s, logonurl, usrid, pwd):
    payload = {'action': 'login', 'username': usrid, 'password': pwd}
    r = s.post(logonurl, data=payload)
    return r.status_code


def logout(s, logonurl):
    payload = {'action': 'logout'}
    r = s.post(logonurl, data=payload)
    return r.status_code


def downloadreport(s, qualysreporturl, reportid, downloadfile):
    status = False
    payload = {'action': 'fetch', 'id': reportid}
    r = s.post(qualysreporturl, data=payload)
    if r.status_code == 200:
        try:
            with open(downloadfile, "w") as report:
                report.write(r.content)
            status = True
        except IOError as e:
            print str(datetime.datetime.now()) + " Error in downloading file at: " + downloadfile + ". Exception: " + e.strerror
            status = False
    else:
        print str(datetime.datetime.now()) + " Error in posting message to Qualys Reporting URL to download report. Cross check URL used. Failure Reason: ", r.reason

    return status


def getreportidfromlist(s, qualysreporturl, reportname, reportformat, reportstate, reporttype):
    found = False
    reportid = ""
    dateformat = '%Y-%m-%dT%H:%M:%SZ'
    latestdate = datetime.datetime.strptime("1990-01-01T01:00:00Z", dateformat)

    payload = {'action': 'list', 'state': reportstate}
    r = s.post(qualysreporturl, data=payload)
    if r.status_code == 200:
        #print r.text

        root = ET.fromstring(r.text)
        for report_elem in root.iter('REPORT'):
            title = report_elem.find('TITLE').text
            reporttypevalue = report_elem.find('TYPE').text
            launchdatetime = report_elem.find('LAUNCH_DATETIME').text
            output_format = report_elem.find('OUTPUT_FORMAT').text
            status = report_elem.find('STATUS')
            state = status.find('STATE').text
            if title == reportname and output_format == reportformat and state == reportstate and reporttypevalue == reporttype:
                launch_datetime = datetime.datetime.strptime(launchdatetime, dateformat)
                if latestdate < launch_datetime:
                    latestdate = launch_datetime
                    reportid = report_elem.find('ID').text
                found = True
    else:
        print str(datetime.datetime.now()) + " Error in posting message to Qualys Reporting URL to get list of reports. Cross check URL used. Failure Reason: ", r.reason, ", Response status code : ", r.status_code

    return found, reportid


def getfinishedcsvreportid(s, qualysreporturl, reportname):
    status, reportid = getreportidfromlist(s, qualysreporturl, reportname, "CSV", "Finished", "Scan")
    return status, reportid


def main():
    status = False

    print str(datetime.datetime.now()) + " ========================= Qualys Script Started ========================="

    config = ConfigParser.ConfigParser()
    config.read('Qualys_Config.cfg')
    usrid = config.get('QualysCreds', 'usrId')
    pwd = config.get('QualysCreds', 'pwd')
    logonurl = config.get('QualysURLs', 'logonURL')
    qualysreporturl = config.get('QualysURLs', 'qualysReportURL')
    reportname = config.get('Input', 'reportname')
    downloadfile = config.get('Input', 'downloadfile')
    sumohttphostedcollectorurl = config.get('SumoUpload', 'sumoURL')

    s = requests.Session()
    s.headers.update({'X-Requested-With': 'SumoLogic Python Script to use Qualys API'})
    status_code = login(s, logonurl, usrid, pwd)
    if status_code == 200:
        print str(datetime.datetime.now()) + " LoggedIn into Qualys"
        status, reportid = getfinishedcsvreportid(s, qualysreporturl, reportname)
        if status is True:
            str_to_print = str(datetime.datetime.now()) + " Downloading report \"" + reportname + "\" with ReportId: " + reportid + ". This may take some time..."
            print str_to_print

            status = downloadreport(s, qualysreporturl, reportid, downloadfile)
            if status is True:
                str_to_print = str(datetime.datetime.now()) + " Report \"" + reportname + "\" with ReportId: " + reportid + " downloaded at: \"" + downloadfile + "\""
                print str_to_print

                status_code = logout(s, logonurl)
                if status_code == 200:
                    print str(datetime.datetime.now()) + " LoggedOut from Qualys"

                s.close()
                print str(datetime.datetime.now()) + " Uploading file \"" + downloadfile + "\" to SumoLogic. This may take some time..."

                # use of python requests module to upload file
                files = {'file': open(downloadfile, 'r')}
                try:
                    r = requests.post(sumoURL, files=files)
                    if (r.status_code == 200):
                        print str(datetime.datetime.now()) + " Uploaded file \"" + downloadfile + "\" to SumoLogic."
                    else:
                        print str(datetime.datetime.now()) + " Error in uploading file: \"" + downloadfile + "\" to SumoLogic. Error code: " + str(r.status_code), "Reason: " + r.reason
                except requests.exceptions.ConnectionError as e:
                    print str(datetime.datetime.now()) + " Error in uploading file: \"" + downloadfile + "\" to SumoLogic. Possibly invalid URL: " + sumoURL

                success_string1 = "We are completely uploaded and fine"
                success_string2 = "HTTP/1.1 200 OK"
                if success_string1 in cmdoutput and success_string2 in cmdoutput:
                    print str(datetime.datetime.now()) + " Uploaded file \"" + downloadfile + "\" to SumoLogic."
                else:
                    print str(datetime.datetime.now()) + " Error in uploading file: \"" + downloadfile + "\" to SumoLogic. " + "Error : " + cmdoutput

            else:
                print str(datetime.datetime.now()) + " Error in downloading report \"" + reportname + "\" with ReportId: " + reportid + " at: \"" + downloadfile + "\""

        else:
            str_to_print = str(datetime.datetime.now()) + " Report \"" + reportname + "\" not found satisfying the filter criteria - OR - Error with Qualys Reporting URL."
            print str_to_print

        status_code = logout(s, logonurl)
        if status_code == 200:
            print str(datetime.datetime.now()) + " LoggedOut from Qualys"

    else:
        print str(datetime.datetime.now()) + " Login Failure - Invalid login URL or bad user credentials."

    s.close()

    print str(datetime.datetime.now()) + " ========================= Qualys Script Ended ========================="

if __name__ == "__main__": main()
