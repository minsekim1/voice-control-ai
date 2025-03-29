import os
import asyncio
import pytest
from edge_tts import Communicate
from pydub import AudioSegment
from app.core.naver_stt import NaverSTT
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 테스트 텍스트 목록
TEST_TEXTS = [
    "안녕하세요, 반갑습니다.",
    "오늘은 날씨가 좋네요.",
    "음성 인식 테스트를 진행합니다.",
    "이 음성은 테스트용입니다.",
    "음성 인식 서버가 잘 작동하는지 확인해보겠습니다.",
    "안녕하세요, 저는 음성 인식 서버입니다.",
    "오늘은 2024년 3월 30일입니다.",
    "음성 인식 정확도가 얼마나 높은지 테스트해보겠습니다.",
    "이 문장은 한글과 영어가 섞여 있습니다. Hello World!",
    "음성 인식 서버가 ㅈㄴ 잘 작동하는지 확인해보겠습니다. 음성 인식 서버가 잘 작동하는지 확인해보겠습니다. 음성 인식 서버가 잘 작동하는지 확인해보겠습니다.음성 인식 서버가 잘 작동하는지 확인해보겠습니다."
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

def test_naver_stt():
    """네이버 클라우드 STT API 테스트"""
    # 인증 정보 확인
    client_id = os.getenv("NAVER_CLOUD_ACCESS_KEY")
    client_secret = os.getenv("NAVER_CLOUD_SECRET_KEY")
    
    assert client_id is not None, "NAVER_CLOUD_ACCESS_KEY가 설정되지 않았습니다."
    assert client_secret is not None, "NAVER_CLOUD_SECRET_KEY가 설정되지 않았습니다."
    
    # STT 인스턴스 생성
    stt = NaverSTT(client_id, client_secret)
    
    print("\n=== STT 테스트 결과 ===")
    print("번호 | 원본 텍스트 | 인식 결과")
    print("-" * 80)
    
    # 각 텍스트에 대해 순차적으로 처리
    for i, text in enumerate(TEST_TEXTS, 1):
        print(f"\n{i}번 테스트 진행 중...")
        
        # 1. 음성 파일 생성
        filepath = asyncio.run(generate_test_audio(text, f"test_{i}.wav"))
        print(f"생성된 파일: {filepath}")
        
        # 2. STT 테스트
        with open(filepath, "rb") as f:
            audio_data = f.read()
        
        result = stt.recognize(audio_data, lang="Kor")
        
        # 3. 결과 출력
        if result.get("error"):
            print(f"{i:2d} | 오류 발생: {result['error']}")
        else:
            print(f"{i:2d} | {text}")
            print(f"   | {result['text']}")
        
        # 검증
        assert result is not None, f"{i}번 테스트 처리 중 오류 발생"
        if not result.get("error"):
            assert isinstance(result["text"], str), "인식 결과가 문자열이 아님"
            assert len(result["text"]) > 0, "인식 결과가 비어있음"
            assert result["audio_info"]["duration"] <= 60, "오디오 길이가 60초를 초과함"
    
    print("\n=== 테스트 완료 ===") 