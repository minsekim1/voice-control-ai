package com.minsekim.voicecontrol

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.minsekim.voicecontrol.ui.theme.VoicecontrolTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            VoicecontrolTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    MainScreen()
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen() {
    var showServerIpDialog by remember { mutableStateOf(false) }
    var serverIp by remember { mutableStateOf("") }

    Scaffold(
        modifier = Modifier.fillMaxSize(),
        containerColor = MaterialTheme.colorScheme.background
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Button(
                onClick = { showServerIpDialog = true },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("서버 IP 입력하기")
            }
        }

        if (showServerIpDialog) {
            AlertDialog(
                onDismissRequest = { showServerIpDialog = false },
                title = { Text("서버 IP 설정") },
                text = {
                    OutlinedTextField(
                        value = serverIp,
                        onValueChange = { serverIp = it },
                        label = { Text("서버 IP 주소") },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true
                    )
                },
                confirmButton = {
                    TextButton(
                        onClick = {
                            // TODO: 서버 IP 적용 로직
                            showServerIpDialog = false
                        }
                    ) {
                        Text("적용")
                    }
                },
                dismissButton = {
                    TextButton(
                        onClick = { showServerIpDialog = false }
                    ) {
                        Text("닫기")
                    }
                }
            )
        }
    }
}