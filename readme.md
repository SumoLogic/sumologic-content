Sumotoolbox
===========

 Sumotoolbox is a GUI utility for accessing the various Sumo Logic APIs. The idea is to make
 it easier to perform common API tasks such as copying sources and generating CSV files from
 searches.

Installing the Binaries
=======================

One way to use sumotoolbox is to look in the "dist" directory of this repo and grab the executable for your 
platform. Make a new directory, copy the executable into it, and run the executable. 

The first time you run the executable it will create a "sumotoolbox.ini" file and if you choose to use the credential
store feature it will also create a "credentials.db" file.

Note: The executables are built for 64-bit only and may not run on less than current operating systems. 
In the case of Windows my build is for a very recent version of Windows 10 and has failed to work on older versions.
Unfortunately I do not have access to an older version of Windows 10 to build against. If it doesn't work your only
option may be to install the source as described below. 

Updating the Binaries
=====================

When it's time to upgrade to a new version of sumotoolbox simply download the new executable and use it to replace
your old one, leaving your ini and db file in place. 

Installing the Source
=====================

If you prefer to clone the archive and run from source then you'll need Python 3.6 or higher and the modules listed 
in the dependency section.  

The steps are as follows: 

    1. Download and install python 3.6 or higher from python.org. 
       Make sure to choose the "add python to the default "path" checkbox in the installer (may be in 
       advanced settings.)

       Note: If you have Linux you can skip this step, but ensure you have python3 installed for your distro. 

       Note: If you have OS X you cannot use the python that comes with the OS, it is too old.

    2. Download and install git for your platform if you don't already have it installed.
       It can be downloaded from https://git-scm.com/downloads
    
    3. Open a new shell/command prompt. It must be new since only a new shell will include the new python 
       path that was created in step 1. Cd to the folder where you want to install sumotoolbox.
    
    4. Execute the following command to install pipenv, which will manage all of the library dependencies 
       for us:

        pip3 install pipenv
    
        -or-
    
        sudo pip3 install pipenv 
 
    5. Clone this repo using the following command:
    
        git clone https://github.com/voltaire321/sumologictoolbox.git
    
    This will create a new folder called sumotoolbox. 
    
    6. Change into the sumotoolbox folder. Type the following to install all the package 
       dependencies (this may take a while as this will download all of the libraries that sumotoolbox uses):

    pipenv install
    
To run sumotoolbox cd into the sumotoolbox directory and type:

    pipenv run python3 sumotoolbox.py
    
Updating the Source
===================

When it's time to upgrade to a new version of sumotoolbox cd into the sumotoolbox directory and type:
    
    1. git pull https://github.com/voltaire321/sumologictoolbox.git
    
    2. pipenv install
    
To run sumotoolbox cd into the sumotoolbox directory and type:

    pipenv run python3 sumotoolbox.py

Dependencies
============

See the contents of "pipfile"

Features and Usage
==================

Collector Source Copying:

    1. Input/select Credentials for your source and destination orgs
    2. Select your regions for source and destination orgs
    3. Click "Update" for source and destination to populate the collector lists
    4. Choose a source collector to populate the sources list.
    5. Select one or more sources
    6. Select a destination collector
    7. Click "Copy".

    NOTE: You can use the same credentials for both source and destination to copy sources from one 
          collector to another within the same org.

Collector Backup:

    1. Input/select Credentials for your org
    2. Select your region for your org
    3. Click "Update" to populate the collector list
    4. Choose one or more get_collectors
    5. Click 'Backup Collector(s)' to write a json dump of the selected get_collectors and their sources
    
    NOTE: There is not currently a collector restore capability in this tool. 

Collector Delete:

    1. Input/select Credentials for your org
    2. Select your region for your org
    3. Click "Update" for destination to populate the collector list
    4. Choose one or more get_collectors
    6. Click "Delete Collector(s)"
    7. Verify that you really want to delete the collector(s) by typing "DELETE"
    8. Click "OK"
    
    NOTE: This can be very dangerous. Accidentally deleting the wrong collector(s) could result
          in log collection interruption and many, many hours of restoration work. Use with EXTREME
          caution. 
    
