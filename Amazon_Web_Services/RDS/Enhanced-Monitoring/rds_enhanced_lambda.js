/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                           RDS Enhanced Monitoring -> CloudWatch Logs -> Sumo Logic                              //
//               https://github.com/SumoLogic/sumologic-aws-lambda/tree/master/cloudwatchlogs                      //
//                                                                                                                 //
//        YOU MUST CREATE A SUMO LOGIC ENDPOINT CALLED SUMO_ENDPOINT AND PASTE IN ENVIRONMENTAL VARIABLES BELOW    //
//            https://help.sumologic.com/Send_Data/Sources/02Sources_for_Hosted_Collectors/HTTP_Source             //
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// CURRENTLY DOES NOT SUPPORT MSSQL ENGINES YET

// SumoLogic Endpoint to post logs
var SumoURL = process.env.SUMO_ENDPOINT;

// The following parameters override the sourceCategoryOverride, sourceHostOverride and sourceNameOverride metadata fields within SumoLogic.
// Not these can also be overridden via json within the message payload. See the README for more information.
var sourceCategoryOverride = process.env.SOURCE_CATEGORY_OVERRIDE || 'none';  // If none sourceCategoryOverride will not be overridden
var sourceHostOverride = process.env.SOURCE_HOST_OVERRIDE || 'none';          // If none sourceHostOverride will not be set to the name of the logGroup
var sourceNameOverride = process.env.SOURCE_NAME_OVERRIDE || 'none';          // If none sourceNameOverride will not be set to the name of the logStream

// CloudWatch logs encoding
var encoding = process.env.ENCODING || 'utf-8';  // default is utf-8

// Include logStream and logGroup as json fields within the message. Required for SumoLogic AWS Lambda App
var includeLogInfo = false;  // default is true

// Regex used to detect logs coming from lambda functions.
// The regex will parse out the requestID and strip the timestamp
// Example: 2016-11-10T23:11:54.523Z	108af3bb-a79b-11e6-8bd7-91c363cc05d9    some message
var consoleFormatRegex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z\t(\w+?-\w+?-\w+?-\w+?-\w+)\t/;

// Used to extract RequestID
var requestIdRegex = /(?:RequestId:|Z)\s+([\w\d\-]+)/;

var https = require('https');
var zlib = require('zlib');
var url = require('url');


function sumoMetaKey(awslogsData, message) {
    var sourceCategory = '';
    var sourceName = '';
    var sourceHost = '';
    
    if (sourceCategoryOverride !== null && sourceCategoryOverride !== '' && sourceCategoryOverride != 'none') {
        sourceCategory = sourceCategoryOverride;
    }
    
    if (sourceHostOverride !== null && sourceHostOverride !== '' && sourceHostOverride != 'none') {
        sourceHost = sourceHostOverride;
    } else {
        sourceHost = awslogsData.logGroup;
    }
    
    if (sourceNameOverride !== null && sourceNameOverride !== '' && sourceNameOverride != 'none') {
        sourceName = sourceNameOverride;
    } else {
        sourceName = awslogsData.logStream;
    }
    
    // Ability to override metadata within the message
    // Useful within Lambda function console.log to dynamically set metadata fields within SumoLogic.
    if (message.hasOwnProperty('_sumo_metadata')) {
        var metadataOverride = message._sumo_metadata;
        if (metadataOverride.category) {
            sourceCategory = metadataOverride.category;
        }
        if (metadataOverride.host) {
            sourceHost = metadataOverride.host;
        }
        if (metadataOverride.source) {
            sourceName = metadataOverride.source;
        }
        delete message._sumo_metadata;
    }
    return sourceName + ':' + sourceCategory + ':' + sourceHost;
    
}

