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
from mgmail.app.checker import Checker


class Application:

    def __init__(self):
        self.cfg = None
        self.logger_config = 'mgmail.logging.yml'
        self.check = False
        self.load_config()

        # load logger configuration from yml file
        with open(self.logger_config, "r") as f:
            config = yaml.safe_load(f)
            logging.config.dictConfig(config)

        self.logger = logging.getLogger(__name__)

    def load_config(self):
        parser = argparse.ArgumentParser(prog='mgmail')
        parser.add_argument(
            "check",
            help="Checks if it can connect to"
            " 1. papermerge"
            " 2. imap server"
            " 3. smtp account"
        )
        parser.add_argument(
            "--config", nargs=1
        )
        parser.add_argument(
            "--logger-config", nargs=1,
            help="path to logger configuration file (as yml)"
        )
        args = parser.parse_args()
        if not args.config:
            config = "mgmail.config.py"
        else:
            config = args.config

        if args.logger_config:
            self.logger_config = args.logger_config

        self.cfg = self.load_config_from_filename(config)

        if args.check:
            self.check = True

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
        if self.check:
            self.logger.debug("Checker")
            checker = Checker(
                config=self.cfg,
                logger=self.logger
            )
            checker.run()
        else:
            read_count = import_attachment(
                config=self.cfg,
                logger=self.logger
            )
            self.logger.info(f"Total messages read {read_count}")


def run():
    Application().run()


if __name__ == '__main__':
    run()
