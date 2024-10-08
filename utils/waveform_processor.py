# waveform_processor.py

import os
import shutil
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

def pre_process(file_path):
    # CSVファイルの読み込み
    df = pd.read_csv(file_path)

    # 欠損値の除去（欠損値が含まれる行を削除）
    df.dropna(inplace=True)

    # ノイズ除去（サバゴルフィルタを使用して高周波ノイズを除去）
    df['Amplitude'] = savgol_filter(df['Amplitude'], window_length=11, polyorder=2)

    # データの正規化（Amplitude列の標準化）
    scaler = StandardScaler()
    df['Amplitude'] = scaler.fit_transform(df[['Amplitude']])

    # 整列処理（Phaseに基づいてデータをソート）
    df.sort_values(by='Phase', inplace=True)

    return df

def segment_waveform(df, segment_length):
    # X軸は2列目（Phase）、Y軸は3列目以降の全列
    x_axis = df.columns[1]
    y_axes = df.columns[2:]

    # データ数とセグメント数を計算
    total_steps = len(df)
    num_segments = int(np.ceil(total_steps / segment_length))

    # 3次元テンソルを初期化 (セグメント数 × セグメント長 × Y軸の列数)
    segments = np.zeros((num_segments, segment_length, len(y_axes) + 1))

    for i in range(num_segments):
        start_idx = i * segment_length
        end_idx = min(start_idx + segment_length, total_steps)

        # X軸のデータを割り当て
        segments[i, :len(df[x_axis].iloc[start_idx:end_idx]), 0] = df[x_axis].iloc[start_idx:end_idx].values

        # Y軸のデータを割り当て
        for j, y_axis in enumerate(y_axes):
            segments[i, :len(df[y_axis].iloc[start_idx:end_idx]), j + 1] = df[y_axis].iloc[start_idx:end_idx].values

    return segments

def run_pre_process(file_path, segment_length):
    df = pre_process(file_path)
    segments = segment_waveform(df, segment_length)

    return segments

