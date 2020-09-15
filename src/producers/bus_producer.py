import sys
sys.path.append('.')

from src.models.parser import Parser

parser = Parser('bus')
parser.obtain_data()