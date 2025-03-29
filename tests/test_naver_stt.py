import os
import asyncio
import pytest
import difflib
from edge_tts import Communicate
from pydub import AudioSegment
from app.core.naver_stt import NaverSTT
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
    "음성 인식 서버가 잘 작동하는지 확인해보겠습니다.",
    "안녕하세요, 저는 음성 인식 서버입니다.",
    "오늘은 2024년 3월 30일입니다.",
    "음성 인식 정확도가 얼마나 높은지 테스트해보겠습니다.",
    "이 문장은 한글과 영어가 섞여 있습니다. Hello World!",
    "음성 인식 서버가 잘 작동하는지 확인해보겠습니다. 음성 인식 서버가 잘 작동하는지 확인해보겠습니다. 음성 인식 서버가 잘 작동하는지 확인해보겠습니다.음성 인식 서버가 잘 작동하는지 확인해보겠습니다."
]

def calculate_similarity(text1: str, text2: str) -> float:
    """두 텍스트 간의 유사도를 계산합니다."""
    return difflib.SequenceMatcher(None, text1, text2).ratio()

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
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== STT 테스트 결과 ==={Colors.END}")
    print(f"{Colors.BOLD}번호 | 원본 텍스트 | 인식 결과 | 유사도{Colors.END}")
    print("-" * 100)
    
    total_similarity = 0
    successful_tests = 0
    
    # 각 텍스트에 대해 순차적으로 처리
    for i, text in enumerate(TEST_TEXTS, 1):
        print(f"\n{Colors.CYAN}{Colors.BOLD}{i}번 테스트 진행 중...{Colors.END}")
        
        # 1. 음성 파일 생성
        filepath = asyncio.run(generate_test_audio(text, f"test_{i}.wav"))
        print(f"{Colors.BLUE}생성된 파일: {filepath}{Colors.END}")
        
        # 2. STT 테스트
        with open(filepath, "rb") as f:
            audio_data = f.read()
        
        result = stt.recognize(audio_data, lang="Kor")
        
        # 3. 결과 출력
        if result.get("error"):
            print(f"{Colors.RED}{i:2d} | 오류 발생: {result['error']}{Colors.END}")
        else:
            similarity = calculate_similarity(text, result["text"])
            total_similarity += similarity
            successful_tests += 1
            
            print(f"{Colors.GREEN}{i:2d} | {text}{Colors.END}")
            print(f"   | {result['text']}")
            print(f"   | 유사도: {similarity:.2%}")
        
        # 검증
        assert result is not None, f"{i}번 테스트 처리 중 오류 발생"
        if not result.get("error"):
            assert isinstance(result["text"], str), "인식 결과가 문자열이 아님"
            assert len(result["text"]) > 0, "인식 결과가 비어있음"
            assert result["audio_info"]["duration"] <= 60, "오디오 길이가 60초를 초과함"
    
    # 평균 유사도 계산 및 출력
    if successful_tests > 0:
        avg_similarity = total_similarity / successful_tests
        print(f"\n{Colors.HEADER}{Colors.BOLD}=== 테스트 완료 ==={Colors.END}")
        print(f"{Colors.GREEN}성공한 테스트 수: {successful_tests}/{len(TEST_TEXTS)}{Colors.END}")
        print(f"{Colors.GREEN}평균 유사도: {avg_similarity:.2%}{Colors.END}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}=== 테스트 실패 ==={Colors.END}")
        print(f"{Colors.RED}성공한 테스트가 없습니다.{Colors.END}") 