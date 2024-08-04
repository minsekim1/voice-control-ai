package com.campustech.iot;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import java.io.IOException;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.SocketException;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.TimeUnit;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {
    private static final int PERMISSION_REQUEST_CODE = 100;
    private static final String TAG = "MainActivity";

    private TextView connectionStatus;
    private Button buttonFindEsp32;
    private Button buttonLedControl;
    private EditText inputPin;
    private EditText inputValue;

    private String esp32Ip;

    private Boolean found;
    private String subnet = null;
    private int failedCount = 0;
    private Toast currentToast = null;

    private Handler handler = new Handler(Looper.getMainLooper());
    private Runnable pingRunnable;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        connectionStatus = findViewById(R.id.connection_status);
        buttonFindEsp32 = findViewById(R.id.button_find_esp32);
        buttonLedControl = findViewById(R.id.button_led_control);
        inputPin = findViewById(R.id.input_pin);
        inputValue = findViewById(R.id.input_value);

        buttonFindEsp32.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                findESP32();
            }
        });

        buttonLedControl.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                controlLED();
            }
        });

        checkAndRequestPermissions();
    }

    private boolean checkAndRequestPermissions() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_WIFI_STATE) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_WIFI_STATE}, PERMISSION_REQUEST_CODE);
            return false;
        }
        return true;
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == PERMISSION_REQUEST_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // 권한이 허용됨
            } else {
                Toast.makeText(this, "Permission denied", Toast.LENGTH_SHORT).show();
            }
        }
    }

    private void findESP32() {
        new Thread(() -> {
            found = false;
            failedCount = 0;

            String localIp = getLocalIpAddress();
            subnet = localIp != null ? localIp.substring(0, localIp.lastIndexOf('.') + 1) : null;

            if (subnet != null) {
                OkHttpClient client = new OkHttpClient.Builder()
                        .connectTimeout(1, TimeUnit.SECONDS)
                        .readTimeout(1, TimeUnit.SECONDS)
                        .writeTimeout(1, TimeUnit.SECONDS)
                        .build();

                for (int i = 1; i <= 253; i++) {
                    String ip = subnet + i;
                    Request request = new Request.Builder()
                            .url("http://" + ip + "/network/status")
                            .build();

                    client.newCall(request).enqueue(new okhttp3.Callback() {
                        @Override
                        public void onFailure(okhttp3.Call call, IOException e) {
                            incrementFailedCount();
                        }

                        @Override
                        public void onResponse(okhttp3.Call call, Response response) throws IOException {
                            if (response.isSuccessful()) {
                                synchronized (found) {
                                    if (!found) {
                                        found = true;
                                        esp32Ip = ip;
                                        runOnUiThread(() -> {
                                            connectionStatus.setText("ESP32 Status: Connected (" + esp32Ip + ")");
                                            connectionStatus.setTextColor(getResources().getColor(android.R.color.holo_green_dark));
                                            showToast("ESP32 found at: " + esp32Ip);
                                            startPingTask();
                                        });
                                    }
                                }
                            } else {
                                incrementFailedCount();
                            }
                        }
                    });
                }
            } else {
                runOnUiThread(() -> {
                    connectionStatus.setText("ESP32 Status: Not connected");
                    connectionStatus.setTextColor(getResources().getColor(android.R.color.holo_red_dark));
                    showToast("Failed to find IoT Device in the network");
                });
            }
        }).start();
    }

    private void showToast(String message) {
        if (currentToast != null) {
            currentToast.cancel();
        }
        currentToast = Toast.makeText(MainActivity.this, message, Toast.LENGTH_SHORT);
        currentToast.show();
    }

    private synchronized void incrementFailedCount() {
        failedCount++;
        if (failedCount >= 253 && !found) {
            failedCount = 0;
            runOnUiThread(() -> {
                connectionStatus.setText("ESP32 Status: Not connected");
                connectionStatus.setTextColor(getResources().getColor(android.R.color.holo_red_dark));
                showToast("Failed to find IoT Device in the network");
            });
        }
    }

    private void controlLED() {
        if (esp32Ip == null || esp32Ip.isEmpty()) {
            Toast.makeText(this, "ESP32 not connected. Please find ESP32 first.", Toast.LENGTH_SHORT).show();
            return;
        }

        String pin = inputPin.getText().toString().trim();
        String value = inputValue.getText().toString().trim();

        if (pin.isEmpty() || value.isEmpty()) {
            Toast.makeText(this, "Please enter both pin and value", Toast.LENGTH_SHORT).show();
            return;
        }

        int pinValue = Integer.parseInt(value);
        if (pinValue < 0 || pinValue > 255) {
            Toast.makeText(this, "Brightness value must be between 0 and 255", Toast.LENGTH_SHORT).show();
            return;
        }

        OkHttpClient client = new OkHttpClient();
        String url = "http://" + esp32Ip + "/pin/control?pin=" + pin + "&value=" + pinValue;

        Request request = new Request.Builder()
                .url(url)
                .build();

        new Thread(() -> {
            try {
                Response response = client.newCall(request).execute();
                if (response.isSuccessful()) {
                    Log.i(TAG, "LED controlled successfully");
                    runOnUiThread(() -> Toast.makeText(MainActivity.this, "LED controlled successfully", Toast.LENGTH_SHORT).show());
                }
            } catch (IOException e) {
                Log.e(TAG, "Error controlling LED", e);
            }
        }).start();
    }

    private String getLocalIpAddress() {
        try {
            List<NetworkInterface> interfaces = Collections.list(NetworkInterface.getNetworkInterfaces());
            for (NetworkInterface intf : interfaces) {
                List<InetAddress> addrs = Collections.list(intf.getInetAddresses());
                for (InetAddress addr : addrs) {
                    if (!addr.isLoopbackAddress() && addr.isSiteLocalAddress() && addr instanceof java.net.Inet4Address) {
                        return addr.getHostAddress();
                    }
                }
            }
        } catch (SocketException ex) {
            Log.e(TAG, ex.toString());
        }
        return null;
    }

    private void startPingTask() {
        if (pingRunnable != null) {
            handler.removeCallbacks(pingRunnable);
        }

        pingRunnable = new Runnable() {
            @Override
            public void run() {
                pingESP32();
                handler.postDelayed(this, 1000); // 1초마다 실행
            }
        };

        handler.post(pingRunnable);
    }

    private void pingESP32() {
        if (esp32Ip == null || esp32Ip.isEmpty()) {
            return;
        }

        OkHttpClient client = new OkHttpClient.Builder()
                .connectTimeout(1, TimeUnit.SECONDS)
                .readTimeout(1, TimeUnit.SECONDS)
                .writeTimeout(1, TimeUnit.SECONDS)
                .build();

        Request request = new Request.Builder()
                .url("http://" + esp32Ip + "/network/status")
                .build();

        new Thread(() -> {
            try {
                Response response = client.newCall(request).execute();
                if (response.isSuccessful()) {
                    runOnUiThread(() -> {
                        connectionStatus.setText("ESP32 Status: Connected (" + esp32Ip + ")");
                        connectionStatus.setTextColor(getResources().getColor(android.R.color.holo_green_dark));
                    });
                } else {
                    runOnUiThread(() -> {
                        connectionStatus.setText("ESP32 Status: Disconnected");
                        connectionStatus.setTextColor(getResources().getColor(android.R.color.holo_red_dark));
                    });
                }
            } catch (IOException e) {
                runOnUiThread(() -> {
                    connectionStatus.setText("ESP32 Status: Disconnected");
                    connectionStatus.setTextColor(getResources().getColor(android.R.color.holo_red_dark));
                });
            }
        }).start();
    }
}
