package com.minsekim.voicecontrol

import android.Manifest
import android.content.pm.PackageManager
import android.media.MediaRecorder
import android.os.Bundle
import android.os.Environment
import android.util.Log
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Image
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.PressInteraction
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import com.minsekim.voicecontrol.ui.theme.VoicecontrolTheme
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.asRequestBody
import java.io.File
import java.io.IOException

class MainActivity : ComponentActivity() {
    private var mediaRecorder: MediaRecorder? = null
    private var audioFile: File? = null
    private var serverIp: String = ""
    private var serverResponse: String = ""

    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        if (permissions.all { it.value }) {
            // 권한이 모두 승인됨
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        
        // 필요한 권한 요청
        requestPermissions()

        setContent {
            VoicecontrolTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    MainScreen(
                        onStartRecording = { startRecording() },
                        onStopRecording = { stopRecording() },
                        onServerIpSet = { ip -> serverIp = ip },
                        serverResponse = serverResponse
                    )
                }
            }
        }
    }

    private fun showToast(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }

    private fun requestPermissions() {
        val permissions = arrayOf(
            Manifest.permission.RECORD_AUDIO,
            Manifest.permission.WRITE_EXTERNAL_STORAGE
        )

        if (permissions.all { ContextCompat.checkSelfPermission(this, it) == PackageManager.PERMISSION_GRANTED }) {
            // 이미 권한이 있는 경우
        } else {
            requestPermissionLauncher.launch(permissions)
        }
    }

    private fun startRecording() {
        try {
            // 이미 녹음 중이면 중지
            if (mediaRecorder != null) {
                stopRecording()
            }

            val outputDir = getExternalFilesDir(Environment.DIRECTORY_MUSIC)
            audioFile = File.createTempFile("audio_", ".m4a", outputDir)

            mediaRecorder = MediaRecorder().apply {
                setAudioSource(MediaRecorder.AudioSource.MIC)
                setOutputFormat(MediaRecorder.OutputFormat.MPEG_4)
                setAudioEncoder(MediaRecorder.AudioEncoder.AAC)
                setOutputFile(audioFile?.absolutePath)
                prepare()
                start()
            }
        } catch (e: IOException) {
            Log.e("MainActivity", "녹음 시작 실패", e)
            showToast("녹음 시작 실패")
            stopRecording()
        }
    }

    private fun stopRecording() {
        try {
            mediaRecorder?.apply {
                try {
                    stop()
                } catch (e: IllegalStateException) {
                    Log.e("MainActivity", "녹음 중지 실패: 녹음 중이 아님", e)
                    showToast("녹음 중지 실패")
                }
                release()
            }
            mediaRecorder = null

            // 녹음된 파일을 서버로 전송
            audioFile?.let { file ->
                if (file.exists() && file.length() > 0) {
                    sendAudioToServer(file)
                } else {
                    Log.e("MainActivity", "녹음 파일이 없거나 비어있음")
                    showToast("녹음 파일이 없거나 비어있음")
                }
            }
        } catch (e: Exception) {
            Log.e("MainActivity", "녹음 중지 실패", e)
            showToast("녹음 중지 실패")
        } finally {
            mediaRecorder = null
        }
    }

    private fun sendAudioToServer(file: File) {
        if (serverIp.isEmpty()) {
            Log.e("MainActivity", "서버 IP가 설정되지 않음")
            showToast("서버 IP를 먼저 설정해주세요")
            return
        }

        val client = OkHttpClient()
        val requestBody = MultipartBody.Builder()
            .setType(MultipartBody.FORM)
            .addFormDataPart(
                "audio",
                "audio.m4a",
                file.asRequestBody("audio/m4a".toMediaType())
            )
            .build()

        val request = Request.Builder()
            .url("http://$serverIp:3000/upload")
            .post(requestBody)
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                Log.e("MainActivity", "서버 전송 실패", e)
                runOnUiThread {
                    showToast("서버 전송 실패")
                }
            }

            override fun onResponse(call: Call, response: Response) {
                val responseBody = response.body?.string()
                Log.d("MainActivity", "서버 전송 성공: $responseBody")
                runOnUiThread {
                    serverResponse = responseBody ?: "응답 없음"
                }
            }
        })
    }

    override fun onDestroy() {
        super.onDestroy()
        stopRecording()
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen(
    onStartRecording: () -> Unit,
    onStopRecording: () -> Unit,
    onServerIpSet: (String) -> Unit,
    serverResponse: String
) {
    var showServerIpDialog by remember { mutableStateOf(false) }
    var serverIp by remember { mutableStateOf("") }
    var isRecording by remember { mutableStateOf(false) }

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
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            Button(
                onClick = { showServerIpDialog = true },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("서버 IP 입력하기")
            }

            Button(
                onClick = { },
                modifier = Modifier
                    .size(80.dp)
                    .clip(CircleShape),
                colors = ButtonDefaults.buttonColors(
                    containerColor = if (isRecording) 
                        MaterialTheme.colorScheme.error 
                    else 
                        MaterialTheme.colorScheme.primary
                ),
                interactionSource = remember { MutableInteractionSource() }
                    .also { interactionSource: MutableInteractionSource ->
                        LaunchedEffect(interactionSource) {
                            interactionSource.interactions.collect { interaction ->
                                when (interaction) {
                                    is PressInteraction.Release -> {
                                        if (isRecording) {
                                            isRecording = false
                                            onStopRecording()
                                        }
                                    }
                                    is PressInteraction.Press -> {
                                        isRecording = true
                                        onStartRecording()
                                    }
                                }
                            }
                        }
                    }
            ) {
                Image(
                    painter = painterResource(id = R.drawable.ic_mic),
                    contentDescription = "음성 녹음",
                    modifier = Modifier.size(32.dp)
                )
            }

            Text(
                text = serverResponse,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                textAlign = TextAlign.Center,
                style = MaterialTheme.typography.bodyLarge
            )
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
                            onServerIpSet(serverIp)
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