function postToSumo(context, messages) {
    var messagesTotal = Object.keys(messages).length;
    var messagesSent = 0;
    var messageErrors = [];
    
    var urlObject = url.parse(SumoURL);
    var options = {
        'hostname': urlObject.hostname,
        'path': urlObject.pathname,
        'method': 'POST'
    };
    
    var finalizeContext = function () {
        var total = messagesSent + messageErrors.length;
        if (total == messagesTotal) {
            console.log('messagesSent: ' + messagesSent + ' messagesErrors: ' + messageErrors.length);
            if (messageErrors.length > 0) {
                context.fail('errors: ' + messageErrors);
            } else {
                context.succeed();
            }
        }
    };
    
    Object.keys(messages).forEach(function (key, index) {
        var headerArray = key.split(':');
        
        options.headers = {
            'X-Sumo-Name': headerArray[0],
            'X-Sumo-Category': headerArray[1],
            'X-Sumo-Host': headerArray[2],
            'X-Sumo-Client': 'cwl-aws-lambda',
            'Content-Type': 'application/vnd.sumologic.carbon2'
        };
        
        var req = https.request(options, function (res) {
            res.setEncoding('utf8');
            res.on('data', function (chunk) {});
            res.on('end', function () {
                if (res.statusCode == 200) {
                    messagesSent++;
                } else {
                    messageErrors.push('HTTP Return code ' + res.statusCode);
                }
                finalizeContext();
            });
        });
        
        req.on('error', function (e) {
            messageErrors.push(e.message);
            finalizeContext();
        });
        

        // Convert Enhanced Monitoring logs to Carbon 2.0 metrics
        for (var i = 0; i < messages[key].length; i++) {
            var timestamp = new Date(messages[key][i].message.timestamp);
            var epoch_timestamp = Math.floor(timestamp / 1000);
            var engine=messages[key][i].message.engine;
            var instanceID=messages[key][i].message.instanceID;
            var instanceResourceID=messages[key][i].message.instanceResourceID;
            var version=messages[key][i].message.version;
            
            // cpuUtilization
            for (var p in messages[key][i].message.cpuUtilization){
                if( messages[key][i].message.cpuUtilization.hasOwnProperty(p) ) {
                    req.write('\n');
                    req.write('engine=' + engine + ' instanceID=' + instanceID + ' instanceResourceID=' + instanceResourceID + ' version=' + version + ' cpuUtilization=' + p + '  type=cpuUtilization ' + messages[key][i].message.cpuUtilization[p] + ' ' + epoch_timestamp);
                } 
            }
            
            // loadAverageMinute
            for (var p in messages[key][i].message.loadAverageMinute){
                if( messages[key][i].message.loadAverageMinute.hasOwnProperty(p) ) {
                    req.write('\n');
                    req.write('engine=' + engine + ' instanceID=' + instanceID + ' instanceResourceID=' + instanceResourceID + ' version=' + version + ' loadAverageMinute=' + p + '  type=loadAverageMinute ' + messages[key][i].message.loadAverageMinute[p] + ' ' + epoch_timestamp);
                } 
            }     
            
            // memory
            for (var p in messages[key][i].message.memory){
                if( messages[key][i].message.memory.hasOwnProperty(p) ) {
                    req.write('\n');
                    req.write('engine=' + engine + ' instanceID=' + instanceID + ' instanceResourceID=' + instanceResourceID + ' version=' + version + ' memory=' + p + '  type=memory ' + messages[key][i].message.memory[p] + ' ' + epoch_timestamp);
                }
            }
            
            // tasks
            for (var p in messages[key][i].message.tasks){
                if( messages[key][i].message.tasks.hasOwnProperty(p) ) {
                    req.write('\n');
                    req.write('engine=' + engine + ' instanceID=' + instanceID + ' instanceResourceID=' + instanceResourceID + ' version=' + version + ' tasks=' + p + '  type=tasks ' + messages[key][i].message.tasks[p] + ' ' + epoch_timestamp);
                }
            }
            
            // swap
            for (var p in messages[key][i].message.swap){
                if( messages[key][i].message.swap.hasOwnProperty(p) ) {
                    req.write('\n');
                    req.write('engine=' + engine + ' instanceID=' + instanceID + ' instanceResourceID=' + instanceResourceID + ' version=' + version + ' swap=' + p + '  type=swap ' + messages[key][i].message.swap[p] + ' ' + epoch_timestamp);
                }
            }
            
            // network
            messages[key][i].message.network.forEach(function(obj) {
                for (var p in obj){
                    if( obj.hasOwnProperty(p) && p!='interface' ) {
                        req.write('\n');
                        req.write('engine=' + engine + ' instanceID=' + instanceID + ' instanceResourceID=' + instanceResourceID + ' version=' + version + ' network=' + p + ' interface=' + obj.interface + '  type=network ' + obj[p] + ' ' + epoch_timestamp);
                    }
                }
            });
            
            // diskIO
            messages[key][i].message.diskIO.forEach(function(obj) {
                for (var p in obj){
                    if( obj.hasOwnProperty(p) && p!='device' ) {
                        req.write('\n');
                        req.write('engine=' + engine + ' instanceID=' + instanceID + ' instanceResourceID=' + instanceResourceID + ' version=' + version + ' diskIO=' + p + ' device=' + obj.device + '  type=diskIO ' + obj[p] + ' ' + epoch_timestamp);
                    }
                }
            });
            
            // fileSys
            messages[key][i].message.fileSys.forEach(function(obj) {
                for (var p in obj){
                    if( obj.hasOwnProperty(p) && p!='name' && p!='mountPoint' ) {
                        var obj_name=obj.name.replace(/\s+/g, '_');
                        req.write('\n');
                        req.write('engine=' + engine + ' instanceID=' + instanceID + ' instanceResourceID=' + instanceResourceID + ' version=' + version + ' fileSys=' + p + ' name=' + obj.name + ' mountPoint=' + obj.mountPoint + '  type=fileSys ' + obj[p] + ' ' + epoch_timestamp);
                    }
                }
            });
            
            // processList
            messages[key][i].message.processList.forEach(function(obj) {
                for (var p in obj){

                    if( obj.hasOwnProperty(p) && p != 'name' && p != 'vmlimit' && p != 'id' && p != 'tgid' && p != 'parentID') {
                        var obj_name=obj.name.replace(/\s+/g, '_');
                        var obj_vmlimit=obj.name.replace(/\s+/g, '_');
                        req.write('\n');
                        req.write('engine=' + engine + ' instanceID=' + instanceID + ' instanceResourceID=' + instanceResourceID + ' version=' + version + ' processList=' + p + ' name=' + obj_name + ' id=' + obj.id +' tgid=' + obj.tgid + ' parentID=' + obj.parentID + ' vmlimit=' + obj_vmlimit + '  type=processList ' + obj[p] + ' ' + epoch_timestamp);
                        
                    }
                }
            });
            
        }

        req.end();
    });
}


