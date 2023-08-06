import os
import argparse

from . import generate
from . import pdf_reference
from . import read_yaml

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", "-v",
                        action="store_true",
                        help="increase output verbosity")
    parser.add_argument("--conf", "-c",
                        help="Add a configuration file")
    parser.add_argument("--time", "-t",
                        default=None,
                        help="Set begin time (eg. 15h12)")
    parser.add_argument("--out", "-o",
                        default="certificate.pdf",
                        help="Set the output filename")
    args = parser.parse_args()
    return args

def get_init_file():
    filename = os.path.join(os.environ['HOME'], ".attgen")
    try:
        return read_yaml.config(filename)
    except FileNotFoundError:
        pass

def run():
    args = init()
    config = get_init_file()
    if args.conf:
        config.update(args.conf)
    pdf_reference.generate()
    generate.main(config, args.time, args.out)

if __name__ == "__main__":
    run()
