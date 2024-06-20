import sys
import screen_brightness_control as sbc

def set_screen_brightness(brightness):
    try:
        # 밝기 값이 숫자인지 확인하고, 조절을 시도합니다.
        brightness = int(brightness)
        if 0 <= brightness <= 100:  # 밝기 값은 0에서 100 사이여야 합니다.
            # 모든 모니터의 밝기를 설정
            monitors = sbc.list_monitors()  # 모든 모니터의 식별자 목록을 가져옵니다.
            for monitor in monitors:
                sbc.set_brightness(brightness, display=monitor)
            print(f"모든 화면의 밝기가 {brightness}%로 설정되었습니다.")
        else:
            print("밝기는 0에서 100 사이의 값이어야 합니다.")
    except ValueError:
        print("오류: 밝기는 숫자여야 합니다.")
    except Exception as e:
        print(f"밝기 설정 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        set_screen_brightness(sys.argv[1])
    else:
        print("밝기 값을 숫자로 제공해주세요. 예: 50")
