package com.example.tanay.firstapp;

import android.app.Application;
import android.content.Context;
import org.acra.*;
import org.acra.annotation.*;
import org.acra.config.CoreConfigurationBuilder;
import org.acra.config.HttpSenderConfigurationBuilder;
import org.acra.config.LimiterConfigurationBuilder;
import org.acra.data.StringFormat;
import org.acra.sender.HttpSender;

@AcraCore(buildConfigClass = BuildConfig.class)
public class MyApplication extends Application {
  @Override
  protected void attachBaseContext(Context base) {
    super.attachBaseContext(base);
    CoreConfigurationBuilder builder = new CoreConfigurationBuilder(this)
            .setBuildConfigClass(BuildConfig.class)
            .setReportFormat(StringFormat.JSON);
    builder.getPluginConfigurationBuilder(HttpSenderConfigurationBuilder.class)
            .setUri("https://long-events.sumologic.net/receiver/v1/http/ZaVnC4dhaV1KvhDc5bIvvcdN01IcbSMWQ4BXmLfRwuGGw1_RE0JKFrq0b_w5fJo0LZADZW0SLNTwPvzArMQT3NuqavePh_4nuZEzHBXZtMdrVW7yaXkG_Q==")
            .setHttpMethod(HttpSender.Method.POST)
            .setEnabled(true);
    builder.getPluginConfigurationBuilder(LimiterConfigurationBuilder.class)
            .setEnabled(true);
    ACRA.init(this, builder);
  }
}
