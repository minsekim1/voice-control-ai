import os
import asyncio
from datetime import datetime
from edge_tts import Communicate
from pydub import AudioSegment
from app.core.naver_stt import NaverSTT
from dotenv import load_dotenv

async def generate_test_audio(text: str, output_dir: str = "test_audio") -> str:
    """
    테스트용 오디오 파일 생성
    
    Args:
        text: 생성할 텍스트
        output_dir: 출력 디렉토리
        
    Returns:
        str: 생성된 파일 경로
    """
    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 파일명 생성 (타임스탬프 포함)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_audio_{timestamp}.wav"
    filepath = os.path.join(output_dir, filename)
    
    # 임시 MP3 파일 경로
    temp_mp3 = filepath.replace(".wav", "_temp.mp3")
    
    try:
        # Edge TTS로 음성 생성
        communicate = Communicate(text, "ko-KR-SunHiNeural")
        await communicate.save(temp_mp3)
        
        # MP3를 WAV로 변환
        audio = AudioSegment.from_mp3(temp_mp3)
        
        # 모노로 변환하고 16kHz로 리샘플링
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)
        
        # WAV 파일로 저장
        audio.export(
            filepath,
            format="wav",
            parameters=[
                "-acodec", "pcm_s16le",  # 16-bit PCM
                "-ar", "16000",          # 16kHz sample rate
                "-ac", "1"               # mono
            ]
        )
        
        print(f"테스트 오디오 파일 생성 완료: {filepath}")
        return filepath
        
    finally:
        # 임시 MP3 파일 삭제
        if os.path.exists(temp_mp3):
            os.remove(temp_mp3)

def test_stt(filepath: str):
    """
    STT 테스트 실행
    
    Args:
        filepath: 테스트할 오디오 파일 경로
    """
    try:
        # 환경 변수 로드
        load_dotenv()
        
        # STT 클라이언트 초기화
        client_id = os.getenv("NAVER_CLIENT_ID")
        client_secret = os.getenv("NAVER_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            raise ValueError("네이버 클라우드 인증 정보가 설정되지 않았습니다.")
        
        stt = NaverSTT(client_id, client_secret)
        
        # 오디오 파일 읽기
        with open(filepath, 'rb') as f:
            audio_data = f.read()
        
        # 음성 인식 실행
        result = stt.recognize(audio_data)
        
        print("\n=== STT 테스트 결과 ===")
        print(f"파일: {filepath}")
        print(f"인식된 텍스트: {result['text']}")
        print(f"오디오 정보: {result['audio_info']}")
        
    except Exception as e:
        print(f"테스트 중 오류 발생: {str(e)}")

async def main():
    """메인 함수"""
    # 테스트 텍스트 목록
    test_texts = [
        "안녕하세요",
        "Hello World",
        "테스트 음성입니다",
        "음성 인식 서버가 잘 작동하는지 확인해보겠습니다. 음성 인식 서버가 잘 작동하는지 확인해보겠습니다. 음성 인식 서버가 잘 작동하는지 확인해보겠습니다."
    ]
    
    print("=== 테스트 오디오 생성 및 STT 테스트 시작 ===")
    
    for text in test_texts:
        print(f"\n테스트 텍스트: {text}")
        filepath = await generate_test_audio(text)
        test_stt(filepath)
    
    print("\n=== 테스트 완료 ===")

if __name__ == "__main__":
    asyncio.run(main()) 