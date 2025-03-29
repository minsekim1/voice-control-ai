import os
import pytest
from app.core.naver_stt import NaverSTT
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

def test_naver_stt():
    """네이버 클라우드 STT API 테스트"""
    # 인증 정보 확인
    client_id = os.getenv("NAVER_CLOUD_ACCESS_KEY")
    client_secret = os.getenv("NAVER_CLOUD_SECRET_KEY")
    
    assert client_id is not None, "NAVER_CLOUD_ACCESS_KEY가 설정되지 않았습니다."
    assert client_secret is not None, "NAVER_CLOUD_SECRET_KEY가 설정되지 않았습니다."
    
    # STT 인스턴스 생성
    stt = NaverSTT(client_id, client_secret)
    
    # 테스트할 오디오 파일 목록
    audio_files = [
        "test_1.wav",
        "test_2.wav",
        "test_3.wav",
        "test_4.wav",
        "test_5.wav"
    ]
    
    # 각 파일 테스트
    for audio_file in audio_files:
        file_path = os.path.join("tests", "audio", audio_file)
        print(f"\n테스트 파일: {audio_file}")
        
        # 파일 읽기
        with open(file_path, "rb") as f:
            audio_data = f.read()
        
        # 음성 인식 수행
        result = stt.recognize(audio_data, lang="Kor")
        
        # 결과 출력
        if result.get("error"):
            print(f"오류 발생: {result['error']}")
        else:
            print(f"인식 결과: {result['text']}")
            print(f"신뢰도: {result['confidence']}")
        
        # 기본 검증
        assert result is not None, f"{audio_file} 처리 중 오류 발생"
        if not result.get("error"):
            assert isinstance(result["text"], str), "인식 결과가 문자열이 아님"
            assert len(result["text"]) > 0, "인식 결과가 비어있음" 