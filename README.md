# 20241008_waveform_analyzer

```
WaveformAnalyzer
├── [GUI設定]
│   ├── __init__(self, master, **kwargs)       # クラスの初期化、UIコンポーネントの作成
│   ├── create_data_frame(self)                # データ選択用のフレームを作成
│   ├── create_operation_frame(self)           # 操作ボタンのフレームを作成
│   ├── create_graph_frame(self)               # グラフ表示用のフレームを作成
│   ├── wave_options(self)                     # 波形グラフの設定を追加
│   ├── map_options(self)                      # 状態マップグラフの設定を追加
│   ├── create_log_frame(self)                 # ログ表示用のフレームを作成
│   └── create_output_frame(self)              # 出力用ボタンのフレームを作成
│
└── [ボタン操作による処理]
    ├── [フォルダ選択ボタン: select_button]
    │   └── select_folder(self)                # フォルダ選択ダイアログを開く
    │
    ├── [波形生成ボタン: generate_button]
    │   └── toggle_generate(self)              # 波形生成の切り替え
    │
    ├── [一時停止ボタン: pause_button]
    │   └── toggle_pause(self)                 # 処理の一時停止・再開を切り替え
    │
    ├── [中止ボタン: stop_button]
    │   └── stop_processing(self)              # 処理を停止
    │
    ├── [マッピングボタン: mapping_button]
    │   └── mapping_button_clicked(self)       # マッピング処理を実行
    │
    └── [終了ボタン: exit_button]
        └── exit_app(self)                     # アプリケーションを終了

```