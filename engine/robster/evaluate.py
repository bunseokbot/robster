from robster.log import logger

import evaluation
import importlib


class ModelEvaluation(object):
    def __init__(self, model, framework):
        self.model = model
        self.framework = framework

    def run(self):
        testcases = self._load_evaluation()
        
        for case in testcases:
            case.run(self.model)

    def _load_evaluation(self):
        frameworks = []

        for module_name in evaluation.__all__:
            mod = importlib.import_module(f"evaluation.{module_name}")
            classes = dir(mod)
            for class_name in classes[:classes.index("__builtins__")]:
                obj = getattr(mod, class_name)()
                if obj.name == self.framework:
                    frameworks.append(obj)

        logger.debug(f"{len(frameworks)} evaluation code(s) are loaded successfully")

        return frameworks