Source Delete:

    1. Input/select Credentials for your org
    2. Select your region for your org
    3. Click "Update" for destination to populate the collector list
    4. Choose a collector
    5. Choose one or more sources
    6. Click "Delete Source(s)"
    7. Verify that you really want to delete the source(s) by typing "DELETE"
    8. Click "OK"

    NOTE: This can be very dangerous. Accidentally deleting the wrong sources(s) could result in log
          collection interruption and many, many hours of restoration work. Use with EXTREME caution. 
    
Search API:

    1. Input/select source credentials
    2. Select your source region
    3. Select your timezone (defaults to local system timezone)
    4. Select your time range (defaults to a relative 15 minute window from the time
    the app was launched)
    5. Enter a valid Sumo Logic search query
    6. Select whether you want to see message results or record results (raw messages
    vs. aggregate data.)
    7. (Optional) Check "Save to CSV" to create a CSV file from the results
    8. (Optional) Check "Convert to Selected Timezone from UTC Epoch". This will return message
    times and "_timeslice"fields as local time formatted as %Y-%m-%d %H:%M:%S rather than 
    UTC epoch time.
    9. Click "Start"
    
    NOTE: The use case for this fuctionality is dumping to CSV. The Sumo Logic UI export feature is
          currently limited to 100,000 log messages. This tool should reliably dump much more than that,
          however the UI will "freeze" during the dump. This could take minutes or even hours depending 
          on the size of the dump. Please resist the temptation to rage quit because of an unresposive UI.
          If you want to check on the status of the download you can look in the console or log file to
          see status messages. 
    
    NOTE: If you choose to save Raw messages to CSV they will no longer be displayed after the job finishes.
          This change was made so that sumotoolbox can download an arbitrary number of messages without 
          running out of RAM. 

Content Folder Creation:    
    
    1. Input/select Credentials for your org
    2. Select your region for your org
    3. Click "Update" for destination to populate the collector list
    4. (Optional) Select "Personal Folder" or "Admin Recommended" radio button to switch context
    4. Navigate to the location you want to create the new folder. 
    6. Click "New Folder".
    7. Enter a name for the new folder. 
    8. Click "OK"
    
    NOTE: You cannot create top level folders when in the "Admin Recommeded" context. This
          should be fixed in the future. 
    

Content Deletion:    
    
    1. Input/select Credentials for your org
    2. Select your region for your org
    3. Click "Update" for destination to populate the collector list
    4. (Optional) Select "Personal Folder" or "Admin Recommended" radio button to switch context
    4. Navigate to the location that contains the content you wish to delete. 
    6. Select one or more items from the list. 
    7. Click "Delete"
    7. Verify that you really want to delete the source(s) by typing "DELETE"
    8. Click "OK"
    
    
    NOTE: This can be very dangerous. Accidentally deleting the wrong content could result in serious 
          issues and many hours of restoration work. Use with EXTREME caution. 
    

Content Copying:    

    1. Input/select Credentials for your source and destination orgs
    2. Select your regions for source and destination orgs
    3. Click "Update" for source and destination to populate the content lists
    4. (Optional) Select "Personal Folder" or "Admin Recommended" radio button to switch context in 
       either pane. 
    5. Select one or more items from the list
    6. Click "Copy" (left to right or right to left). Your content will be copied to the current folder 
       in the destination pane.
    
Field Extraction Rule copy/import/export: !New!

    1. Input/select Credentials for your source and destination orgs
    2. Select your regions for source and destination orgs
    3. Click "Update" for source and destination to populate the FER lists
    4. Click "Copy" or "Backup" or "Restore".
    
Scheduled View copy/import/export: !New!

    1. Input/select Credentials for your source and destination orgs
    2. Select your regions for source and destination orgs
    3. Click "Update" for source and destination to populate the FER lists
    4. Click "Copy" or "Backup" or "Restore".
    
