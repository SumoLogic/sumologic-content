# Sumo Logic for Netflow

![Netflow](Meraki-Netflow-dashboard.png)

This is an app for Netflow. It contains a dashboard calculating key netflow statistics. 

Netflow logs are collected using a fluentd netflow plugin and then forwarded to a 

Additional documentation from Heroku on required logging:

* [HTTP Routing - Heroku Router Log Format](https://devcenter.heroku.com/articles/http-routing#heroku-router-log-format)
* [Heroku Labs: log-runtime-metrics](https://devcenter.heroku.com/articles/log-runtime-metrics)


## Fluentd Setup for Netflow Collection
1. [Install fluentd](https://docs.fluentd.org/installation/before-install)
2. Install one of the following fluentd input sources to handle collection of netflow data. Each are recommended from Fluentd's docs, but the latter seems to be receiving more frequent updates. [fluent-plugin-netflow](https://github.com/repeatedly/fluent-plugin-netflow) or [fluent-plugin-netflowipfix](https://github.com/yvesbd/fluent-plugin-netflowipfix)
3. Install the [SumoLogic fluentd output plugin](https://github.com/SumoLogic/fluentd-output-sumologic)
4. Create a hosted collector in SumoLogic and add an HTTP source
5. Modify the fluentd config file to reference the new input/output plugins (sample config shown below)
6. Restart the fluentd agent after updating the config file

```
  ##Netflow input
  <source>
    type netflowipfix
    tag netflow.event
    bind {IP address for plugin to accept Netflow}
    port {UDP port for plugin to accept Netflow; 5140 is default}
  </source>
  
  ##Sumo Logic output
  <match **>
    @type sumologic
    endpoint {Sumo HTTP endpoint}
  </match>
```

## Troubleshooting Tips
* Monitor stdout for errors after starting the fluentd agent and check the fluentd log for specifics
* Verify that your input/output plugins are installed in the correct plugin directory so that the fluentd agent can find them
* Comment out any unused input/output plugins in the config file
* Use this [netflow generator](https://github.com/mshindo/NetFlow-Generator) to test a config on your own in a lab env

### Update Source Categories

Update `$$Netflow` to `_sourceCategory=yourSourceCategory`

### Import App

Once imported, the app should automatically be setup to query against Netflow logs.
