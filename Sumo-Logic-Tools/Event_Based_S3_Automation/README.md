# EVENT BASED S3 SETUP AUTOMATOR

### NOTE: This script is *community supported* and no guarantees are made by Sumo Logic.

### DESCRIPTION
This is a python script that will automatically configure event based S3 on all of your polling sources.
Event based S3 is a method where Sumo Logic gets notified about any objects that are added to your S3 bucket rather than us polling the bucket to fetch new objects. 
The polling mechanism can be slow if the bucket is very large. Event based S3 is the way to go in such cases. 

# Steps to run the automation script
* Run **sudo apt-get install python3-pip** to install pip3
* Run **sudo pip3 install -r requirements.txt** to install the requirements
* Run **aws configure** to configure aws cli
* Run **chmod +x script.py** to give execution permission to the script
* Run the script using **python3 script.py**