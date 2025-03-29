import pytest
import requests
import os
import time
import wave
import json
from typing import Dict, Any

TEST_SENTENCES = [
    "안녕하세요, 반갑습니다.",
    "오늘은 날씨가 좋네요.",
    "음성 인식 테스트를 진행합니다.",
    "이 음성은 테스트용입니다.",
    "음성 인식 서버가 잘 작동하는지 확인해보겠습니다."
]

def validate_recognition_result(result: Dict[str, Any]) -> bool:
    """
    인식 결과의 유효성을 검사합니다.
    """
    if not isinstance(result, dict):
        return False
    
    if "text" not in result or not isinstance(result["text"], str):
        return False
        
    if "confidence" not in result or not isinstance(result["confidence"], (int, float)):
        return False
        
    return True

def get_wav_info(file_path: str) -> Dict[str, Any]:
    """
    WAV 파일의 정보를 반환합니다.
    """
    with wave.open(file_path, "rb") as wf:
        return {
            "channels": wf.getnchannels(),
            "sample_width": wf.getsampwidth(),
            "sample_rate": wf.getframerate(),
            "frames": wf.getnframes(),
            "duration": wf.getnframes() / wf.getframerate()
        }

@pytest.fixture
def audio_files():
    """테스트할 오디오 파일 목록을 반환합니다."""
    audio_dir = "tests/audio"
    if not os.path.exists(audio_dir):
        pytest.skip(f"오디오 디렉토리를 찾을 수 없습니다: {audio_dir}")
    
    files = [f for f in sorted(os.listdir(audio_dir)) if f.endswith(".wav")]
    if not files:
        pytest.skip(f"WAV 파일을 찾을 수 없습니다: {audio_dir}")
    
    return [os.path.join(audio_dir, f) for f in files]

def test_file_recognition(audio_files):
    """
    음성 파일을 서버에 업로드하고 인식 결과를 받아옵니다.
    """
    url = "http://localhost:8000/api/v1/recognition/file"
    
    print("\n음성 인식 테스트 결과:")
    print("=" * 50)
    
    for i, file_path in enumerate(audio_files):
        try:
            # WAV 파일 정보 출력
            wav_info = get_wav_info(file_path)
            print(f"\n[테스트 {i+1}]")
            print(f"원본 텍스트: {TEST_SENTENCES[i]}")
            print(f"파일: {os.path.basename(file_path)}")
            print(f"채널 수: {wav_info['channels']}")
            print(f"샘플 너비: {wav_info['sample_width']} bytes")
            print(f"샘플링 레이트: {wav_info['sample_rate']} Hz")
            print(f"재생 시간: {wav_info['duration']:.2f}초")
            
            # 파일 업로드 및 인식
            with open(file_path, "rb") as f:
                files = {"file": f}
                response = requests.post(url, files=files)
                
            if response.status_code == 200:
                result = response.json()
                print(f"인식 결과: {result['text']}")
                print(f"신뢰도: {result['confidence']:.2f}")
                
                # 기본적인 검증
                assert "text" in result
                assert "confidence" in result
                assert isinstance(result["text"], str)
                assert isinstance(result["confidence"], (int, float))
                
            elif response.status_code == 204:
                print("음성이 감지되지 않았습니다.")
                
            else:
                pytest.fail(f"오류 발생 (코드: {response.status_code})\n{response.text}")
                
        except requests.exceptions.ConnectionError:
            pytest.fail("서버에 연결할 수 없습니다.")
        except Exception as e:
            pytest.fail(f"오류 발생: {str(e)}")
            
        time.sleep(1)  # 서버 부하 방지를 위한 대기
        print("-" * 50)

if __name__ == "__main__":
    pytest.main([__file__]) 