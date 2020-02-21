#!/usr/bin/env python

import sys
from src.cli import cli

if __name__ == '__main__':
    if sys.version_info < (3, 6, 0):
        sys.exit('Python >= 3.6 required')
    cli()
