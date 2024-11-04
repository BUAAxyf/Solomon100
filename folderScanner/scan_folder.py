import os

def scan_folder(file_folder: str) -> list[str]:
    """
    读取file_folder目录下的所有文件名, 返回所有文件名构成的列表
    """
    try:
        # 获取文件夹中的所有文件名
        file_names = os.listdir(file_folder)
        # 过滤出文件名，排除目录
        files = [f for f in file_names if os.path.isfile(os.path.join(file_folder, f))]
        return files
    except FileNotFoundError:
        print(f"Error: The directory '{file_folder}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
