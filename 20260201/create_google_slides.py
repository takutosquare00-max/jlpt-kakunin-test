#!/usr/bin/env python3
"""
マークダウンファイルをGoogle Slidesに変換するスクリプト
"""

import re
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle

# Google Slides APIのスコープ
SCOPES = ['https://www.googleapis.com/auth/presentations']

# 認証情報ファイルのパス
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'


def authenticate():
    """Google APIの認証を行う"""
    creds = None
    
    # 既存のトークンを読み込む
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # トークンが無効な場合、再認証
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"エラー: {CREDENTIALS_FILE} が見つかりません。")
                print("Google Cloud Consoleから認証情報をダウンロードしてください。")
                print("https://console.cloud.google.com/apis/credentials")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # トークンを保存
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds


def parse_markdown_slides(markdown_file):
    """マークダウンファイルを解析してスライドのリストを返す"""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Marp形式のスライドを分割（---で区切られている）
    slides = []
    slide_sections = re.split(r'^---\s*$', content, flags=re.MULTILINE)
    
    for section in slide_sections:
        section = section.strip()
        if not section:
            continue
        
        # フロントマター（YAML）を除去
        if section.startswith('marp:'):
            lines = section.split('\n')
            # 最初の---までの行をスキップ
            skip = True
            filtered_lines = []
            for line in lines:
                if skip and line.strip() == '---':
                    skip = False
                    continue
                if not skip:
                    filtered_lines.append(line)
            section = '\n'.join(filtered_lines)
        
        if section:
            slides.append(section)
    
    return slides


def markdown_to_text_elements(markdown_text):
    """マークダウンテキストをGoogle Slidesのテキスト要素に変換"""
    elements = []
    lines = markdown_text.split('\n')
    
    y_position = 50  # 開始位置（ポイント）
    line_height = 30  # 行の高さ
    
    for line in lines:
        line = line.strip()
        if not line:
            y_position += line_height
            continue
        
        # 見出しレベルの判定
        if line.startswith('# '):
            # H1
            text = line[2:].strip()
            font_size = 36
            bold = True
        elif line.startswith('## '):
            # H2
            text = line[3:].strip()
            font_size = 28
            bold = True
        elif line.startswith('### '):
            # H3
            text = line[4:].strip()
            font_size = 24
            bold = True
        elif line.startswith('**') and line.endswith('**'):
            # 太字
            text = line[2:-2].strip()
            font_size = 18
            bold = True
        elif line.startswith('- '):
            # リスト項目
            text = line[2:].strip()
            font_size = 16
            bold = False
        elif re.match(r'^\d+\.', line):
            # 番号付きリスト
            text = line.strip()
            font_size = 16
            bold = False
        else:
            # 通常のテキスト
            text = line
            font_size = 16
            bold = False
        
        # マークダウンの装飾を除去
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # 太字
        text = re.sub(r'\*(.*?)\*', r'\1', text)  # 斜体
        
        if text:
            elements.append({
                'text': text,
                'fontSize': {'magnitude': font_size, 'unit': 'PT'},
                'bold': bold,
                'y': y_position
            })
            y_position += line_height + 10
    
    return elements


def create_slide_with_text(presentation_id, slide_index, title, content, service):
    """テキストを含むスライドを作成"""
    try:
        # 新しいスライドを作成
        requests = [{
            'createSlide': {
                'insertionIndex': slide_index,
                'slideLayoutReference': {
                    'predefinedLayout': 'BLANK'
                }
            }
        }]
        
        response = service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': requests}
        ).execute()
        
        slide_id = response['replies'][0]['createSlide']['objectId']
        
        # テキスト要素を作成
        text_elements = markdown_to_text_elements(content)
        
        if not text_elements:
            return slide_id
        
        # テキストボックスを作成
        requests = []
        y_pos = 50
        
        for i, elem in enumerate(text_elements):
            # テキストボックスを作成
            create_text_box = {
                'createShape': {
                    'objectId': f'text_box_{slide_index}_{i}',
                    'shapeType': 'TEXT_BOX',
                    'elementProperties': {
                        'pageObjectId': slide_id,
                        'size': {
                            'height': {'magnitude': elem['fontSize']['magnitude'] + 20, 'unit': 'PT'},
                            'width': {'magnitude': 700, 'unit': 'PT'}
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': 50,
                            'translateY': elem['y'],
                            'unit': 'PT'
                        }
                    }
                }
            }
            
            insert_text = {
                'insertText': {
                    'objectId': f'text_box_{slide_index}_{i}',
                    'insertionIndex': 0,
                    'text': elem['text'] + '\n'
                }
            }
            
            update_text_style = {
                'updateTextStyle': {
                    'objectId': f'text_box_{slide_index}_{i}',
                    'style': {
                        'fontSize': elem['fontSize'],
                        'bold': elem['bold']
                    },
                    'fields': 'fontSize,bold'
                }
            }
            
            requests.extend([create_text_box, insert_text, update_text_style])
        
        if requests:
            service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
        
        return slide_id
        
    except HttpError as error:
        print(f'エラーが発生しました: {error}')
        return None


def create_presentation(title, service):
    """新しいプレゼンテーションを作成"""
    try:
        presentation = service.presentations().create(
            body={'title': title}
        ).execute()
        
        presentation_id = presentation.get('presentationId')
        print(f'プレゼンテーションが作成されました: {presentation_id}')
        print(f'URL: https://docs.google.com/presentation/d/{presentation_id}/edit')
        
        return presentation_id
    except HttpError as error:
        print(f'エラーが発生しました: {error}')
        return None


def main():
    """メイン関数"""
    markdown_file = '/Users/hayashi./DataxWorkspace/Developer/school/20260131/n5-test-20questions.md'
    
    # 認証
    print('Google APIに認証中...')
    creds = authenticate()
    if not creds:
        return
    
    # Google Slides APIサービスを構築
    service = build('slides', 'v1', credentials=creds)
    
    # マークダウンファイルを解析
    print('マークダウンファイルを解析中...')
    slides = parse_markdown_slides(markdown_file)
    print(f'{len(slides)}個のスライドが見つかりました')
    
    # プレゼンテーションを作成
    print('プレゼンテーションを作成中...')
    presentation_id = create_presentation('JLPT N5 練習テスト（20問）', service)
    if not presentation_id:
        return
    
    # 各スライドを作成
    print('スライドを作成中...')
    for i, slide_content in enumerate(slides):
        print(f'スライド {i+1}/{len(slides)} を作成中...')
        
        # タイトルを抽出（最初の行から）
        lines = slide_content.split('\n')
        title = lines[0].replace('#', '').strip() if lines else f'スライド {i+1}'
        
        create_slide_with_text(presentation_id, i+1, title, slide_content, service)
    
    print('完了しました！')
    print(f'プレゼンテーションURL: https://docs.google.com/presentation/d/{presentation_id}/edit')


if __name__ == '__main__':
    main()
