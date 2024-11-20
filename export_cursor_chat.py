import sqlite3
import json
import os
from pathlib import Path

def export_cursor_chat():
    # 获取用户主目录
    home = str(Path.home())
    
    possible_paths = [
        os.path.join(home, 'Library/Application Support/Cursor/User/workspaceStorage'),
    ]
    
    # 找到第一个存在的路径
    workspace_path = None
    for path in possible_paths:
        if os.path.exists(path):
            workspace_path = path
            break
    
    if not workspace_path:
        print("找不到Cursor工作区目录")
        return
        
    chats = []
    
    try:
        # 遍历所有工作区文件夹
        for workspace in os.listdir(workspace_path):
            db_path = os.path.join(workspace_path, workspace, 'state.vscdb')
            
            if not os.path.exists(db_path):
                continue
            
            # 连接数据库
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # 获取所有需要的数据
            cursor.execute("""
                SELECT [key], value 
                FROM ItemTable 
                WHERE [key] IN (
                    'workbench.panel.aichat.view.aichat.chatdata',
                    'composer.composerData'
                )
            """)
            
            for row in cursor.fetchall():
                key, value = row
                try:
                    data = json.loads(value)
                    chats.append({
                        'workspace': workspace,
                        'type': key,
                        'data': data
                    })
                except Exception as e:
                    continue
            
            conn.close()
        
        if not chats:
            print("没有找到任何聊天记录")
            return
            
        # 导出为JSON文件
        output_file = 'cursor_chats.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chats, f, ensure_ascii=False, indent=2)
            
        print(f"聊天记录已成功导出到: {output_file}")
        print(f"共导出 {len(chats)} 条记录")
        
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    export_cursor_chat() 