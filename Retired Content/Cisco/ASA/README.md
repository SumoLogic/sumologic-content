# Cisco ASA/AnyConnect VPN Dashboard

This folder contains a pre-built dashboard for Cisco ASA logs related to the use of the AnyConnect VPN.

**Ingesting Your Cisco ASA Logs into Sumo Logic**

For information on collecting your Cisco ASA logs in Sumo Logic, refer to our documentation [here](https://help.sumologic.com/07Sumo-Logic-Apps/22Security_and_Threat_Detection/Cisco_ASA/01Collect_Logs_for_the_Cisco_ASA_App).

**Installing in Your Sumo Logic Account**

1. Open the file `AnyConnect_ASA.json` in a text editor. 
2. Replace all instances of `<ASA_SOURCE_CATEGORY>` with the Source Category for your ASA logs. 
3. Copy the contents of the edited `AnyConnect_ASA.json` file.
4. Open your Sumo Logic account and follow the instructions [here](https://help.sumologic.com/05Search/Library/Export-and-Import-Content-in-the-Library#import-content-in-the-library) for importing content into your account.