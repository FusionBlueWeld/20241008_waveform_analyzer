# main.py
import customtkinter as ctk
from gui.waveform_analyzer import WaveformAnalyzer

def main():
    app = ctk.CTk()
    app.title("Waveform Analyzer")
    app.geometry("1000x800")

    waveform_analyzer = WaveformAnalyzer(app)
    waveform_analyzer.pack(expand=True, fill="both", padx=10, pady=10)

    app.mainloop()

if __name__ == "__main__":
    main()