Content Find/Replace/Copy:  !EXPERIMENTAL!

    Copying content between orgs often requires that the sourceCategory tags be changed to match the new 
    environment. The Find/Replace/Copy feature is intended to lighten this burden by doing sourceCategory
    tag replacement during the copy. It finds all of the sourceCategory tags in your original content and 
    presents them to you along with the sourceCategory tags in your destination environment allowing you 
    to match them for replacement.
    
    1. Input/select Credentials for your source and destination orgs
    2. Select your regions for source and destination orgs
    3. Click "Update" for source and destination to populate the content lists
    4. (Optional) Select "Personal Folder" or "Admin Recommended" radio button to switch context in either
       pane. 
    5. Select one or more items from the list
    6. Click "Find/Replace/Copy" (left to right or right to left). 
    7. Wait a bit (the REST calls involved can take a while)
    8. Choose what tags to replace. 
    9. Click "OK"
    10. Wait a bit (lot) more. If you are copying large amounts of content the wait can be significant. 
        The UI will seem to freeze or lockup during the copy because the tool is not multithreaded. Have 
        patience and resist the urge to rage quit, it's still a million times faster than doing this by hand.
    11. Once the pop-up window closes your content should be copied to the current folder in the 
        destination pane.
    
Content Backup: 

    1. Input/select Credentials for your source and destination orgs
    2. Select your regions for source and destination orgs
    3. Click "Update" for source and destination to populate the content lists
    4. (Optional) Select "Personal Folder" or "Admin Recommended" radio button to switch context in 
       either pane. 
    5. Select one or more items from the list
    6. Click "Backup"
    7. Choose a folder to save your backup files into
    8. The selected content will be exported and written as JSON to the selected folder, one file per 
       selected item. 
    
    Note: The filenames are created automatically from the item names that are selected for backup. 
    
Content Restore: 

    1. Input/select Credentials for your source and destination orgs
    2. Select your regions for source and destination orgs
    3. Click "Update" for source and destination to populate the content lists
    4. (Optional) Select "Personal Folder" or "Admin Recommended" radio button to switch context in either 
       pane. 
    5. Navigate to the folder you wish to restore into. 
    6. Click "Restore"
    7. Select one or more valid Sumo Logic exports files to restore. These must be valid JSON that has been 
       previously exported from Sumo Logic, either using this tool, the API, or the Sumo Logic UI. 
    8. Your content will be restored into the current directory. 
    
    Note: You cannot currently restore into the root admin folder. This will be fixed soon.     

Logging:   

    The tool should now generate a "sumologic.log" file in the directory it lives in. If you experience a
    bug, please delete the log file, set the logging level to "debug" (from the "settings" menu), recreate
    the bug, and send me the new log file along with a screenshot and/or description or what you were doing
    at the time. I can't promise an immediate fix but I will do my best. 
    
    tmacdonald@sumologic.com
    
Config File:    

    sumologictoolbox now includes a sumologictoolbox.ini file to configure the tool. The ini file contains 
    documetation on each setting. 
    
    NOTE: If you downloaded the executables rather than the source then this file will be generated on your 
          first execution of the tool in the same directory as the tool. 
   
