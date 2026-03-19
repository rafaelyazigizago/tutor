import argparse
from build_logger import BuildLogger

logger = BuildLogger()

parser = argparse.ArgumentParser()

parser.add_argument("--step", help="Step title")
parser.add_argument("--desc", help="Step description")
parser.add_argument("--cmd", help="Command executed")
parser.add_argument("--decision", help="Architecture decision")

args = parser.parse_args()

if args.step:
    logger.log_step(args.step, args.desc or "")

if args.cmd:
    logger.log_command(args.cmd)

if args.decision:
    logger.log_decision(args.decision)