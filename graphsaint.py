import os.path as osp
from datetime import datetime
import argparse
import arguments
import torch
import torch.nn.functional as F
from torch_geometric.datasets import Flickr
from torch_geometric.data import GraphSAINTRandomWalkSampler,DataListLoader
from torch_geometric.nn import GraphConv, DataParallel
from torch_geometric.utils import degree
import torch_geometric.transforms as T
# from torch.nn.parallel import DataParallel
import graphsaint_args

class Net(torch.nn.Module):
    def __init__(self, hidden_channels):
        super(Net, self).__init__()
        in_channels = dataset.num_node_features
        out_channels = dataset.num_classes
        self.conv1 = GraphConv(in_channels, hidden_channels)
        self.conv2 = GraphConv(hidden_channels, hidden_channels)
        self.conv3 = GraphConv(hidden_channels, hidden_channels)
        self.lin = torch.nn.Linear(3 * hidden_channels, out_channels)

    def set_aggr(self, aggr):
        self.conv1.aggr = aggr
        self.conv2.aggr = aggr
        self.conv3.aggr = aggr

    def forward(self, x0, edge_index, edge_weight=None):
        x1 = F.relu(self.conv1(x0, edge_index, edge_weight))
        x1 = F.dropout(x1, p=0.2, training=self.training)
        x2 = F.relu(self.conv2(x1, edge_index, edge_weight))
        x2 = F.dropout(x2, p=0.2, training=self.training)
        x3 = F.relu(self.conv3(x2, edge_index, edge_weight))
        x3 = F.dropout(x3, p=0.2, training=self.training)
        x = torch.cat([x1, x2, x3], dim=-1)
        x = self.lin(x)
        return x.log_softmax(dim=-1)

def train():
    model.train()
    model.set_aggr('add' if args.use_normalization else 'mean')

    total_loss = total_examples = 0
    for data in loader:
        data = data.to(device)
        optimizer.zero_grad()

        if args.use_normalization:
            edge_weight = data.edge_norm * data.edge_weight
            out = model(data.x, data.edge_index, edge_weight)
            loss = F.nll_loss(out, data.y, reduction='none')
            loss = (loss * data.node_norm)[data.train_mask].sum()
        else:
            out = model(data.x, data.edge_index)
            loss = F.nll_loss(out[data.train_mask], data.y[data.train_mask])

        loss.backward()
        optimizer.step()
        total_loss += loss.item() * data.num_nodes
        total_examples += data.num_nodes
    return total_loss / total_examples


@torch.no_grad()
def test():
    model.eval()
    model.set_aggr('mean')

    out = model(data.x.to(device), data.edge_index.to(device))
    pred = out.argmax(dim=-1)
    correct = pred.eq(data.y.to(device))

    accs = []
    for _, mask in data('train_mask', 'val_mask', 'test_mask'):
        accs.append(correct[mask].sum().item() / mask.sum().item())
    return accs

path = osp.join(osp.dirname(osp.realpath(__file__)), '..', 'data', 'Flickr')
dataset = Flickr(path)
data = dataset[0]
row, col = data.edge_index
data.edge_weight = 1. / degree(col, data.num_nodes)[col]  # Norm by in-degree.

# parser = argparse.ArgumentParser()
# parser.add_argument('--use_normalization', action='store_true')
# args = parser.parse_args()

args = graphsaint_args.arg_parse()

loader = GraphSAINTRandomWalkSampler(data, batch_size=args.batch_size, walk_length=2,
                                     num_steps=5, sample_coverage=100,
                                     save_dir=dataset.processed_dir,
                                     num_workers=4)
loader = DataListLoader(loader, batch_size=args.batch_size, shuffle=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = Net(hidden_channels=256)
if args.gpu=="multi": 
    model = DataParallel(model)
model = model.to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

f = open(args.log_path, 'w')

for epoch in range(1, args.epochs + 1):
    start_epoch = datetime.now()
    loss = train()
    end_epoch = datetime.now()

    train_acc, val_acc, test_acc = test()
    print(f'Epoch: {epoch:02d}, Loss: {loss:.4f}', ",\tTime: ", str(end_epoch - start_epoch), f', Train: {train_acc:.4f}, Val: {val_acc:.4f}, Test: {test_acc:.4f}')  
    print(f'Epoch: {epoch:02d}, Loss: {loss:.4f}', ",\tTime: ", str(end_epoch - start_epoch), f', Train: {train_acc:.4f}, Val: {val_acc:.4f}, Test: {test_acc:.4f}', file=f)  
    f.flush()
    
f.close()