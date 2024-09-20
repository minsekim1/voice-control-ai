package com.campustech.iot;

import android.Manifest;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Switch;
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
    private Switch inputToggle;
    private String esp32Ip = null;
    private String subnet = null;
    private Toast currentToast = null;
    private String inputType = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        connectionStatus = findViewById(R.id.connection_status);
        buttonFindEsp32 = findViewById(R.id.button_find_esp32);
        inputPin = findViewById(R.id.input_pin);
        inputValue = findViewById(R.id.input_value);
        inputToggle = findViewById(R.id.input_toggle);
        buttonLedControl = findViewById(R.id.button_led_control);

        buttonFindEsp32.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(esp32Ip != null) disconnectESP32();
                else findESP32();
            }
        });

        buttonLedControl.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                controlLED();
            }
        });

        // input_type 선택창
        Spinner spinner = findViewById(R.id.input_type);
        // 어댑터 생성
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this,
                R.array.options_array, android.R.layout.simple_spinner_item);
        // 드롭다운 레이아웃 스타일 지정
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        // 스피너에 어댑터 설정
        spinner.setAdapter(adapter);
        // 스피너 아이템 선택 리스너 설정
        spinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                // 선택된 아이템을 처리
                String newInputType = parent.getItemAtPosition(position).toString();
                inputType = newInputType;
                switch (inputType) {
                    case "All LED":
                        inputPin.setVisibility(View.GONE);
                        inputValue.setVisibility(View.GONE);
                        inputToggle.setVisibility(View.VISIBLE);
                        buttonLedControl.setVisibility(View.VISIBLE);
                        break;
                    case "Specific LED":
                        inputPin.setVisibility(View.VISIBLE);
                        inputValue.setVisibility(View.GONE);
                        inputToggle.setVisibility(View.VISIBLE);
                        buttonLedControl.setVisibility(View.VISIBLE);
                        break;
                    case "Motor":
                        inputPin.setVisibility(View.GONE);
                        inputValue.setVisibility(View.VISIBLE);
                        inputToggle.setVisibility(View.GONE);
                        buttonLedControl.setVisibility(View.VISIBLE);
                        break;
                    default:
                        inputPin.setVisibility(View.VISIBLE);
                        inputValue.setVisibility(View.VISIBLE);
                        inputToggle.setVisibility(View.GONE);
                        buttonLedControl.setVisibility(View.VISIBLE);
                        break;
                }
            }
            @Override
            public void onNothingSelected(AdapterView<?> parent) {
                // 선택되지 않았을 때 처리
            }
        });

        // 권한 처리 후 저장된 wifi ip 있는지 체크 후 연동
        checkAndRequestPermissions();

    }

    private boolean checkAndRequestPermissions() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_WIFI_STATE) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_WIFI_STATE}, PERMISSION_REQUEST_CODE);
            return false;
        }
        // 재연결시도

        if(esp32Ip == null){
            String ip = loadEsp32Ip();
            Log.i(TAG, "try to reconnect saved esp32Ip:"+ip);
            if(ip != null) checkIp(ip);
        }
        return true;
    }
    private void saveEsp32Ip(String ip) {
        SharedPreferences sharedPreferences = getSharedPreferences("MyAppPreferences", MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString("esp32Ip", ip);
        editor.apply();
    }
    private String loadEsp32Ip() {
        SharedPreferences sharedPreferences = getSharedPreferences("MyAppPreferences", MODE_PRIVATE);
        return sharedPreferences.getString("esp32Ip", null);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == PERMISSION_REQUEST_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {}
            else Toast.makeText(this, "Permission denied", Toast.LENGTH_SHORT).show();
        }
    }

    private void findESP32() {
        new Thread(() -> {
            Log.i(TAG, "func: findESP32");

            String localIp = getLocalIpAddress();
            subnet = (localIp != null) ? localIp.substring(0, localIp.lastIndexOf('.') + 1) : null;
            if (subnet == null) {
                runOnUiThread(() -> {
                    connectionStatus.setText("ESP32 Status: Wifi Not connected");
                    connectionStatus.setTextColor(getResources().getColor(android.R.color.holo_red_dark));
                    showToast("Failed to find wifi subnet");
                });
                return;
            }

            for (int i = 1; i <= 253; i++) {
                Log.i(TAG, esp32Ip + " i:"+ i);
                if (esp32Ip != null) break;
                checkIp(subnet + i);
                try {
                    Thread.sleep(1); // 50ms 대기
                } catch (InterruptedException e) {
                    runOnUiThread(() -> {
                        connectionStatus.setText("ESP32 Status: Failed to wait timer");
                        connectionStatus.setTextColor(getResources().getColor(android.R.color.holo_red_dark));
                        showToast("Failed to wait timer");
                    });
                    e.printStackTrace();
                }
                if(i == 253) {
                    runOnUiThread(() -> {
                        connectionStatus.setText("ESP32 Status: Failed to find ESP32");
                        connectionStatus.setTextColor(getResources().getColor(android.R.color.holo_red_dark));
                        showToast("Failed to find ESP32");
                    });
                }
            }

        }).start();
    }

    private void disconnectESP32 () {
        Log.i(TAG, "func: disconnectESP32");
        showToast("disconnect esp32, ip:"+esp32Ip);
        esp32Ip = null;
        subnet = null;

        runOnUiThread(() -> {
            connectionStatus.setText("ESP32 Status: Not connected");
            connectionStatus.setTextColor(ContextCompat.getColorStateList(getApplicationContext(), R.color.red_700));
            buttonFindEsp32.setText("Find ESP32");
            buttonFindEsp32.setBackgroundTintList(ContextCompat.getColorStateList(getApplicationContext(), R.color.green_500));
            buttonLedControl.setBackgroundTintList(ContextCompat.getColorStateList(getApplicationContext(), R.color.gray_700));
            showToast("disconnect ESP32");
            saveEsp32Ip(null);
        });

    }
    private void checkIp(String ip) {
        OkHttpClient client = new OkHttpClient.Builder()
                .connectTimeout(1000, TimeUnit.MILLISECONDS)
                .readTimeout(1000, TimeUnit.MILLISECONDS)
                .writeTimeout(1000, TimeUnit.MILLISECONDS)
                .build();

        Request request = new Request.Builder()
                .url("http://" + ip + "/network/status")
                .build();

        client.newCall(request).enqueue(new okhttp3.Callback() {
            @Override
            public void onFailure(okhttp3.Call call, IOException e) {
                // 여기서 실패 처리를 수행할 수 있습니다.
            }

            @Override
            public void onResponse(okhttp3.Call call, Response response) {
                Log.i(TAG, ip);
                if (response.isSuccessful()) {
                    synchronized (this) {
                        if (esp32Ip != null) return;
                        esp32Ip = ip;
                        runOnUiThread(() -> {
                            connectionStatus.setText("ESP32 Status: Connected (" + esp32Ip + ")");
                            connectionStatus.setTextColor(ContextCompat.getColorStateList(getApplicationContext(), R.color.green_500));
                            buttonFindEsp32.setText("Disconnect ESP32");
                            buttonFindEsp32.setBackgroundTintList(ContextCompat.getColorStateList(getApplicationContext(), R.color.gray_700));
                            buttonLedControl.setBackgroundTintList(ContextCompat.getColorStateList(getApplicationContext(), R.color.green_500));

                            showToast("ESP32 found at: " + esp32Ip);
                            saveEsp32Ip(esp32Ip);
                        });
                    }
                }
            }
        });
    }

    private void showToast(String message) {
        if (currentToast != null) currentToast.cancel();
        currentToast = Toast.makeText(MainActivity.this, message, Toast.LENGTH_SHORT);
        currentToast.show();
    }

    private void controlLED() {
        if (esp32Ip == null || esp32Ip.isEmpty()) {
            Toast.makeText(this, "ESP32 not connected. Please find ESP32 first.", Toast.LENGTH_SHORT).show();
            return;
        }

        String pin = inputPin.getText().toString().trim();
        int pinValue = inputToggle.isChecked() ? 1 : 0;


        if (!"All LED".equals(inputType) && pin.isEmpty()) {
            Toast.makeText(this, "Please enter pin number(s)", Toast.LENGTH_SHORT).show();
            return;
        }

        if (pinValue < 0 || pinValue > 255) {
            Toast.makeText(this, "Brightness value must be between 0 and 255", Toast.LENGTH_SHORT).show();
            return;
        }

        OkHttpClient client = new OkHttpClient();
        if ("All LED".equals(inputType)) {
            int[] allPins = {4, 3, 2, 1, 0, 5, 6, 7, 8, 9, 10, 20, 21};

            new Thread(() -> {
                for (int pinNumber : allPins) {
                    String url = "http://" + esp32Ip + "/pin/control?pin=" + pinNumber + "&value=" + pinValue;
                    Request request = new Request.Builder()
                            .url(url)
                            .build();

                    try {
                        Response response = client.newCall(request).execute();
                        if (response.isSuccessful()) {
                            Log.i(TAG, "LED on pin " + pinNumber + " controlled successfully");
                            runOnUiThread(() -> Toast.makeText(MainActivity.this, "LED on pin " + pinNumber + " controlled successfully", Toast.LENGTH_SHORT).show());
                        }
                        Thread.sleep(100); // 100ms 대기
                    } catch (IOException | InterruptedException e) {
                        Log.e(TAG, "Error controlling LED on pin " + pinNumber, e);
                    }
                }
            }).start();
        } else {
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
}
