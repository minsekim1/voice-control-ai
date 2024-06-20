import sys
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

def set_system_volume(volume):
    try:
        # 음량 값이 숫자인지 확인하고 조절을 시도합니다.
        volume = int(volume)
        if 0 <= volume <= 100:  # 음량 값은 0에서 100 사이여야 합니다.
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume_control = cast(interface, POINTER(IAudioEndpointVolume))

            # 음량을 실제 퍼센트로 설정합니다 (-65.25 ~ 0.0 dB).
            volume_control.SetMasterVolumeLevelScalar(volume / 100.0, None)
            print(f"시스템 음량이 {volume}%로 설정되었습니다.")
        else:
            print("음량은 0에서 100 사이의 값이어야 합니다.")
    except ValueError:
        print("오류: 음량은 숫자여야 합니다.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        set_system_volume(sys.argv[1])
    else:
        print("음량 값을 숫자로 제공해주세요. 예: 50")


# TODO
# 음량 native 로 처리할 수 있게하기 -> 예: 백 -> 100으로 설정