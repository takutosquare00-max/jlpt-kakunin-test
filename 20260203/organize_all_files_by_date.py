#!/usr/bin/env python3
"""
Business/schoolディレクトリ内のすべてのファイル（サブディレクトリ含む）を作成日別にフォルダに分けるスクリプト
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
    """ファイルを作成日別にフォルダに分ける（再帰的に処理）"""
    base_path = Path(base_dir)
    
    # 既存の日付フォルダをスキップするためのセット
    existing_date_folders = set()
    for item in base_path.iterdir():
        if item.is_dir() and item.name.startswith('202'):
            existing_date_folders.add(item.name)
    
    # すべてのファイルを再帰的に収集
    files_to_move = []
    
    # 再帰的にすべてのファイルを探索
    for root, dirs, files in os.walk(base_path):
        root_path = Path(root)
        
        # 日付フォルダ内も処理するが、処理中の日付フォルダはスキップ（無限ループを防ぐ）
        # ただし、既に正しい日付フォルダにいるファイルは後で確認する
        
        for file_name in files:
            # .DS_Storeはスキップ
            if file_name == '.DS_Store':
                continue
            
            file_path = root_path / file_name
            
            # ファイルの作成日を取得
            creation_date = get_file_creation_date(file_path)
            date_folder = creation_date.strftime('%Y%m%d')
            
            # 日付フォルダのパス
            date_folder_path = base_path / date_folder
            
            # ファイルを移動するリストに追加
            files_to_move.append((file_path, date_folder_path, date_folder, root_path))
    
    # ファイルを移動
    moved_count = 0
    skipped_count = 0
    
    for file_path, date_folder_path, date_folder, original_dir in files_to_move:
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
                skipped_count += 1
                continue
            
            # ファイルを移動
            shutil.move(str(file_path), str(dest_path))
            relative_path = file_path.relative_to(base_path)
            print(f"Moved {relative_path} -> {date_folder}/")
            moved_count += 1
            
            # 元のディレクトリが空になったら削除（日付フォルダ以外）
            if original_dir != base_path and not original_dir.name.startswith('202'):
                try:
                    # ディレクトリ内にファイルが残っているか確認
                    remaining_files = [f for f in original_dir.iterdir() 
                                      if f.is_file() and f.name != '.DS_Store']
                    if not remaining_files:
                        # サブディレクトリも確認
                        remaining_dirs = [d for d in original_dir.iterdir() if d.is_dir()]
                        if not remaining_dirs:
                            original_dir.rmdir()
                            print(f"Removed empty directory: {original_dir.relative_to(base_path)}")
                except Exception as e:
                    print(f"Could not remove directory {original_dir}: {e}")
                    
        except Exception as e:
            print(f"Error moving {file_path.name}: {e}")
    
    print(f"\nTotal files moved: {moved_count}")
    print(f"Total files skipped: {skipped_count}")

if __name__ == '__main__':
    base_directory = '/Users/hayashi./DataxWorkspace/Developer/school'
    print("Organizing files by creation date...")
    print("=" * 50)
    organize_files_by_date(base_directory)
    print("=" * 50)
    print("Done!")
