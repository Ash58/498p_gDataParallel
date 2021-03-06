import argparse

def arg_parse():
    parser = argeparse.ArgumentParser(description='arguments')
    parser.add_argument('Path',metavar='path',type=str,help='the path to list')
    parser.add_argument('Path',metavar='path',type=str,help='the path to list')
    parser.add_argument('Path',metavar='path',type=str,help='the path to list')
    
    args = parser.parse_args()
    return args

parser = argparse.ArgumentParser(description='OGBN-Products (GraphSAINT) - Single GPU')
    parser.add_argument('--device', type=int, default=0)
    parser.add_argument('--inductive', action='store_true')
    parser.add_argument('--num_layers', type=int, default=3)
    parser.add_argument('--hidden_channels', type=int, default=256)
    parser.add_argument('--dropout', type=float, default=0.5)
    parser.add_argument('--batch_size', type=int, default=20000)
    parser.add_argument('--walk_length', type=int, default=3)
    parser.add_argument('--lr', type=float, default=0.01)
    parser.add_argument('--num_steps', type=int, default=30)
    parser.add_argument('--epochs', type=int, default=50)
    parser.add_argument('--eval_steps', type=int, default=10)
    parser.add_argument('--eval_enable', type=bool, default=True)    
    parser.add_argument('--dataset_path', type=str, default="/fs/class-projects/fall2020/cmsc498p/c498p001/data/Products")
    parser.add_argument('--log_path', type=str, default="graph_saint_co_single.txt")
    args = parser.parse_args()