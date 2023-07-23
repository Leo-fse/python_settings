import os
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

if __name__ == "__main__":
    p = Path(__file__).resolve().parents[1]
    py_file_list = list(p.glob("*.py"))
    print(py_file_list)
