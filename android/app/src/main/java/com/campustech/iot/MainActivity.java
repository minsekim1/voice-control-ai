package com.campustech.iot;
import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import java.io.IOException;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {
    private static final int PERMISSION_REQUEST_CODE = 100;
    private static final String TAG = "MainActivity";

    private Button buttonLedControl;
    private EditText inputPin;
    private EditText inputValue;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        buttonLedControl = findViewById(R.id.button_led_control);
        inputPin = findViewById(R.id.input_pin);
        inputValue = findViewById(R.id.input_value);

        buttonLedControl.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                controlLED();
            }
        });

        // 권한 확인 및 요청
        checkAndRequestPermissions();
    }

    private boolean checkAndRequestPermissions() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, PERMISSION_REQUEST_CODE);
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

    private void controlLED() {
        String pin = inputPin.getText().toString().trim();
        String value = inputValue.getText().toString().trim();

        if (pin.isEmpty() || value.isEmpty()) {
            Toast.makeText(this, "Please enter both pin and value", Toast.LENGTH_SHORT).show();
            return;
        }

        int brightness = Integer.parseInt(value);
        if (brightness < 0 || brightness > 255) {
            Toast.makeText(this, "Brightness value must be between 0 and 255", Toast.LENGTH_SHORT).show();
            return;
        }

        OkHttpClient client = new OkHttpClient();
        String esp32Ip = "your-esp32-ip"; // ESP32의 IP 주소
        String url = "http://" + esp32Ip + "/led?pin=" + pin + "&brightness=" + brightness;

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
