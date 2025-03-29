import os
import asyncio
from edge_tts import Communicate
from pydub import AudioSegment

async def generate_test_audio(text: str, output_file: str):
    communicate = Communicate(text, "ko-KR-SunHiNeural")
    temp_mp3 = output_file.replace(".wav", "_temp.mp3")
    
    try:
        await communicate.save(temp_mp3)
        audio = AudioSegment.from_mp3(temp_mp3)
        
        # Convert to mono and resample to 16kHz
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)
        
        # Export with specific parameters for Vosk
        audio.export(
            output_file,
            format="wav",
            parameters=[
                "-acodec", "pcm_s16le",  # 16-bit PCM
                "-ar", "16000",          # 16kHz sample rate
                "-ac", "1"               # mono
            ]
        )
    finally:
        if os.path.exists(temp_mp3):
            os.remove(temp_mp3)

async def main():
    test_sentences = [
        "안녕하세요, 반갑습니다.",
        "오늘은 날씨가 좋네요.",
        "음성 인식 테스트를 진행합니다.",
        "이 음성은 테스트용입니다.",
        "음성 인식 서버가 잘 작동하는지 확인 해보겠 습니 다."
    ]

    os.makedirs("tests/audio", exist_ok=True)

    for i, sentence in enumerate(test_sentences, 1):
        output_file = f"tests/audio/test_{i}.wav"
        await generate_test_audio(sentence, output_file)
        print(f"생성된 파일: {output_file}")

if __name__ == "__main__":
    asyncio.run(main()) 