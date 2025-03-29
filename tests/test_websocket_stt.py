import os
import asyncio
import pytest
import websockets
import json
from edge_tts import Communicate
from pydub import AudioSegment
from dotenv import load_dotenv

# ANSI 컬러 코드
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'

# 환경 변수 로드
load_dotenv()

# 테스트 텍스트 목록
TEST_TEXTS = [
    "안녕하세요, 반갑습니다.",
    "오늘은 날씨가 좋네요.",
    "음성 인식 테스트를 진행합니다.",
    "이 음성은 테스트용입니다.",
    "음성 인식 서버가 잘 작동하는지 확인해보겠습니다."
]

async def generate_test_audio(text: str, filename: str, output_dir: str = "tests/audio") -> str:
    """테스트용 오디오 파일 생성"""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    temp_mp3 = filepath.replace(".wav", "_temp.mp3")
    
    try:
        communicate = Communicate(text, "ko-KR-SunHiNeural")
        await communicate.save(temp_mp3)
        
        audio = AudioSegment.from_mp3(temp_mp3)
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)
        
        audio.export(
            filepath,
            format="wav",
            parameters=[
                "-acodec", "pcm_s16le",
                "-ar", "16000",
                "-ac", "1"
            ]
        )
        return filepath
    finally:
        if os.path.exists(temp_mp3):
            os.remove(temp_mp3)

async def stream_audio_file(websocket, filepath: str, chunk_size: int = 1024):
    """오디오 파일을 청크 단위로 스트리밍"""
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            await websocket.send(chunk)
            await asyncio.sleep(0.1)  # 스트리밍 간격 조절

@pytest.mark.asyncio
async def test_websocket_stt():
    """WebSocket STT 테스트"""
    uri = "ws://localhost:8000/api/v1/recognition/stream"
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== WebSocket STT 테스트 ==={Colors.END}")
    print(f"{Colors.BOLD}번호 | 원본 텍스트 | 인식 결과{Colors.END}")
    print("-" * 100)
    
    async with websockets.connect(uri) as websocket:
        for i, text in enumerate(TEST_TEXTS, 1):
            print(f"\n{Colors.CYAN}{Colors.BOLD}{i}번 테스트 진행 중...{Colors.END}")
            
            # 1. 음성 파일 생성
            filepath = await generate_test_audio(text, f"test_ws_{i}.wav")
            print(f"{Colors.BLUE}생성된 파일: {filepath}{Colors.END}")
            
            # 2. WebSocket 스트리밍 테스트
            try:
                # 오디오 스트리밍 시작
                await stream_audio_file(websocket, filepath)
                
                # 스트리밍 종료 신호 전송
                await websocket.send(json.dumps({"end": True}))
                
                # 결과 수신
                response = await websocket.recv()
                result = json.loads(response)
                
                # 3. 결과 출력
                if result.get("error"):
                    print(f"{Colors.RED}{i:2d} | 오류 발생: {result['error']}{Colors.END}")
                else:
                    print(f"{Colors.GREEN}{i:2d} | {text}{Colors.END}")
                    print(f"   | {result['text']}")
                    
                    # 검증
                    assert isinstance(result["text"], str), "인식 결과가 문자열이 아님"
                    assert len(result["text"]) > 0, "인식 결과가 비어있음"
                    
            except Exception as e:
                print(f"{Colors.RED}{i:2d} | 테스트 실패: {str(e)}{Colors.END}")
                raise
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== WebSocket 테스트 완료 ==={Colors.END}") 