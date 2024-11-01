import torch
import torch.nn.functional as F
from torch_geometric.nn import GATConv


class GAT(torch.nn.Module):
    def __init__(self, num_features, hidden_channels, num_embeding, heads=1):
        super(GAT, self).__init__()
        self.conv1 = GATConv(num_features, hidden_channels, heads=heads)
        self.conv2 = GATConv(hidden_channels * heads, num_embeding, heads=1)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index)
        x = F.elu(x)
        x = self.conv2(x, edge_index)
        return x

    def bpr_loss(self, data, pos_edge, neg_edge):
        # Extract node embeddings from the GAT model
        emb = self.forward(data)

        # Positive and negative pairs embeddings
        pos_scores = (emb[pos_edge[0]] * emb[pos_edge[1]]).sum(dim=1)
        neg_scores = (emb[neg_edge[0]] * emb[neg_edge[1]]).sum(dim=1)

        # BPR loss computation
        loss = -torch.log(torch.sigmoid(pos_scores - neg_scores)).mean()
        return loss
