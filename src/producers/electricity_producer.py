import sys

sys.path.append('.')

from src.models.parser import Parser

parser = Parser('electricity')
parser.obtain_data()