exports.handler = function (event, context) {
    
    // Used to hold chunks of messages to post to SumoLogic
    var messageList = {};

    // Validate URL has been set
    var urlObject = url.parse(SumoURL);
    if (urlObject.protocol != 'https:' || urlObject.host === null || urlObject.path === null) {
        context.fail('Invalid SUMO_ENDPOINT environment variable: ' + SumoURL);
    }
    
    var zippedInput = new Buffer(event.awslogs.data, 'base64');
    
    zlib.gunzip(zippedInput, function (e, buffer) {
        if (e) {
            context.fail(e);
        }
        
        var awslogsData = JSON.parse(buffer.toString(encoding));
        
        if (awslogsData.messageType === 'CONTROL_MESSAGE') {
            console.log('Control message');
            context.succeed('Success');
        }
        
        var lastRequestID = null;
        
        console.log('Log events: ' + awslogsData.logEvents.length);
        
        // Chunk log events before posting to SumoLogic
        awslogsData.logEvents.forEach(function (log, idx, arr) {
            
            // Remove any trailing \n
            log.message = log.message.replace(/\n$/, '');
            
            // Try extract requestID
            var requestId = requestIdRegex.exec(log.message);
            if (requestId !== null) {
                lastRequestID = requestId[1];
            }
            
            // Attempt to detect console log and auto extract requestID and message
            var consoleLog = consoleFormatRegex.exec(log.message);
            if (consoleLog !== null) {
                lastRequestID = consoleLog[1];
                log.message = log.message.substring(consoleLog[0].length);
            }
            
            // Auto detect if message is json
            try {
                //log.message = JSON.parse(log.message);
                log.message = JSON.parse(log.message)
            } catch (err) {
                // Do nothing, leave as text
                log.message.trim();
            }
            
            // delete id as it's not very useful
            delete log.id;
            
            if (includeLogInfo) {
                log.logStream = awslogsData.logStream;
                log.logGroup = awslogsData.logGroup;
            }
            
            if (lastRequestID) {
                log.requestID = lastRequestID;
            }
            
            var metadataKey = sumoMetaKey(awslogsData, log.message);
            
            if (metadataKey in messageList) {
                messageList[metadataKey].push(log);
            } else {
                messageList[metadataKey] = [log];
            }
        });
        
        // Push messages to Sumo
        postToSumo(context, messageList);
        
    });
};