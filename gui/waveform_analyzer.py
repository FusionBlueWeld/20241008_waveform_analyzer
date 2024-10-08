import customtkinter as ctk
from tkinter import filedialog, Listbox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.file_processor import process_folder
from utils.waveform_generator import run_waveform_generation
from utils.waveform_processor import run_pre_process
from utils.models import run_models
import os
import glob
import time
import numpy as np
from datetime import datetime
from mpl_toolkits.mplot3d import Axes3D

class WaveformAnalyzer(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.is_waveform_generated = False
        self.condition_plot = []

        self.is_paused = False
        self.is_stopped = False

        self.create_data_frame()
        self.create_operation_frame()
        self.create_graph_frame()
        self.create_log_frame()
        self.create_output_frame()

    def create_data_frame(self):
        data_frame = ctk.CTkFrame(self)
        data_frame.pack(pady=10, padx=10, fill="x")

        self.folder_path = ctk.StringVar()
        self.data_count = ctk.StringVar()

        self.select_button = ctk.CTkButton(data_frame, text="フォルダ選択", command=self.select_folder, fg_color="blue")
        self.select_button.grid(row=0, column=0, padx=5, pady=5)

        self.path_entry = ctk.CTkEntry(data_frame, textvariable=self.folder_path, width=600, state="readonly")
        self.path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.generate_button = ctk.CTkButton(data_frame, text="波形生成", command=self.toggle_generate, fg_color="blue")
        self.generate_button.grid(row=1, column=0, padx=5, pady=5)
        
        self.data_count = ctk.StringVar(value="5")
        self.count_entry = ctk.CTkEntry(data_frame, textvariable=self.data_count, width=100)
        self.count_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def create_operation_frame(self):
        operation_frame = ctk.CTkFrame(self)
        operation_frame.pack(pady=10, padx=10, fill="x")

        self.mapping_button = ctk.CTkButton(operation_frame, text="マッピング", command=self.mapping_button_clicked)
        self.detail_toggle = ctk.CTkSwitch(operation_frame, text="詳細", onvalue="on", offvalue="off")
        self.pause_button = ctk.CTkButton(operation_frame, text="一時停止", command=self.toggle_pause)
        self.stop_button = ctk.CTkButton(operation_frame, text="中止", command=self.stop_processing)

        self.stop_button.pack(side="right", padx=5)
        self.pause_button.pack(side="right", padx=5)
        self.detail_toggle.pack(side="right", padx=5)
        self.mapping_button.pack(side="right", padx=5)

    def create_graph_frame(self):
        graph_frame = ctk.CTkFrame(self)
        graph_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # 波形グラフの作成
        self.wave_fig, self.wave_ax = plt.subplots(figsize=(1, 1))
        self.wave_canvas = FigureCanvasTkAgg(self.wave_fig, master=graph_frame)
        self.wave_canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

        # 波形グラフにのグラフオプションを追加
        self.wave_options()

        # 状態マップグラフの作成
        self.map_fig = plt.figure(figsize=(1, 1))
        self.map_ax = self.map_fig.add_subplot(111, projection='3d')
        self.map_canvas = FigureCanvasTkAgg(self.map_fig, master=graph_frame)
        self.map_canvas.get_tk_widget().pack(side="right", fill="both", expand=True)

        # 状態マップグラフのオプションを設定
        self.map_options()

    def wave_options(self):
        # 波形グラフのオプションを追加
        self.wave_ax.grid(True)
        self.wave_ax.set_xlim(-20, 40)

    def map_options(self):
        pass

    def create_log_frame(self):
        log_frame = ctk.CTkFrame(self)
        log_frame.pack(pady=10, padx=10, fill="x", ipady=30)

        self.log_listbox = Listbox(log_frame, height=5)
        self.log_listbox.pack(fill="both", expand=True)

    def create_output_frame(self):
        output_frame = ctk.CTkFrame(self)
        output_frame.pack(pady=10, padx=10, fill="x")

        button_frame = ctk.CTkFrame(output_frame)
        button_frame.pack(side="right")

        self.exit_button = ctk.CTkButton(button_frame, text="終了", fg_color="red", command=self.exit_app)
        self.exit_button.pack(side="right")

        self.csv_button = ctk.CTkButton(button_frame, text="CSV出力")
        self.csv_button.pack(side="right", padx=(0, 5))

    def select_folder(self):
        folder = filedialog.askdirectory(initialdir=os.path.join(os.getcwd(), "data\\user"))
        if folder:
            self.folder_path.set(folder)
            process_folder(folder)

    def toggle_generate(self):
        if self.generate_button.cget("fg_color") == "blue":
            self.generate_button.configure(fg_color="green")
            self.select_button.configure(state="disabled", fg_color="gray")
            self.path_entry.configure(state="disabled")
        else:
            self.generate_button.configure(fg_color="blue")
            self.select_button.configure(state="normal", fg_color="blue")
            self.path_entry.configure(state="readonly")

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_button.configure(text="再開")
        else:
            self.pause_button.configure(text="一時停止")

    def stop_processing(self):
        self.is_stopped = True

    def mapping_button_clicked(self):
        timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        folder_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.is_paused = False
        self.is_stopped = False
        self.pause_button.configure(text="一時停止")

        if self.generate_button.cget("fg_color") == "green":
            try:
                num_iterations = int(self.data_count.get())

                data_folder_path = f'data\generated\{folder_timestamp}'
                run_waveform_generation(num_iterations, data_folder_path, plot_waveforms=False)

                self.log_listbox.insert(
                    "end", f"{timestamp} 状態1. 波形が {num_iterations} 生成されました")

            except ValueError:
                self.log_listbox.insert(
                    "end", f"{timestamp} 状態1. エラー: 波形生成数が無効です")
                return
        else:
            data_folder_path = self.folder_path.get()

            if not data_folder_path:
                self.log_listbox.insert(
                    "end", f"{timestamp} 状態2. エラー: フォルダが選択されていません")
                return

            csv_files = glob.glob(f'{data_folder_path}/*.csv')
            if not csv_files:
                self.log_listbox.insert(
                    "end", f"{timestamp} 状態2. エラー: フォルダ内にCSVファイルが見つかりません")
                return

            self.log_listbox.insert(
                "end", f"{timestamp} 状態2. フォルダパス: {data_folder_path} が抽出されました")

        waveform_files = glob.glob(f'{data_folder_path}\\*.csv')

        segment_length = 128
        self.condition_plot = []
        for index, file_path in enumerate(waveform_files):
            if self.is_stopped:
                self.log_listbox.insert("end", f"{timestamp} 状態: 処理が中止されました")
                break

            while self.is_paused:
                self.update()  # GUIを更新して応答性を維持
                time.sleep(0.1)
                if self.is_stopped:
                    self.log_listbox.insert("end", f"{timestamp} 状態: 処理が中止されました")
                    return

            segments = run_pre_process(file_path, segment_length)
            feature_vectors = run_models(segments)

            # 3次元テンソル (バッチ数, バッチあたりのデータ数, 系列数) を2次元テンソル (全データ数, 系列数) に変換
            combined_segments = segments.reshape(-1, segments.shape[-1])
            # 0パディングされた部分を除去
            combined_segments = combined_segments[np.any(combined_segments != 0, axis=1)]

            if self.detail_toggle.get() == "on":
                for i in range(segments.shape[0]):

                    if self.is_stopped:
                        self.log_listbox.insert("end", f"{timestamp} 状態: 処理が中止されました")
                        return

                    while self.is_paused:
                        self.update()  # GUIを更新して応答性を維持
                        time.sleep(0.1)
                        if self.is_stopped:
                            self.log_listbox.insert("end", f"{timestamp} 状態: 処理が中止されました")
                            return

                    # 波形グラフの更新
                    self.wave_ax.clear()
                    # 個別セグメントの0パディングされた部分を除去
                    zero_canceled_seg = segments[i][np.any(segments[i] != 0, axis=1)]

                    if combined_segments.shape[1] >= 2:
                        self.wave_ax.plot(combined_segments[:, 0], combined_segments[:, 1], color='#FF3300')
                        self.wave_ax.plot(zero_canceled_seg[:, 0], zero_canceled_seg[:, 1], color='#0000FF')
                    else:
                        self.log_listbox.insert(
                            "end", f"{timestamp} 状態3. エラー: データに2列以上の系列がありません")

                    self.wave_options()
                    self.wave_canvas.draw()

                    # 状態マップの更新
                    self.condition_plot.append(feature_vectors[i])
                    self.map_ax.clear()

                    condition_plot_array = np.array(self.condition_plot)
                    if len(condition_plot_array) > 0:
                        self.map_ax.scatter(condition_plot_array[:, 0], condition_plot_array[:, 1], condition_plot_array[:, 2], color='#0000FF', alpha=0.5)

                    self.map_options()
                    self.map_canvas.draw()

                    self.wave_canvas.get_tk_widget().update()  # 明示的にGUIを更新
                    time.sleep(0.1)  # 更新速度を調整

            else:
                # 波形グラフの更新
                self.wave_ax.clear()

                if combined_segments.shape[1] >= 2:
                    self.wave_ax.plot(combined_segments[:, 0], combined_segments[:, 1], color='#FF3300')
                else:
                    self.log_listbox.insert(
                        "end", f"{timestamp} 状態3. エラー: データに2列以上の系列がありません")

                self.wave_options()
                self.wave_canvas.draw()

                # 状態マップの更新
                self.condition_plot.extend(feature_vectors)
                self.map_ax.clear()

                condition_plot_array = np.array(self.condition_plot)
                if len(condition_plot_array) > 0:
                    self.map_ax.scatter(condition_plot_array[:, 0], condition_plot_array[:, 1], condition_plot_array[:, 2], color='#0000FF', alpha=0.9)

                self.map_options()
                self.map_canvas.draw()

                self.wave_canvas.get_tk_widget().update()  # 明示的にGUIを更新

            self.log_listbox.insert(
                "end", f"{timestamp} 状態 Processing. ファイル# {index} 完了")

            self.update()  # GUIを更新

    def exit_app(self):
        self.master.quit()

