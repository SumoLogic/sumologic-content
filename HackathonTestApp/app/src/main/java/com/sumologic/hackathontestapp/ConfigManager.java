package com.sumologic.hackathontestapp;

import android.app.job.JobInfo;
import android.app.job.JobScheduler;
import android.content.ComponentName;
import android.content.Context;
import android.os.PersistableBundle;
import android.util.Log;

public class ConfigManager {
    static private String url = "http://ec2-54-145-154-222.compute-1.amazonaws.com/config.json";
    static private Long period = 2*1000L;

    public static void scheduleJob(Context context) {
        Log.i("ConfigManger", "Scheduling a job");
        ComponentName serviceComponent = new ComponentName(context, ConfigSyncService.class);
        PersistableBundle bundle = new PersistableBundle();
        bundle.putString("url", url);
        JobInfo.Builder builder = new JobInfo.Builder(0, serviceComponent);
        builder.setExtras(bundle);
        //builder.setPeriodic(period);

        builder.setRequiredNetworkType(JobInfo.NETWORK_TYPE_ANY);

        JobScheduler jobScheduler = context.getSystemService(JobScheduler.class);
        builder.setMinimumLatency(1000);
        if(jobScheduler.schedule(builder.build()) <= 0 ) {
            Log.e("ConfigManager","Some error with job scheduler");
        }
    }
}
