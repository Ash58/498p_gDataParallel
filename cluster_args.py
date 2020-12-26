import argparse

def arg_parse():
    parser = argparse.ArgumentParser(description='Reddit (Cluster-GCN)')
    parser.add_argument('--gpu', type=str, default="single" )
    parser.add_argument('--batch_size', type=int, default=12)
    parser.add_argument('--lr', type=float, default=0.005)
    parser.add_argument('--epochs', type=int, default=50)
    parser.add_argument('--eval_steps', type=int, default=10)
    parser.add_argument('--eval_enable', type=bool, default=True)    
    parser.add_argument('--dataset_path', type=str, default="/fs/class-projects/fall2020/cmsc498p/c498p001/data/Reddit")
    parser.add_argument('--log_path', type=str, default="cluster_gcn.txt")
    args = parser.parse_args()
    return args