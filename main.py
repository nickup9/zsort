#!/usr/bin/env python3
from Killboard import Killboard


dark_taboo = Killboard()
dark_taboo.pull_kills()
dark_taboo.to_file()