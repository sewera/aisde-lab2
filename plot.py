import numpy as np
from matplotlib import pyplot as plt
import sys
import json

if __name__ == '__main__':
    files = sys.argv[1:]
    with open(str(files[0])) as input_file:
        data = json.load(input_file)

    print(data)
