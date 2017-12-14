package net.bierbaumer.totmann;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.PowerManager;
import android.os.SystemClock;
import android.util.Log;

public class AlarmReceiver extends BroadcastReceiver {
    public static final String TAG = "AlarmReceiver";
    public static final long TOTMANN_TIMEOUT = 5 * 24 * 60 * 60 * 1000;

    public static void scheduleAlarm(Context context) {
        Log.d(TAG,"scheduleAlarm");

        Intent intent = new Intent(context, AlarmReceiver.class);
        PendingIntent alarmIntent = PendingIntent.getBroadcast(context, 0, intent, 0);
        AlarmManager manager = (AlarmManager) context.getSystemService(Context.ALARM_SERVICE);
        manager.set(AlarmManager.ELAPSED_REALTIME_WAKEUP,  SystemClock.elapsedRealtime() + TOTMANN_TIMEOUT, alarmIntent);
    }

    public static void reboot(Context context){
        Log.w(TAG,"reboot");

        PowerManager pm = (PowerManager) context.getSystemService(Context.POWER_SERVICE);
        pm.reboot(null);
    }

    @Override
    public void onReceive(Context context, Intent intent) {
        Log.d(TAG,"onReceive");

        reboot(context);
    }
}
