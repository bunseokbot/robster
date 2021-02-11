from zipfile import ZipFile, is_zipfile

from dexparser import Dexparser

from .log import logger

import framework
import importlib
import os


FRAMEWORK_KEYWORD = [
    b'ReLU',
    b'Softmax',
    b'conv1',
]


FRAMEWORK_METHOD = {
    b'Lorg/tensorflow/lite': 'tflite',
    b'Lcom/googlecode/tesseract': 'tesseract',
    b'Lorg/pytorch': 'pytorch'
}


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
        self.methods = []

    def scan(self):
        self.scan_dex()
        self.scan_asset()

    def scan_dex(self):
        dexfiles = self._read_dexfiles()
        classes = set()

        for dexfile in dexfiles:
            dex = Dexparser(fileobj=self.zfile.read(dexfile))
            string_table = dex.get_strings()
            type_table = dex.get_typeids()
            method_keywords = list(FRAMEWORK_METHOD.keys())
            method_tmp = set()

            for method in dex.get_methods():
                class_name = string_table[type_table[method['class_idx']]]
                for keyword in method_keywords:
                    if class_name.startswith(keyword):
                        method_name = class_name + string_table[method['name_idx']]
                        if method_name not in method_tmp:
                            method_tmp.add(method_name)
                            self.methods.append({
                                'type': FRAMEWORK_METHOD[keyword],
                                'method': method_name.decode()
                            })

    def scan_asset(self):
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
                    self.keywords.append({
                        'keyword': keyword,
                        'path': filepath
                    })

    def _load_frameworks(self):
        frameworks = []

        for module_name in framework.__all__:
            mod = importlib.import_module(f"framework.{module_name}")
            classes = dir(mod)
            for class_name in classes[:classes.index("__builtins__")]:
                frameworks.append(getattr(mod, class_name)())

        logger.debug(f"{len(frameworks)} framework(s) are loaded successfully")

        return frameworks

    def read(self, path):
        return self.zfile.read(path)

    def _read_assets(self):
        return [name for name in self.zfile.namelist() if name.startswith("assets")]

    def _read_dexfiles(self):
        return [name for name in self.zfile.namelist() if name.endswith('.dex')]
