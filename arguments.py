import argparse

def arg_parse():
    parser = argeparse.ArgumentParser(description='arguments')
    parser.add_argument('Path',metavar='path',type=str,help='the path to list')
    parser.add_argument('Path',metavar='path',type=str,help='the path to list')
    parser.add_argument('Path',metavar='path',type=str,help='the path to list')
    
    args = parser.parse_args()
    return args