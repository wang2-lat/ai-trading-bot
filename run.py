#!/usr/bin/env python3
"""
AI Trading Bot - Entry Point
Run this script to execute one trading cycle
"""

from trader import Trader
from logger import logger
import sys

def main():
    try:
        logger.info("AI Trading Bot Starting...")

        trader = Trader()
        trader.execute_trading_cycle()

        logger.info("AI Trading Bot Finished Successfully")
        return 0

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