Credential Database: 

    The tool now includes an optional credential store. You can create a new credential database using the
    "Create Cred Database" button. This will ask for you to enter a new password and will create a new, 
    empty credential database in the same directory as your sumologictoolbox script/executable. 
    
    sumologictoolbox enforces a minimal complexity of 10 characters with upper/lower/numeric/non-alphanumeric
    characters.This password will be used as your master encryption key so longer/more complex is always better. 
    You must REMEMBER this password. It cannot be retrieved once set. If you forget your password you must 
    create a new credential database. 
    
    Once the credential database is created you can load it on subsequent executions of sumologictoolbox using
    the "Load Cred DB" button. This will require the same password you entered when you initially created it. 
    
    Once the database is created/loaded you can then save/update/delete credentials in the database using the
    Create/Update/Delete preset buttons. 
    
    Note: The credentials db functionality is optional. You can still use sumologictoolbox without it in the 
          same way as previous versions (by entering information manually into the appropriate fields.)
    
    Note: Before using the credential database functionality please ensure it complies with all policies/laws
          applicable to your organization. 
         
    Specs:
    
    1. Argon2 for main password hashing
    2. AES 256 (GCM) for encrypt/decrypt of credentials
    3. PBKDF2HMAC using SHA3_512 to create 256 bit encryption/decryption keys 
       (500,000 iterations using a 64 byte random salt)
    4. salts are generated randomly per set of credentials every time they are saved/updated in the database

    Credential DB FAQ:

    Q: I see a flaw in your implementation. Can I send feedback?
    A: Please do! I have done my utmost to do this in the most secure fashion possible but any constructive 
       feedback is welcome! Please read the rest of the FAQ first though before sending feedback.
       You can send feedback to: tmacdonald@sumologic.com

    Q: What is Argon2? I've never heard of it!
    A: At the time of writing argon2 was the recommended password hashing algoritm by the password hashing 
       competititon.
       https://password-hashing.net/ 

    Q: I have my own keystore, can I use that instead?
    A: Yes! I have attempted to write sumologictoolbox in such a way that you can implement your own version
       of the CredentialDB class that calls or implements a different keystore. To this end I have done the
       following:

       1. Sumologictoolbox will pass a username/id as well as a password to the CredentialDB class if one is
          set in the sumologictoolbox ini file.
       2. You can turn off the "create/delete cred database" button in sumologictoolbox with the appropriate
          setting in the sumologictoolbox ini file. This will leave only the load button to be used in 
          connecting to the external credential store.
       3. Sumologictoolbox will only activate the "create preset", 'update preset', and 'delete preset' 
          buttons if the "add_cred", "update_cred", and "delete_cred" methods exist in the CredentialDB class. 
          This means you can implement a read-only version of this class that authenticates against an 
          external credential store. I've added comments to each method marking them as "required", "optional",
          and "internal". You only need to implement the "required" methods for a read-only credential store.

    Q: I looked at your code. Why are you storing the salt in the open? Doesn't that make it worthless?
    A: The salt is stored in "plain text" with the encrypted data as they must be used for decryption. 
       This is an accepted practice. For more information on why that is the case I suggest the following 
       reading:
       https://crackstation.net/hashing-security.htm
    
    Q: Can I turn all of this off? I don't want my users using your/any credential store.
    A: Yes! You can turn it off in the Sumologictoolbox ini file.
    
        

Screen Shots:
=============

![Collector Source Copy](https://github.com/voltaire321/sumologictoolbox/blob/master/screenshots/sumotoolbox_collector_example.png "Source Copy")

![Search API Example](https://github.com/voltaire321/sumologictoolbox/blob/master/screenshots/sumotoolbox_search_example.png "Search API")

![Content API Example](https://github.com/voltaire321/sumologictoolbox/blob/master/screenshots/sumotoolbox_content_example.png "Content API")

![Field Extraction Rule API Example](https://github.com/voltaire321/sumologictoolbox/blob/master/screenshots/sumotoolbox_FER_example.png "Content API")

![Scheduled View API Example](https://github.com/voltaire321/sumologictoolbox/blob/master/screenshots/sumotoolbox_SV_example.png "Content API")

Known Issues:
=============

* No status updates during searches/copy operations. When making API calls the UI becomes non-responsive
until the calls complete. This is due to the requests library blocking Qt5 when REST calls are being used. One day this
might be fixed by multithreading the app but currently this is expected behaviour. 

* When copying content to Admin Recommended folders the content will be copied but not visible in this tool until it is shared in the
SumoLogic UI. This will be resolved in a future release. 

* New style dashboards are not currently visible in the content explorer.

To Do:
======

* Add "source update" functionality (for instance to add filters)

* Add Users/Roles API functionality

* Add Connections Functionality

License
=======

Copyright 2015 Timothy MacDonald

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Support
=======

This is an opensource tool that I've written in my spare time. It is NOT an official Sumo Logic product. Use at your
own risk. 

This repository and the code within are NOT supported by Sumo Logic.

Feel free to e-mail me with issues however and I will provide "best effort" fixes: tmacdonald@sumologic.com


