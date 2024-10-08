# waveform_generator.py

import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
import csv

def fourier_square_wave(t, num_terms1, num_terms2):
    wave = np.zeros_like(t)
    for i, ti in enumerate(t):
        if -np.pi/2 <= ti < np.pi/2:
            for n in range(1, num_terms1*2, 2):
                wave[i] += (4 / (n * np.pi)) * np.sin(n * ti)
        elif np.pi/2 <= ti <= 3*np.pi/2:
            for n in range(1, num_terms2*2, 2):
                wave[i] += (4 / (n * np.pi)) * np.sin(n * ti)
    return wave

def generate_waveform(num_terms1, num_terms2, noise_amplitude, phase_offset, gaussian_peak, gaussian_width, sin_amplitude, shift_value, index, data_folder_path, plot_waveform=False):
    # パラメータ設定
    # num_points = 1000
    offset = 1.5
    extended_num_points = 10000  # 拡張された範囲のためにポイント数を増やす

    # 拡張された範囲の時間配列を生成
    t_extended = np.linspace(-10*np.pi, 15*np.pi, extended_num_points)

    # オリジナルの範囲のインデックスを計算
    original_start = np.argmin(np.abs(t_extended - (-np.pi/2 + phase_offset)))
    original_end = np.argmin(np.abs(t_extended - (3*np.pi/2 + phase_offset)))

    # 拡張された範囲で波形を初期化（すべて0）
    extended_wave = np.zeros(extended_num_points)

    # オリジナルの波形を生成
    t_original = t_extended[original_start:original_end+1]
    square_wave = fourier_square_wave(t_original, num_terms1, num_terms2) + offset

    # 位相3π/4のインデックスを特定
    phase_target_index = np.argmin(np.abs(t_original - 3*np.pi/4))

    # ガウス関数を生成し、位相3π/4を中心に加算
    gaussian = gaussian_peak * np.exp(-((t_original - t_original[phase_target_index])**2) / (2 * gaussian_width**2))
    gaussian_wave = square_wave * gaussian

    # πから3π/2の範囲でサイン波を乗算
    sin_wave = np.ones_like(t_original)
    pi_index = np.argmin(np.abs(t_original - np.pi))
    three_pi_half_index = np.argmin(np.abs(t_original - 3*np.pi/2))

    sin_wave[pi_index:three_pi_half_index+1] = sin_amplitude * np.sin(t_original[pi_index:three_pi_half_index+1] - np.pi)

    # 振幅調整後のサイン波を1〜6の範囲に変換
    sin_wave = (sin_wave - 1) / 4 + 1
    sin_wave = gaussian_wave * sin_wave

    # 配置開始位置をπだけずらす
    shift = int((shift_value / (t_extended[1] - t_extended[0])))

    # オリジナルの波形を拡張された範囲に配置
    extended_wave[original_start + shift:original_end + 1 + shift] = sin_wave

    # ノイズを生成し、波形に加える
    noise = np.random.normal(0, noise_amplitude, extended_num_points)
    noisy_wave = extended_wave + noise

    if plot_waveform:
        # プロット
        plt.figure(figsize=(12, 6))
        plt.plot(t_extended, noisy_wave)
        plt.title(f'Approximation of Square Wave using Fourier Series\n(Terms1: {num_terms1}, Terms2: {num_terms2}, Noise Amplitude: {noise_amplitude:.2f}, Phase Offset: {phase_offset:.2f})')
        plt.xlabel('Phase (radians)')
        plt.ylabel('Amplitude')
        plt.grid(True)
        plt.axhline(y=offset, color='r', linestyle='--', label='Offset')
        plt.axvline(x=-np.pi/2 + phase_offset, color='g', linestyle='--')
        plt.axvline(x=np.pi/2 + phase_offset, color='g', linestyle='--')
        plt.axvline(x=3*np.pi/2 + phase_offset, color='g', linestyle='--')
        plt.xticks([-10*np.pi, -5*np.pi, 0, 5*np.pi, 10*np.pi, 15*np.pi], 
                   [r'$-10\pi$', r'$-5\pi$', '0', r'$5\pi$', r'$10\pi$', r'$15\pi$'])
        plt.ylim(offset-1.7, offset+30.7)
        plt.legend()
        plt.savefig(f'{data_folder_path}/punch_shot{index}.png')
        plt.close()

    # CSVファイルに出力
    with open(f'{data_folder_path}/punch_shot{index}.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Index', 'Phase', 'Amplitude'])
        for i, (phase, amplitude) in enumerate(zip(t_extended, noisy_wave)):
            csvwriter.writerow([i, phase, amplitude])

def run_waveform_generation(num_iterations, data_folder_path, plot_waveforms=False):
    # 出力フォルダの準備
    if os.path.exists(data_folder_path):
        shutil.rmtree(data_folder_path)
    os.makedirs(data_folder_path)

    # 繰り返し処理
    for i in range(num_iterations):
        # ランダムパラメータの生成
        num_terms1 = np.random.randint(5, 16)  # 5から15の範囲
        num_terms2 = np.random.randint(10, 31)  # 10から30の範囲
        noise_amplitude = np.random.uniform(0.05, 0.15)
        phase_offset = np.random.uniform(0, 0)  # オフセット0
        gaussian_peak = np.random.uniform(5, 10)
        gaussian_width = np.random.uniform(0.5, 1.5)
        sin_amplitude = np.random.uniform(15, 30)
        shift_value = np.random.uniform(-np.pi, np.pi)

        # 波形生成フローの実行
        generate_waveform(num_terms1, num_terms2, noise_amplitude, phase_offset, gaussian_peak, gaussian_width, sin_amplitude, shift_value, i+1, data_folder_path, plot_waveform=plot_waveforms)
