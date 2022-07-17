from pathlib import Path
import sys


IMAGES = []
VIDEO = []
DOCUMENTS = []
AUDIO = []
MY_OTHER = []
ARCHIVES = []

IMAGES_FILE = []
VIDEO_FILE = []
DOCUMENTS_FILE = []
AUDIO_FILE = []
MY_OTHER_FILE = []
# списки для виводу назв файлів
REGISTER_EXTENSIONS = {
    'JPEG': IMAGES,
    'PNG': IMAGES,
    'JPG': IMAGES,
    'SVG': IMAGES,
    'AVI': VIDEO,
    'MP4': VIDEO,
    'MOV': VIDEO,
    'MKV': VIDEO,
    'DOC': DOCUMENTS,
    'DOCX': DOCUMENTS,
    'TXT': DOCUMENTS,
    'PDF': DOCUMENTS,
    'XLSX': DOCUMENTS,
    'PPTX': DOCUMENTS,
    'MP3': AUDIO,
    'OGG': AUDIO,
    'WAV': AUDIO,
    'AMR': AUDIO,
    'ZIP': ARCHIVES,
    'GZ': ARCHIVES,
    'TAR': ARCHIVES
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()


def get_extension(filename: str) -> str:
    # перетворюємо розширення файлу на назву папки .jpg -> JPG
    return Path(filename).suffix[1:].upper()


def scan(folder: Path) -> None:
    for item in folder.iterdir():
        # Якщо це папка то додаємо її зі списку FOLDERS і переходимо до наступного елемента папки
        if item.is_dir():
            # перевіряємо, щоб папка не була тією, в яку ми складаємо вже файли.
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'my_other'):
                FOLDERS.append(item)
                # скануємо цю вкладену папку - рекурсія
                scan(item)
            # перейти до наступного елемента в сканованій папці
            continue

        # Робота з файлом
        ext = get_extension(item.name)  # взяти розширення

        if ext in ('JPEG', 'PNG', 'JPG', 'SVG'):
            IMAGES_FILE.append(item.name)
        if ext in ('AVI', 'MP4', 'MOV', 'MKV'):
            VIDEO_FILE.append(item.name)
        if ext in ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'):
            DOCUMENTS_FILE.append(item.name)
        if ext in ('MP3', 'OGG', 'WAV', 'AMR'):
            AUDIO_FILE.append(item.name)
        if ext not in ('MP3', 'OGG', 'WAV', 'AMR', 'JPEG', 'PNG', 'JPG', 'SVG', 'AVI', 'MP4', 'MOV', 'MKV',
                       'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'):
            MY_OTHER_FILE.append(item.name)

        fullname = folder / item.name  # взяти повний шлях до файлу
        if not ext:  # якщо файл не має розширення додати до невідомих
            MY_OTHER.append(fullname)
        else:
            try:
                # взяти список куди покласти повний шлях до файлу
                container = REGISTER_EXTENSIONS[ext]
                EXTENSIONS.add(ext)
                container.append(fullname)
            except KeyError:
                # Якщо ми не реєстрували розширення у REGISTER_EXTENSIONS, то додати до іншого
                UNKNOWN.add(ext)
                MY_OTHER.append(fullname)


if __name__ == '__main__':

    folder_for_scan = sys.argv[1]
    print(f'Start in folder {folder_for_scan}')

    scan(Path(folder_for_scan))
    print(f'images: {IMAGES_FILE}')
    print(f'video: {VIDEO_FILE}')
    print(f'docs: {DOCUMENTS_FILE}')
    print(f'audio: {AUDIO_FILE}')
    print(f'other file: {MY_OTHER_FILE}')
    print(f'Types of files in folder: {EXTENSIONS}')
    print(f'Unknown files of types: {UNKNOWN}')

    print(FOLDERS[::-1])
# запускаємо:  python3 main.py `назва_папки_для_сортування`
