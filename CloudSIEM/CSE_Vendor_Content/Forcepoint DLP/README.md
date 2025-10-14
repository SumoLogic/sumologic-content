# Forcepoint DLP (CEF) — Sumo Logic Content # 

### Turnkey content to parse and detect Forcepoint DLP events in Sumo Logic + Cloud SIEM.
### Includes a Sumo FER (ingest parser), Cloud SIEM Parser(s), Log Mapping, and a Detection Rule. ###

Import the log mapper, the parser, and the FER before importing the Detection Rule.

The Detection Rule will alert when Forcepoint DLP fires its built-in Standard Sensitive Data Detection policy (e.g., credit cards, SSNs, banking/health IDs) on outbound traffic or file movement—indicating potential sensitive-data exfiltration or policy violation. You can add additional categories 

Once the Forcepoint DLP logs are sent to the SIEM with our log mappings and parsers, you can run a query like this to view all of the different alerts from ForcePoint DLP to customize the dectection rule:
```
_index=sec_record* metadata_sourcecategory=syslog/forcepoint 
| where !isEmpty(%"fields.cat") 
| count by %"fields.cat"  
```
