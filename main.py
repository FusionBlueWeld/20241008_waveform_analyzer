# main.py

import customtkinter as ctk
from gui.waveform_analyzer import WaveformAnalyzer

def main():
    # アプリケーションのメインウィンドウを作成
    app = ctk.CTk()
    app.title("Waveform Analyzer")  # ウィンドウタイトルを設定
    app.geometry("1000x800")  # ウィンドウサイズを設定

    # WaveformAnalyzerクラスのインスタンスを作成し、メインウィンドウに配置
    waveform_analyzer = WaveformAnalyzer(app)
    waveform_analyzer.pack(expand=True, fill="both", padx=10, pady=10)  # ウィジェットをウィンドウに配置

    # アプリケーションのメインループを開始
    app.mainloop()

# スクリプトが直接実行された場合にmain関数を呼び出す
if __name__ == "__main__":
    main()

