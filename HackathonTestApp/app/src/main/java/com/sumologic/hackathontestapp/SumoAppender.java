package com.sumologic.hackathontestapp;

import android.util.Log;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.UnsynchronizedAppenderBase;


public class SumoAppender extends UnsynchronizedAppenderBase<ILoggingEvent> {
    private String url = null;
    private String sourceName = null;
    private String sourceHost = null;
    private String sourceCategory = null;
    private String prefix = null;

    public String getTestMessage() {
        return prefix;
    }

    public void setPrefix(String prefix) {
        if (prefix != null && !prefix.isEmpty()) {
            this.prefix = prefix;
        }
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        if (url != null && !url.isEmpty()) {
            this.url = url;
        }
    }

    public String getSourceName() {
        return sourceName;
    }

    public void setSourceName(String sourceName) {
        this.sourceName = sourceName;
    }

    public String getSourceHost() {
        return sourceHost;
    }

    public void setSourceHost(String sourceHost) {
        this.sourceHost = sourceHost;
    }

    public String getSourceCategory() {
        return sourceCategory;
    }

    public void setSourceCategory(String sourceCategory) {
        this.sourceCategory = sourceCategory;
    }

    private SumoHttpSender sender = new SumoHttpSender();
    public SumoAppender() {
        Log.v("Hi", "Init Sumo Appender!");
    }

    public void append(ILoggingEvent event) {
        Log.v("Hi", "Came to Sumo appender " + prefix + " " + event.getMessage());
        sender.testSend(event.getMessage(), getUrl());
    }
}
