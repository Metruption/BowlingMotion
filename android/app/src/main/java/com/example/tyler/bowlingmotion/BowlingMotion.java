package com.example.tyler.bowlingmotion;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.AsyncTask;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import java.util.Random;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;


public class BowlingMotion extends AppCompatActivity implements SensorEventListener, View.OnTouchListener {
    private Button b;
    private TextView test;
    private SensorManager manager;
    private Sensor acc;
    private float x;
    private float y;
    private float z;
    private Handler mHandler = new Handler();
    private boolean pressed = false;
    MqttAndroidClient client;
    String deviceID;
    Queue<Float> xStream,yStream,zStream;
    Queue<Integer> timeStream;
    /*starts the app, adds the listener to the center button to allow it to collect data when it is pressed,
    initializes all variables need globally*/



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_bowling_motion);
        //connedtToServer();
        manager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        acc = manager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        manager.registerListener(this, acc, SensorManager.SENSOR_DELAY_NORMAL);
        b = (Button) findViewById(R.id.activation);
        //allow center button to capture motion
        b.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                switch (event.getAction()) {
                    //capture motion when button is pressed down
                    case MotionEvent.ACTION_DOWN:
                        //b.setText("x:" + x + " y: " + y + " z: " + z);
                        if (pressed == false) {
                            pressed = true;
                            new ButtonPressed().execute();
                        }
                        break;
                    //send data to server when button is released
                    case MotionEvent.ACTION_UP:

                        pressed = false;
                        try {
                            messageServer();
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                        break;


                }
                return false;
            }

        });
        test = (TextView) findViewById(R.id.title);
        xStream=new ConcurrentLinkedQueue<Float>();
        yStream=new ConcurrentLinkedQueue<Float>();
        zStream=new ConcurrentLinkedQueue<Float>();
        timeStream=new ConcurrentLinkedQueue<>();
    }
    /*sends the data that was collected when the buttons was pressed down
     converts the queues collected during the pressdown to jsonn arrays
     */
    private void messageServer() throws JSONException {
        JSONArray xArray = new JSONArray();
        JSONArray yArray = new JSONArray();
        JSONArray zArray = new JSONArray();
        JSONArray timeArray=new JSONArray();
        JSONObject data = new JSONObject();


        while(!xStream.isEmpty()){

            xArray.put(xStream.remove());
            yArray.put(yStream.remove());
            zArray.put(zStream.remove());
            timeArray.put(timeStream.remove());
        }
        xStream.clear();
        yStream.clear();
        zStream.clear();
        timeStream.clear();

        data.put("x",xArray);
        data.put("y",yArray);
        data.put("z",zArray);
        data.put("time",timeArray);


        String topic = "device/" + deviceID;
        String payload = data.toString();
        Log.d("output", data.toString(2));
        byte[] encodedPayload = new byte[0];
        try {
            encodedPayload = payload.getBytes("UTF-8");
            MqttMessage message = new MqttMessage(encodedPayload);
            client.publish(topic, message);
        } catch (UnsupportedEncodingException | MqttException e) {
            e.printStackTrace();
        }
    }
    /*connects app to server, is done when app is restarted or initialized*/

    private void connectToServer() {
        Random randy=new Random();
        int rand=randy.nextInt(9999);
        deviceID = Integer.toString(rand);
        String clientId = MqttClient.generateClientId();
        // Set destination server
        client =
                new MqttAndroidClient(this.getApplicationContext(), "tcp://ec2-52-23-213-20.compute-1.amazonaws.com:1883",
                        clientId);
        // set Last Will Testment
        MqttConnectOptions options = new MqttConnectOptions();
        final String LWTtopic = "status/device/" + deviceID;
        byte[] LWTpayload = "".getBytes();
        options.setWill(LWTtopic, LWTpayload ,1,true);

        try {
            IMqttToken token = client.connect(options);
            token.setActionCallback(new IMqttActionListener() {
                public static final String TAG = "jamie";

                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    // We are connected
                    Log.d(TAG, "onSuccess");
                    try {
                        client.publish(LWTtopic, "1".getBytes(), 1, true);
                    } catch (MqttException e) {
                        e.printStackTrace();
                    }
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    // Something went wrong e.g. connection timeout or firewall problems
                    Log.d(TAG, "onFailure");

                }
            });
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    protected void onPause() {
        super.onPause();
        manager.unregisterListener(this);
        try {
            client.disconnect();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    protected void onResume() {
        super.onResume();
        manager.registerListener(this, acc, SensorManager.SENSOR_DELAY_NORMAL);
        connectToServer();
    }

   /* method for allowing volume button to capture data*/
    public boolean dispatchKeyEvent(KeyEvent event) {
        int action = event.getAction();
        int keyCode = event.getKeyCode();
        if(keyCode==KeyEvent.KEYCODE_VOLUME_DOWN) {
            switch (event.getAction()) {

                case MotionEvent.ACTION_DOWN:
                    //b.setText("x:" + x + " y: " + y + " z: " + z);
                    if (pressed == false) {
                        pressed = true;
                        new ButtonPressed().execute();
                    }
                    break;
                case MotionEvent.ACTION_UP:

                    pressed = false;
                    try {
                        messageServer();
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                    break;


            }
            return true;
        }
        return false;
    }




/*allows device to capture accelerometer data*/
    @Override
    public void onSensorChanged(SensorEvent sensorEvent) {
        Sensor mySensor = sensorEvent.sensor;

        if (mySensor.getType() == Sensor.TYPE_ACCELEROMETER) {
            x = sensorEvent.values[0];
            y = sensorEvent.values[1];
            z = sensorEvent.values[2];
        }
    }





/*special anonymous class that allows me to have the button pressed and continue collecting data until the
button is released, need to be in a separate anonymous class in order to not get stuck in a loop
 */
    class ButtonPressed extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... arg0) {
            while (pressed) {
                mHandler.postDelayed(new Runnable() {
                    public void run() {
                        int time = (int) (System.currentTimeMillis());
                        if(time%50==0) {
                            if(xStream.size()>9){
                                xStream.remove();
                                yStream.remove();
                                zStream.remove();
                                timeStream.remove();
                            }
                            b.setText("x:" + x + " y: " + y + " z: " + z);
                            xStream.add((Float)x);
                            yStream.add((Float)y);
                            zStream.add((Float)z);
                            timeStream.add(time);
                        }

                    }
                }, 0);

            }
            return null;
        }
    }
    @Override
    public void onAccuracyChanged(Sensor sensor, int i) {

    }
    @Override
    public boolean onTouch(View view, MotionEvent motionEvent) {
        if ((view.equals(b))) {

        }

        return true;
    }
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_VOLUME_DOWN
                || keyCode == KeyEvent.KEYCODE_VOLUME_DOWN)
            return true;
        else
            return true;
    }
}
