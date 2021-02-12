from argparse import ArgumentParser

from robster.log import logger
from robster.apk import APK, InvalidAPKFileError

import glob
import os


count = 0



def run_engine_as_single_mode(path):
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
            for keyword in keywords:
                logger.debug(f"Asset: {keyword['path']} Keyword: {keyword['keyword']}")

        methods = apk.methods
        if methods:
            logger.info("ML method found")
            for method in methods:
                logger.debug(f"Asset: {method['method']} Type: {method['type']}")

        if models or keywords or methods:
            count += 1

        del apk

    except InvalidAPKFileError as apkfileerror:
        logger.error(apkfileerror)

    except Exception:
        logger.error("Worker error", exc_info=True)


def run_engine_as_worker_mode():
    logger.info("Starting APK analysis worker")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", help="Path of APK file")
    parser.add_argument("-d", "--directory", help="Directory path of APK file(s)")
    parser.add_argument("-w", "--worker", action="store_true", help="Run as worker mode")
    args = parser.parse_args()
    
    if args.file is not None:
        logger.debug("File mode detected")
        if not os.path.isfile(args.file):
            raise FileNotFoundError(args.file)

        run_engine_as_single_mode(args.file)

    elif args.directory is not None:
        logger.debug("Directory mode detected")
        files = glob.glob(os.path.join(args.directory, "*"))

        for filepath in files:
            run_engine_as_single_mode(filepath)

        logger.info(f"Total count: {count}")

    elif args.worker:
        logger.debug("Worker mode detected")
        run_engine_as_worker_mode()

    else:
        logger.error("Invaild option")
