package net.bierbaumer.totmann;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;

public class MainActivity extends Activity {
    private static final String TAG = "MainActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Log.d(TAG,"onCreate");

        AlarmReceiver.scheduleAlarm(this);
   }

    public void onClickRebootButton(View view) {
        Log.d(TAG, "onClickRebootButton");

        AlarmReceiver.reboot(this);
    }
}
