# fileManager/views/helper.py

import os
import shutil
from django.conf import settings

class FileManager:
    """
    Класс FileManager предназначен для управления файловой системой внутри директории MEDIA_ROOT в Django.
    Он организует файлы и папки по идентификатору `iin`, предоставляя методы для получения структуры каталогов,
    создания, проверки, удаления и переименования папок и файлов.

    Атрибуты:
        iin (str): Идентификатор, определяющий подпапку внутри MEDIA_ROOT.
        base_path (str): Абсолютный путь к базовой директории, соответствующей `iin`.
    """

    def __init__(self, iin):
        """
        Инициализирует экземпляр класса FileManager.

        Аргументы:
            iin (str или int): Идентификатор, используемый для создания или доступа к соответствующей подпапке в MEDIA_ROOT.

        Описание:
            - Преобразует `iin` в строку и устанавливает базовый путь как MEDIA_ROOT/iin.
            - Если базовая директория не существует, она создается.
        """
        self.iin = str(iin)
        self.base_path = os.path.join(settings.MEDIA_ROOT, self.iin)
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def _get_full_path(self, path):
        """
        Формирует абсолютный путь на основе относительного пути и базовой директории.

        Аргументы:
            path (str): Относительный путь внутри базовой директории.

        Возвращает:
            str: Абсолютный путь, объединяющий base_path и path.

        Исключения:
            ValueError: Если сформированный путь выходит за пределы базовой директории (предотвращение обхода директорий).
        """
        full_path = os.path.normpath(os.path.join(self.base_path, path))
        # Проверка, чтобы полный путь находился внутри базовой директории
        if os.path.commonpath([self.base_path, full_path]) != self.base_path:
            raise ValueError("Неверный путь")
        return full_path

    def get_directory_structure(self, path=""):
        """
        Получает структуру всех файлов и папок в указанном каталоге.

        Аргументы:
            path (str, опционально): Относительный путь внутри базовой директории для сканирования.
                                      По умолчанию сканируется базовая директория.

        Возвращает:
            list: Список словарей, представляющих структуру каталогов и файлов.
                  Каждый словарь содержит ключи `name`, `type`, и дополнительные в зависимости от типа.
        """
        full_path = self._get_full_path(path)
        structure = self._scan_directory(full_path)
        return structure

    def _scan_directory(self, path):
        """
        Рекурсивно сканирует директорию и собирает информацию о файлах и подпапках.

        Аргументы:
            path (str): Абсолютный путь к директории для сканирования.

        Возвращает:
            list: Список элементов в директории с их деталями.
        """
        items = []
        if os.path.exists(path):
            for name in sorted(os.listdir(path)):
                item_path = os.path.join(path, name)
                if os.path.isdir(item_path):
                    items.append({
                        'name': name,
                        'type': 'directory',
                        'children': self._scan_directory(item_path)
                    })
                else:
                    rel_path = os.path.relpath(item_path, settings.MEDIA_ROOT)
                    items.append({
                        'name': name,
                        'type': 'file',
                        'src': os.path.join(settings.MEDIA_URL, rel_path).replace('\\', '/')
                    })
        return items

    def create_directory(self, path, directory_name):
        """
        Создает новую папку в указанном каталоге.

        Аргументы:
            path (str): Относительный путь внутри базовой директории, где нужно создать папку.
            directory_name (str): Название новой папки.

        Возвращает:
            bool: True, если папка успешно создана, иначе False (например, если папка уже существует).
        """
        full_path = self._get_full_path(os.path.join(path, directory_name))
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            return True
        return False  # Папка уже существует

    def check_directory_exists(self, path, directory_name):
        """
        Проверяет, существует ли папка с заданным именем в указанном каталоге.

        Аргументы:
            path (str): Относительный путь внутри базовой директории для поиска.
            directory_name (str): Название папки для проверки.

        Возвращает:
            bool: True, если папка существует и является директорией, иначе False.
        """
        full_path = self._get_full_path(os.path.join(path, directory_name))
        return os.path.exists(full_path) and os.path.isdir(full_path)

    def delete_directory(self, path, directory_name):
        """
        Рекурсивно удаляет папку и все ее содержимое в указанном каталоге.

        Аргументы:
            path (str): Относительный путь внутри базовой директории, где находится папка.
            directory_name (str): Название папки для удаления.

        Возвращает:
            bool: True, если папка успешно удалена, иначе False.
        """
        full_path = self._get_full_path(os.path.join(path, directory_name))
        if os.path.exists(full_path) and os.path.isdir(full_path):
            shutil.rmtree(full_path)
            return True
        return False

    def rename_directory(self, path, directory_name, new_name):
        """
        Переименовывает существующую папку в указанном каталоге.

        Аргументы:
            path (str): Относительный путь внутри базовой директории, где находится папка.
            directory_name (str): Текущее название папки.
            new_name (str): Новое название папки.

        Возвращает:
            bool: True, если переименование прошло успешно, иначе False.
        """
        old_path = self._get_full_path(os.path.join(path, directory_name))
        new_path = self._get_full_path(os.path.join(path, new_name))
        if os.path.exists(old_path) and os.path.isdir(old_path):
            os.rename(old_path, new_path)
            return True
        return False

    def add_file(self, path, file_obj):
        """
        Добавляет файл в указанный каталог.

        Аргументы:
            path (str): Относительный путь внутри базовой директории, куда нужно добавить файл.
            file_obj (UploadedFile): Объект файла, полученный, например, из формы Django.

        Возвращает:
            list: Обновленная структура каталога после добавления файла.

        Описание:
            - Создает директорию, если она не существует.
            - Сохраняет файл поблочно для эффективной работы с большими файлами.
            - Возвращает обновленную структуру директории.
        """
        full_path = self._get_full_path(path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        file_path = os.path.join(full_path, file_obj.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)
        return self.get_directory_structure(path)

    def delete_file(self, path, file_name):
        """
        Удаляет указанный файл из каталога.

        Аргументы:
            path (str): Относительный путь внутри базовой директории, где находится файл.
            file_name (str): Название файла для удаления.

        Возвращает:
            list или bool: Обновленная структура каталога после удаления файла, 
                          или False, если файл не был найден.

        Описание:
            - Проверяет существование файла.
            - Удаляет файл, если он существует.
            - Возвращает обновленную структуру каталога.
        """
        file_path = self._get_full_path(os.path.join(path, file_name))
        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)
            return self.get_directory_structure(path)
        return False

    def rename_file(self, path, old_file_name, new_file_name):
        """
        Переименовывает существующий файл, сохраняя его расширение.

        Аргументы:
            path (str): Относительный путь внутри базовой директории, где находится файл.
            old_file_name (str): Текущее название файла.
            new_file_name (str): Новое название файла без расширения.

        Возвращает:
            bool: True, если переименование прошло успешно, иначе False.

        Описание:
            - Сохраняет расширение оригинального файла.
            - Переименовывает файл, добавляя новое имя и исходное расширение.
        """
        old_file_path = self._get_full_path(os.path.join(path, old_file_name))
        root, ext = os.path.splitext(old_file_name)
        new_file_name_with_ext = new_file_name + ext
        new_file_path = self._get_full_path(os.path.join(path, new_file_name_with_ext))
        if os.path.exists(old_file_path) and os.path.isfile(old_file_path):
            os.rename(old_file_path, new_file_path)
            return True
        return False

    def create_file(self, path, file_name):
        """
        Создает пустой файл в указанном каталоге.

        Аргументы:
            path (str): Относительный путь внутри базовой директории, где нужно создать файл.
            file_name (str): Название нового файла.

        Возвращает:
            bool: True, если файл успешно создан, иначе False (например, если файл уже существует).
        """
        full_path = self._get_full_path(os.path.join(path, file_name))
        if not os.path.exists(full_path):
            with open(full_path, 'w') as f:
                pass  # Создает пустой файл
            return True
        return False  # Файл уже существует

    def update_file(self, path, file_name, content):
        """
        Перезаписывает содержимое существующего файла.

        Аргументы:
            path (str): Относительный путь внутри базовой директории, где находится файл.
            file_name (str): Название файла для обновления.
            content (str или bytes): Новое содержимое файла.

        Возвращает:
            bool: True, если файл успешно обновлен, иначе False.
        """
        file_path = self._get_full_path(os.path.join(path, file_name))
        if os.path.exists(file_path) and os.path.isfile(file_path):
            mode = 'w' if isinstance(content, str) else 'wb'
            with open(file_path, mode) as f:
                f.write(content)
            return True
        return False
