package com.sumologic.hackathontestapp;

import android.Manifest;
import android.app.Activity;
import android.content.Context;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.StrictMode;
import android.provider.Settings;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.content.ContextCompat;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.telephony.TelephonyManager;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.Appender;
import okhttp3.OkHttpClient;


public class MainActivity extends AppCompatActivity {

    private Logger log = LoggerFactory.getLogger(MainActivity.class);
    private OkHttpClient client = new OkHttpClient();
    private Logger  sumoLogger = LoggerFactory.getLogger("Sumo logger");
    private Activity mActivity;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);
        mActivity = MainActivity.this;

        TelephonyManager telephonyManager = (TelephonyManager)getSystemService(Context.TELEPHONY_SERVICE);
        Log.v("Hi", "Permission state is: " + ContextCompat.checkSelfPermission(mActivity, Manifest.permission.READ_PHONE_STATE));
        if(ContextCompat.checkSelfPermission(mActivity, Manifest.permission.READ_PHONE_STATE) == PackageManager.PERMISSION_GRANTED) {
            String deviceId = telephonyManager.getDeviceId();
            log.debug("Device ID is: " + deviceId);
        }

        String android_id = Settings.Secure.getString(this.getContentResolver(), Settings.Secure.ANDROID_ID);

        log.error("Android ID : " + android_id);

        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                test();
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action",  null).show();
            }
        });

        // Action for INFO Button
        Button infoButton = (Button) findViewById(R.id.button2);
        infoButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Log.v("HI", "Info button pressed!");
                log.info("The INFO button was pressed!");
            }
        });

        // Action for ERROR Button
        Button errorButton = (Button) findViewById(R.id.button);
        errorButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Log.v("HI", "Error button pressed!");
                try {
                    throwException();
                } catch (Exception e) {
                    log.error("Error button was pressed. Throwing error", e);
                }
            }
        });

        // Action for SUMO SEND Button
        Button sendButton = (Button) findViewById(R.id.button3);
        final EditText editText = (EditText) findViewById(R.id.editText);
        sendButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Log.v("HI", "Sumo send button pressed!");
                final String message = editText.getText().toString();
                log.debug(message);
            }
        });


        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.addDrawerListener(toggle);
        toggle.syncState();

        postCreation();
    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    private void postCreation(){
        ConfigManager.scheduleJob(getApplicationContext());
    }

    private void throwException(){
        throw new IllegalArgumentException("Test stack trace exception");
    }

    private void test() {

        Double counter = Math.random();
        counter += 1;
        ch.qos.logback.classic.Logger root = (ch.qos.logback.classic.Logger) LoggerFactory.getLogger(Logger.ROOT_LOGGER_NAME);
        Appender<ILoggingEvent> appender = root.getAppender("sumoAppender");
        SumoAppender sumoAppender = appender instanceof SumoAppender ? ((SumoAppender) appender) : null;
        sumoAppender.setPrefix("" + counter);
        try {
            throwException();
        } catch (Exception e) {
            log.error("Some error thrown", e);
        }
    }
}
