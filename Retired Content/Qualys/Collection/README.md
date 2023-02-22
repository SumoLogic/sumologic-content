The Qualys script achieves following functionality
1> Connects to Qualys
2> Get list of reports
3> Filters out latest report based on reportname, report format of CSV, report state as "Finished" and report type as "Scan"
   report with same name can exists with different report id
4> downloads report into local system
5> uploads the report on sumo hosted http collector

1. The python scripts are developed and tested with Python version 2.7.8.

2. The python scripts requires following python modules to be installed.
requests
datetime
ConfigParser
commands

3. "Qualys.py" takes input from configuration file "Qualys_Config.cfg"
Configure Qualys login credentials in [QualysCreds] section (usrId and pwd)
Configure Qualys logon and reports url in [QualysURLs] section (logonURL and qualysReportURL)
Configure reportname and download location with full path and filename in [Input] section (reportname and downloadfile)
Configure Sumo http hosted collector URL in [SumoUpload] section (sumoURL)


IMPORTANT:
The attached config file requires you to add your credentials, URL's, output file names as well as the sumo HTTP Endpoint URL that the script will be posting the data to.
Please refer to the below documentation for instructions on how to set up HTTPS Sources.

http://help.sumologic.com/Send_Data/Setup_Wizard/Collect_Streaming_Data_from_HTTP
http://help.sumologic.com/Send_Data/Sources/02Sources_for_Hosted_Collectors/HTTP_Source/Upload_Data_to_an_HTTP_Source