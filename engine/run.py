from argparse import ArgumentParser

from robster.log import logger
from robster.apk import APK, InvalidAPKFileError

import glob
import os

count = 0


def worker(path):
    global count
    logger.info(f"Reading {path} file")

    try:
        apk = APK(path)
        apk.scan()

        models = apk.models
        if models:
            logger.info(f"ML model found")
            for model in models:
                logger.debug(f"Asset: {model['path']} Type: {model['type']}")

        keywords = apk.keywords
        if keywords:
            logger.info("ML keyword found")
            logger.debug(f"Asset: {model['path']} Keyword: {model['keyword']}")

        del apk

    except InvalidAPKFileError as apkfileerror:
        logger.error(apkfileerror)

    except Exception:
        logger.error("Worker error", exc_info=True)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", help="Path of APK file")
    parser.add_argument("-d", "--directory", help="Directory path of APK file(s)")
    args = parser.parse_args()
    
    if args.file is not None:
        logger.debug("File mode detected")
        if not os.path.isfile(args.file):
            raise FileNotFoundError(args.file)

        worker(args.file)

    elif args.directory is not None:
        logger.debug("Directory mode detected")
        files = glob.glob(os.path.join(args.directory, "*"))

        for filepath in files:
            worker(filepath)

    else:
        logger.error("Invaild option")
