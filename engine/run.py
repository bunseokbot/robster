from argparse import ArgumentParser
from concurrent import futures
from datetime import datetime

from pymongo import MongoClient

from robster.log import logger
from robster.apk import APK, InvalidAPKFileError

import protos.robster_pb2 as robster_pb2
import protos.robster_pb2_grpc as robster_pb2_grpc

import grpc
import glob
import time
import os


count = 0
client = MongoClient(f"mongodb://{os.environ.get('MONGODB_HOST', 'localhost')}:27017/")

MODEL_PATH = os.environ.get("MODEL_PATH", "models")
if not os.path.isdir(MODEL_PATH):
    os.makedirs(MODEL_PATH)


class Robster(robster_pb2_grpc.RobsterServicer):
    def _make_report(self, _id, apk):
        report = {
            '_id': _id,
            'filehash': apk.sha256,
            'models': apk.models,
            'keywords': apk.keywords,
            'methods': apk.methods,
        }

        for model in apk.models:
            self._save_model(model['hash'], apk.read(model['path']))
    
        return report

    def _save_model(self, filehash, content):
        path = os.path.join(MODEL_PATH, filehash)
        with open(path, 'wb') as f:
            f.write(content)

    def _save_report(self, report):
        now = datetime.now().isoformat()
        report['time'] = now
        reports = client.robster.reports
        with client.start_session(causal_consistency=True) as session:
            reports.insert_one(report, session=session)
        logger.debug("Successfully save report")

    def ExecuteAnalysis(self, request, context):
        _id = request.id
        status = True
        message = "success"

        try:
            apk = APK(request.path)
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

            report = self._make_report(_id=request.id, apk=apk)
            self._save_report(report)

            del apk

        except InvalidAPKFileError:
            status = False
            message = "invalid apk"
            logger.error("APK error", exc_info=True)

        except:
            status = False
            message = "worker error"
            logger.error("Worker error", exc_info=True)

        finally:
            return robster_pb2.AnalysisResponse(
                id=request.id,
                status=status,
                message=message,
            )


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
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    robster_pb2_grpc.add_RobsterServicer_to_server(Robster(), server)
    server.add_insecure_port('0.0.0.0:50051')
    server.start()

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        server.stop(0)


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
