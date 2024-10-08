import os

def process_folder(folder_path):
    """
    選択されたフォルダに対する処理を行う関数。
    この例では、フォルダ内のファイル数を数えて表示します。
    """
    file_count = sum([len(files) for r, d, files in os.walk(folder_path)])
    print(f"選択されたフォルダ: {folder_path}")
    print(f"フォルダ内のファイル数: {file_count}")

    # ここに必要な処理を追加してください
    # 例: ファイルの分析、データの抽出など