import argparse
import os
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from sumologic import client
from sumologic.api import content, folder, permission


parser = argparse.ArgumentParser()
parser.add_argument('access_id', type=str, help="Sumologic API access ID")
parser.add_argument('access_key', type=str, help="Sumologic API access key")
parser.add_argument('endpoint', type=str, help="Sumologic API endpoint")
