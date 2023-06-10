import os
import shutil

# 从项目根目录获取所有app目录
app_dirs = [d for d in os.listdir() if os.path.isdir(d) and not d.startswith('.')]

for app_dir in app_dirs:
    migration_dir = os.path.join(app_dir, 'migrations')
    
    # 检查migrations目录是否存在
    if os.path.exists(migration_dir):
        # 遍历migrations目录中的所有文件和目录
        for item in os.listdir(migration_dir):
            item_path = os.path.join(migration_dir, item)
            
            # 如果item是文件且不是__init__.py，删除它
            if os.path.isfile(item_path) and item != "__init__.py":
                os.remove(item_path)
                print(f"Deleted: {item_path}")
            
            # 如果item是__pycache__目录，删除整个目录
            if os.path.isdir(item_path) and item == "__pycache__":
                shutil.rmtree(item_path)
                print(f"Deleted directory: {item_path}")
    else:
        print(f"No migrations directory found in {app_dir}.")

os.remove("db.sqlite3")
print(f"Deleted: db.sqlite3")

