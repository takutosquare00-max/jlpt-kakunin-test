#!/usr/bin/env python3
"""
Business/schoolディレクトリ内のファイルを作成日別にフォルダに分けるスクリプト
"""
import os
import shutil
from pathlib import Path
from datetime import datetime

def get_file_creation_date(file_path):
    """ファイルの作成日を取得（macOS用）"""
    try:
        # macOSではstat.st_birthtimeが作成日
        stat = os.stat(file_path)
        creation_time = stat.st_birthtime
        return datetime.fromtimestamp(creation_time)
    except Exception as e:
        print(f"Error getting creation date for {file_path}: {e}")
        # フォールバック: 最終変更日を使用
        stat = os.stat(file_path)
        modification_time = stat.st_mtime
        return datetime.fromtimestamp(modification_time)

def organize_files_by_date(base_dir):
    """ファイルを作成日別にフォルダに分ける"""
    base_path = Path(base_dir)
    
    # 既存の日付フォルダをスキップするためのセット
    existing_date_folders = set()
    for item in base_path.iterdir():
        if item.is_dir() and item.name.startswith('202'):
            existing_date_folders.add(item.name)
    
    # すべてのファイルを処理
    files_to_move = []
    for item in base_path.iterdir():
        # ディレクトリと.DS_Storeはスキップ
        if item.is_dir() or item.name == '.DS_Store':
            continue
        
        # ファイルの作成日を取得
        creation_date = get_file_creation_date(item)
        date_folder = creation_date.strftime('%Y%m%d')
        
        # 日付フォルダのパス
        date_folder_path = base_path / date_folder
        
        # ファイルを移動するリストに追加
        files_to_move.append((item, date_folder_path, date_folder))
    
    # ファイルを移動
    moved_count = 0
    for file_path, date_folder_path, date_folder in files_to_move:
        try:
            # 日付フォルダが存在しない場合は作成
            if not date_folder_path.exists():
                date_folder_path.mkdir(parents=True, exist_ok=True)
                print(f"Created folder: {date_folder}")
            
            # ファイルを移動
            dest_path = date_folder_path / file_path.name
            
            # 同名ファイルが既に存在する場合はスキップ
            if dest_path.exists():
                print(f"Skipping {file_path.name} (already exists in {date_folder})")
                continue
            
            shutil.move(str(file_path), str(dest_path))
            print(f"Moved {file_path.name} -> {date_folder}/")
            moved_count += 1
        except Exception as e:
            print(f"Error moving {file_path.name}: {e}")
    
    print(f"\nTotal files moved: {moved_count}")

if __name__ == '__main__':
    base_directory = '/Users/hayashi./DataxWorkspace/Developer/school'
    organize_files_by_date(base_directory)
