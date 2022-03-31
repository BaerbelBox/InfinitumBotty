#!/bin/python

"""
mainfile, initializes everything
"""

# function declarations
from argparse import ArgumentParser

from FaustBot.FaustBot import FaustBot

if __name__ == "__main__":
    arg_parser = ArgumentParser(description="FautBot - ")
    arg_parser.add_argument('--config', required=True, type=str, help="Path to the configuration file")
    args = arg_parser.parse_args()
    bot = FaustBot(args.config)
    bot.run()
