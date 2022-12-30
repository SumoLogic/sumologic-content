# Sumo Logic for Fortinet Fortigate Firewall
Sumo Logic Community Content built for Fortigate Firewall that is not yet published to the [App Catalog](https://help.sumologic.com/docs/integrations/).

For instructions on how to collect logs and metrics for use with content, please see [Sumo Logic Documentation](https://help.sumologic.com/docs/send-data/).

![Overview](Screenshots/FortiGate%20Firewalls%20-%20Overview.png)

![Events](Screenshots/FortiGate%20Firewalls%20-%20Events.png)

![System Performance](Screenshots/FortiGate%20Firewalls%20-%20System%20Performance.png)

![Threat Analysis](Screenshots/FortiGate%20Firewalls%20-%20Threat%20Analysis.png)

![Traffic](Screenshots/FortiGate%20Firewalls%20-%20Traffic.png)

### Collection
#### **Prerequisites**
Configure your FortiGate Firewall to send its logs to a syslog server. FortiGate sends
syslog on UDP port 514 by default, but you can set the protocol and port.
FortiGate syslog documentation for v6.4.4 can be found at:
https://docs.fortinet.com/document/fortigate/6.4.4/cli-reference/444620/config-log-syslogd-setting. Documentation for additional versions can be found in FortiGate’s Document Library.

The Fortinet FortiGate Firewall App supports the raw syslog format, not CEF formatting.

1. Configure an Installed Collector appropriate for right for your host environment.
2. Configure a Syslog Source to the same port and protocol used by your FortiGate
Firewall.

#### **Sample Log**
    date=2017-11-15 time=11:44:16 logid="0000000013" type="traffic"
    subtype="forward" level="notice" vd="vdom1" eventtime=1510775056
    srcip=10.1.100.155 srcname="pc1" srcport=40772 srcintf="port12"
    srcintfrole="undefined" dstip=35.197.51.42
    dstname="fortiguard.com" dstport=443 dstintf="port11"
    dstintfrole="undefined" poluuid="707a0d88-c972-51e7-bbc7-
    4d421660557b" sessionid=8058 proto=6 action="close" policyid=1
    policytype="policy" policymode="learn" service="HTTPS"
    dstcountry="United States" srccountry="Reserved" trandisp="snat"
    transip=172.16.200.2 transport=40772 appid=40568
    app="HTTPS.BROWSER" appcat="Web.Client" apprisk="medium"
    duration=2 sentbyte=1850 rcvdbyte=39898 sentpkt=25 rcvdpkt=37
    utmaction="allow" countapp=1 devtype="Linux PC" osname="Linux"
    mastersrcmac="a2:e9:00:ec:40:01" srcmac="a2:e9:00:ec:40:01"
    srcserver=0 utmref=0-220586

#### **Field Extraction Rule**
This Field Extraction Rule (FER) is provided as an example to help you reduce your overall parsing time. Note that not all parse operators are supported in FERs. For more information, see Creating a Field Extraction Rule. There is a 200 field name limit for Field Extraction Rules (FER) and once a field is persisted using a FER, it can’t be removed. You can assign different targets to the name, but do not create overlapping messages and source categories.

    | extract "date=(?<date>.*?) " nodrop
    | extract "time=(?<time>.*?) " nodrop
    | extract "devname=\"(?<devname>.*?)\" " nodrop
    | extract "devid=\"(?<devid>.*?)\" " nodrop
    | extract "logid=\"(?<logid>.*?)\" " nodrop
    | extract "type=\"(?<type>.*?)\" " nodrop
    | extract "subtype=\"(?<subtype>.*?)\" " nodrop
    | extract "level=\"(?<level>.*?)\" " nodrop
    | extract "vd=\"(?<vd>.*?)\" " nodrop
    | extract "srcip=(?<srcip>.*?) " nodrop
    | extract "(?:src_port|srcport)=(?<srcport>.*?) " nodrop
    | extract "dstip=(?<dstip>.*?) " nodrop
    | extract "(?:dst_port|dstport)=(?<dstport>.*?) " nodrop
    | extract "proto=(?<proto>.*?) " nodrop
    | extract "action=\"(?<action>.*?)\" " nodrop
    | extract "duration=(?<duration>.*?) " nodrop
    | extract "sentpkt=(?<sentpkt>.*?) " nodrop
    | extract "rcvdpkt=(?<rcvdpkt>.*?) " nodrop
    | extract "msg=\"(?<msg>.*?)\"" nodrop
    | extract "action=\"(?<action>.*?)\" " nodrop
    | extract "user=\"(?<user>.*?)\" " nodrop
    | extract "srcname=\"(?<srcname>.*?)\" " nodrop
    | extract "poluuid=\"(?<poluuid>.*?)\" " nodrop
    | extract "sessionid=(?<sessionid>.*?) " nodrop
    | extract "policyid=(?<policyid>.*?) " nodrop
    | extract "dstcountry=\"(?<dstcountry>.*?)\" " nodrop
    | extract "srccountry=\"(?<srccountry>.*?)\" " nodrop
    | extract "service=\"(?<service>.*?)\" " nodrop
    | extract "sentbyte=(?<sentbyte>.*?) " nodrop
    | extract "rcvdbyte=(?<rcvdbyte>.*?) " nodrop
    | extract "devcategory=\"(?<devcategory>.*?)\" " nodrop
    | extract "osname=\"(?<osname>.*?)\" " nodrop

### To use the content:
- Download the JSON file(s).
- Find/replace all Source Categories within the JSON with your own Source Category (Ex: sourceCategory=yourSourceCategory).
- Import the content to your desired folder location in Sumo Logic.

### To upload your own content:
Please see [Sumo Logic Community Ecosystem Apps FAQs](https://help.sumologic.com/docs/integrations/community-ecosystem-apps/#faq).

