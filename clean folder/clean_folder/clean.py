import sys
from pathlib import Path
import unicodedata
import shutil

CATEGORIES = {
    "audio": [".mp3", ".ogg", ".wav", ".amr"],
    "documents": [".txt", ".docx", ".pdf", ".doc", ".xlsx", ".pptx"],
    "images": [".jpeg", ".png", ".jpg", ".svg"],
    "video": [".avi", ".mp4", ".mov", ".mkv"],
    "archives": [".zip", ".gz"]
}

def normalize(name):
    valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')
    normalized_name = ''.join(c if c in valid_chars else '_' for c in name.lower())
    return normalized_name

def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"

def move_file(file: Path, category: str, root_dir: Path) -> None:
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir(parents=True)
    new_name = normalize(file.stem) + file.suffix.lower()
    target_path = target_dir.joinpath(new_name)
    file.replace(target_path)

    if category == "archives" and file.suffix.lower() == ".zip":
        shutil.unpack_archive(target_path, target_dir)
        file.unlink()  

def remove_empty_folders(path: Path) -> None:
    for folder in path.glob("**/"):
        if folder.is_dir() and not list(folder.iterdir()):
            folder.rmdir()

def sort_folder(path: Path) -> None:
    for element in path.glob("**/*"):
        if element.is_file():
            category = get_categories(element)
            move_file(element, category, path)
    remove_empty_folders(path)

def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"
    if not path.exists():
        return "Folder does not exist"
        
    sort_folder(path)
    
    return "All ok"

if __name__ == '__main__':
    print(main())
