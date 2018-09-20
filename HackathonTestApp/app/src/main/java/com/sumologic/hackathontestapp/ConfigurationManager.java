package com.sumologic.hackathontestapp;

import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.io.IOException;
import java.util.TimerTask;
import ch.qos.logback.classic.Level;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.Appender;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class ConfigurationManager extends TimerTask {

  private String serverUrl;
  private int sleep;
  private OkHttpClient client = new OkHttpClient();
  private Logger log = LoggerFactory.getLogger(MainActivity.class);
  private ch.qos.logback.classic.Logger root = (ch.qos.logback.classic.Logger) LoggerFactory.getLogger(Logger.ROOT_LOGGER_NAME);
  private Appender<ILoggingEvent> appender = root.getAppender("sumoAppender");
  private SumoAppender sumoAppender = appender instanceof SumoAppender ? ((SumoAppender) appender) : null;

  public ConfigurationManager(String serverUrl, int sleep) {
    log.debug("Hi", "Initializing task!");
    log.info("Printing info log");
    this.serverUrl = serverUrl;
    this.sleep = sleep;
    run();
  }

  @Override
  public void run() {
    log.debug("Started com.sumologic.hackathontestapp.ConfigurationManager.run");
    JSONObject jsonObject;
    String url;
    String prefix;
    String logLevel;

    Request request = new Request.Builder()
            .url(serverUrl)
            .addHeader("Accept", "application/json")
            .method("GET", null)
            .build();

    try {
      Response response = client.newCall(request).execute();
      jsonObject = extractJsonObject(response);

      // Extract and update the URL
      url = extract(jsonObject, "url");
      prefix = extract(jsonObject, "prefix");
      sumoAppender.setUrl(url);
      sumoAppender.setPrefix(prefix);
      logLevel= extract(jsonObject, "logLevel");
      setLevel(logLevel);

    } catch (IOException e) {
      log.error(e.toString());
    }
  }

  private JSONObject extractJsonObject(Response response) {
    JSONObject jsonObject = null;
    try {
      String responseString = response.body().string();
      try {
        jsonObject = new JSONObject(responseString);
      } catch (JSONException e) {
        log.error(e.toString());
      }
    } catch (IOException e) {
      log.error(e.toString());
    }
    return jsonObject;
  }

  private String extract(JSONObject jsonObject, String key) {
    String value = null;
    try {
      value = jsonObject.getString(key);
    } catch (JSONException e) {
      log.error(e.toString());
    }
    return value;
  }

  private void setLevel(String logLevel) {
    log.info("Going to set log level to " + logLevel);
    if (logLevel == null) {
      log.warn("Empty log level found");
      root.setLevel(Level.INFO);
    } else if(logLevel.equals("info")) {
      log.debug("setting log level to info");
      root.setLevel(Level.INFO);
    } else if (logLevel.equals("debug")) {
      log.debug("setting log level to debug");
      root.setLevel(Level.DEBUG);
    } else if (logLevel.equals("warn")) {
      log.debug("setting log level to warn");
      root.setLevel(Level.WARN);
    } else if (logLevel.equals("error")) {
      log.debug("setting log level to error");
      root.setLevel(Level.ERROR);
    } else {
      log.warn("No log level found");
      root.setLevel(Level.INFO);
    }
  }
}
