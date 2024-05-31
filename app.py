import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Voice Status")

    # 화면 중앙에 위치
    root.eval('tk::PlaceWindow . center')

    label = tk.Label(root, text="on Voice", font=('Helvetica', 18, 'bold'))
    label.pack(pady=20)  # 패딩으로 위젯 주변에 여백 추가

    root.mainloop()

if __name__ == "__main__":
    main()
