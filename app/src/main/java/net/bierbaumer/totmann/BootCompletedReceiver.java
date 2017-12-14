package net.bierbaumer.totmann;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

public class BootCompletedReceiver extends BroadcastReceiver {
    private static final String TAG = "BootCompletedReceiver";

    @Override
    public void onReceive(Context context, Intent intent) {
        Log.d(TAG,"onReceive");
        if (intent.getAction().equals(Intent.ACTION_BOOT_COMPLETED)) {
            AlarmReceiver.scheduleAlarm(context);
        }
    }
}
