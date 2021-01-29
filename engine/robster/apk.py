from zipfile import ZipFile, is_zipfile

from .log import logger

import framework
import importlib
import os


FRAMEWORK_KEYWORD = [
    b'ReLU',
    b'Softmax',
    b'conv1',
]


class InvalidAPKFileError(Exception):
    pass


class APK(object):
    def __init__(self, path):
        if not is_zipfile(path):
            raise InvalidAPKFileError(f"{path} is not an APK file")

        self.filename = os.path.basename(path)
        self.zfile = ZipFile(path)
        self.models = []
        self.keywords = []

    def scan(self):
        files = self._read_assets()
        logger.debug(f"{len(files)} asset(s) found")

        if len(files) == 0:
            return

        patterns = self._load_frameworks()

        for filepath in files:
            stream = self.zfile.read(filepath)

            for pattern in patterns:
                is_found = pattern.detect(stream)
                if is_found:
                    logger.debug(f"Detect {pattern.name} framework - {filepath}")
                    self.models.append({
                        'type': pattern.name,
                        'path': filepath,
                    })
                    break
    
            if is_found:
                continue

            for keyword in FRAMEWORK_KEYWORD:
                if keyword in stream:
                    self.models.append({
                        'keyword': keyword,
                        'path': filepath
                    })

    def _load_frameworks(self):
        frameworks = []

        for module_name in framework.__all__:
            mod = importlib.import_module(f"framework.{module_name}")
            for class_name in [value for value in dir(mod) if not value.startswith("__")]:
                frameworks.append(getattr(mod, class_name)())

        logger.debug(f"{len(frameworks)} framework(s) are loaded successfully")

        return frameworks

    def _read_assets(self):
        return [name for name in self.zfile.namelist() if name.startswith("assets")]
