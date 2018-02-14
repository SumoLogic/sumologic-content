In some cases, a multiline log message may not have a first line that matches any of the default rules used by Sumo Logic to detect a multiline message. 
In this case, you will need to specify a regular expression to detect the entire first line of each new log message within the file. 

For example, when logs contain messages that span multiple lines separated by line breaks, such as a stack trace, you may need to specify a boundary regex.

For more information, see the documentation here: 

Define Boundary Regex for Multiline Messages: https://help.sumologic.com/Send-Data/Sources/01Sources-for-Installed-Collectors/Local-File-Source/Define-Boundary-Regex-for-Multiline-Messages
