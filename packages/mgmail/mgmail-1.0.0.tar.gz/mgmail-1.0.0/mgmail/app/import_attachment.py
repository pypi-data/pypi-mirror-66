import yaml
import logging.config
import os
import argparse
import logging
import sys
import traceback
import importlib.util
import importlib.machinery

from mgmail.attachment import import_attachment


with open('mgmail.logging.yml', "r") as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)


class Application:

    def __init__(self):
        self.cfg = None
        self.load_config()
        self.logger = logging.getLogger(__name__)

    def load_config(self):
        parser = argparse.ArgumentParser(prog='mgmail')
        parser.add_argument(
            "--config", nargs=1
        )
        args = parser.parse_args()
        if not args.config:
            config = "mgmail.config.py"
        else:
            config = args.config

        self.cfg = self.load_config_from_filename(config)

    def load_config_from_filename(self, filename):

        if not os.path.exists(filename):
            raise RuntimeError("%r doesn't exist" % filename)

        ext = os.path.splitext(filename)[1]

        try:
            module_name = '__config__'
            if ext in [".py", ".pyc"]:
                spec = importlib.util.spec_from_file_location(
                    module_name,
                    filename
                )
            else:
                msg = "config file should have a valid Python extension.\n"
                self.logger.warn(msg)
                loader_ = importlib.machinery.SourceFileLoader(
                    module_name,
                    filename
                )
                spec = importlib.util.spec_from_file_location(
                    module_name,
                    filename,
                    loader=loader_
                )
            mod = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = mod
            spec.loader.exec_module(mod)
        except Exception:
            print("Failed to read config file: %s" % filename, file=sys.stderr)
            traceback.print_exc()
            sys.stderr.flush()
            sys.exit(1)

        return vars(mod)

    def run(self):
        read_count = import_attachment(
            config=self.cfg,
            logger=self.logger
        )
        self.logger.info(f"Total messages read {read_count}")


def run():
    Application().run()


if __name__ == '__main__':
    run()
