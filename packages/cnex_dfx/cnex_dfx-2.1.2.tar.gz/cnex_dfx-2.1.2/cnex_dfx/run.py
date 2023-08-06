import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from optparse import OptionParser
from lib.executor import Executor


def runner(option):
    executor = Executor(option.rout)
    if option.list:
        executor.list()
    else:
        executor.execute(option.dfx_file)
    return 0


def main():
    parser = OptionParser()
    parser.add_option('--dfx', dest='dfx_file', type=str, default=None, help='dfx file name')
    parser.add_option('--list', dest='list', action='store_true', help="List all scripts name.")
    parser.add_option('--rout', dest='rout', choices=["rdma", "pcie"], default="rdma",  help="rdma or pcie")
    options, args = parser.parse_args()
    sys.exit(runner(options))

if __name__ == '__main__':
    main()
