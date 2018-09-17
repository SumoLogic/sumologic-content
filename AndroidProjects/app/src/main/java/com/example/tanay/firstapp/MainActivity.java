package com.example.tanay.firstapp;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;

import com.hypertrack.hyperlog.HyperLog;

import org.apache.log4j.Logger;

public class MainActivity extends AppCompatActivity {
	public static final String EXTRA_MESSAGE = "com.example.tanay.firstapp.MESSAGE";
	public static final String LOG_TAG = "MainActivity";

	private final Logger log = ALogger.getLogger(MainActivity.class);

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		HyperLog.initialize(this);
		HyperLog.setLogLevel(Log.VERBOSE);

	}

	/** Called when the user presses the send button */
	public void sendMessage(View view) {
		Intent intent = new Intent(this, DisplayMessageActivity.class);
		EditText editText = (EditText) findViewById(R.id.editText);
		// Log.v(LOG_TAG, "Button Pushed!");
		// log.info("This message should be seen in log file and logcat");
		HyperLog.d(LOG_TAG, "Debug Log");
		String message = editText.getText().toString();
		intent.putExtra(EXTRA_MESSAGE, message);
		startActivity(intent);
	}
}
