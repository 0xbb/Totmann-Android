package net.bierbaumer.totmann;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

public class UserPresentReceiver extends BroadcastReceiver {
    public static final String TAG = "UserPresentReceiver";

    @Override
    public void onReceive(Context context, Intent intent) {
        Log.d(TAG, "onReceive");

        AlarmReceiver.scheduleAlarm(context);
    }
}
