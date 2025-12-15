# Threat Intel - Intel471 Log Query Guide

Intel471 in Sumo comes out of the box as threat source inside sumo://threat/i471. You don’t query it directly with _sourceCategory; you join it into your existing searches with lookup. In this content pack, there is a dashboard with many sample panels that might be useful for Threat Hunting in Log Search with Intel471

The pattern is always: 
- Extract an indicator from your logs
- lookup that field against sumo://threat/i471 using threat 
- Filter to matches
- Aggregate however you want (maps, tables, timecharts) 

### Example of lookup:
```
_sourceCategory=...
| parse regex field=_raw "(?<ip_address>\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" multi
| lookup raw as i471_raw, threatlevel as i471_howbad
    from sumo://threat/i471 on threat=ip_address
| where !isNull(i471_howbad)
```

You can extract out the results and use the Intel471 fields with the following statement:
```
| json field=i471_raw
     "data.threat.data.family",
    "data.context.description",
    "data.threat.type",
    "data.mitre_tactics",
    "data.confidence"
      as malware_family, description,threat_type, mitre_tactics, ti_confidence nodrop
```

You can find other similar fields to extract and reference them with the json field operator. This is an example of an output for an ip address match for stealc_v2

```json
{
    "uid": "",
    "source_id": "",
    "threat": {
        "type": "malware",
        "uid": "",
        "data": {
            "malware_family_profile_uid": "",
            "family": "stealc_v2"
        }
    },
    "expiration": 1766982832000,
    "confidence": "medium",
    "context": {
        "description": "stealc_v2 controller IPv4"
    },
    "mitre_tactics": "command_and_control",
    "indicator_type": "ipv4",
    "indicator_data": {
        "address": "62.60.226.170"
    },
    "intel_requirements": [
        "1.4.1",
        "1.1.6",
        "1.1.5"
    ]
}
```