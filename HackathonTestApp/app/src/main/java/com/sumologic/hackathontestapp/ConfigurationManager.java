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
    Log.v("Hi", "Initializing task!");
    log.info("Printing info log");
    this.serverUrl = serverUrl;
    this.sleep = sleep;
    run();
  }

  @Override
  public void run() {
    Log.v("Hey", "Hi see you after 10 seconds: " + Thread.currentThread().getId());
    log.debug("Printing debug log");
    log.error("Printing error log");
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
      url = extractUrl(jsonObject);
      sumoAppender.setUrl(url);

      // Extract and update the prefix
      prefix = extractPrefix(jsonObject);
      sumoAppender.setPrefix(prefix);

      // Extract and update the logging level
      logLevel = extractLogLevel(jsonObject);
      setLevel(logLevel);

    } catch (IOException e) {
      log.error(e.toString());
    }

    // sleep for some time
    try {
      Thread.sleep(sleep);
      run();
    } catch (InterruptedException e) {
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

  private String extractUrl(JSONObject jsonObject) {
    String url = null;
    try {
      url = jsonObject.getString("url");
    } catch (JSONException e) {
      log.error(e.toString());
    }
    Log.v("Hi", "Extracted URL is: " + url);
    return url;
  }

  private String extractPrefix(JSONObject jsonObject) {
    String prefix;
    try {
      prefix = jsonObject.getString("prefix");
    } catch (JSONException e) {
      log.error(e.toString());
      return null;
    }
    Log.v("Hi", "Extracted prefix is: " + prefix);
    return prefix;
  }

  private String extractLogLevel(JSONObject jsonObject) {
    String logLevel;
    try {
      logLevel = jsonObject.getString("logLevel");
    } catch (JSONException e) {
      log.error(e.toString());
      return null;
    }
    Log.v("Hi", "Extracted logLevel is: " + logLevel);
    return logLevel;
  }

  private void setLevel(String logLevel) {
    if (logLevel.equals("info")) {
      Log.v("Hi", "setting log level to info");
      root.setLevel(Level.INFO);
    } else if (logLevel.equals("debug")) {
      Log.v("Hi", "setting log level to debug");
      root.setLevel(Level.DEBUG);
    } else if (logLevel.equals("warn")) {
      Log.v("Hi", "setting log level to warn");
      root.setLevel(Level.WARN);
    } else if (logLevel.equals("error")) {
      Log.v("Hi", "setting log level to error");
      root.setLevel(Level.ERROR);
    } else {
      Log.v("Hi", "setting log level to others");
      root.setLevel(Level.INFO);
    }
  }
}
