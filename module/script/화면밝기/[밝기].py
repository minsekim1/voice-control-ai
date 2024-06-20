import sys
import screen_brightness_control as sbc

def set_screen_brightness(brightness):
    try:
        # 밝기 값이 숫자인지 확인하고, 조절을 시도합니다.
        brightness = int(brightness)
        if 0 <= brightness <= 100:  # 밝기 값은 0에서 100 사이여야 합니다.
            sbc.set_brightness(brightness)
            print(f"화면 밝기가 {brightness}%로 설정되었습니다.")
        else:
            print("밝기는 0에서 100 사이의 값이어야 합니다.")
    except ValueError:
        print("오류: 밝기는 숫자여야 합니다.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        set_screen_brightness(sys.argv[1])
    else:
        print("밝기 값을 숫자로 제공해주세요. 예: 50")
