import torch 

class CharRNN_2L_LSTM(torch.nn.Module):
    def __init__(self):
        """
        In the constructor we instantiate two nn.Linear modules and assign them as
        member variables.
        """
        super(CharRNN_2L_LSTM, self).__init__()
        
        self.encoder = torch.nn.Embedding(100, 64)
        self.lstm_1 = torch.nn.LSTM(64, 128, batch_first=True, num_layers = 2, dropout = 0.3)
        self.dense = torch.nn.Linear(128, 100)
        
        
    def forward(self, seq, len_sorted, hidden = None):
        """
        In the forward function we accept a Tensor of input data and we must return
        a Tensor of output data. We can use Modules defined in the constructor as
        well as arbitrary operators on Tensors.
        """
        if(hidden == None):
            h0 = torch.zeros(2, seq.size(0), 128).cuda().requires_grad_()
            c0 = torch.zeros(2, seq.size(0), 128).cuda().requires_grad_()
        else:
            h0, c0 = hidden
            
        seq = self.encoder(seq)
        seq_pack = torch.nn.utils.rnn.pack_padded_sequence(seq, batch_first=True, lengths=len_sorted).cuda()
        seq_pack_output, (ht, ct) = self.lstm_1(seq_pack, (h0.detach(), c0.detach()))
        output, _ = torch.nn.utils.rnn.pad_packed_sequence(seq_pack_output, batch_first=True)
        
        output = self.dense(output)
        
        return output, (ht, ct)


class models():
    """Selects appropriate model depending on user selection"""
    def __init__(self, model_type="lstm", model_path=None, pretrained=True):
        super(models, self).__init__()
        if(pretrained):
            self.model = CharRNN_2L_LSTM()
            self.model.cuda()
            self.model.load_state_dict(torch.load(model_path))
        else:
            self.model = CharRNN_2L_LSTM() if (model_type == "lstm") else None
            self.model.cuda()

    def train(self, dataloader, optimizer, criterion):
        """
        Returns the train loss
        """
        losses = []
        for seq_input, seq_output, seq_len in dataloader:
            self.model.train()
            self.model.zero_grad()
            
            seq_input, seq_output, seq_len = Variable(seq_input), Variable(seq_output), Variable(seq_len)
            seq_input, seq_output, seq_len = seq_input.cuda(), seq_output.cuda(), seq_len.cuda()

            output, _ = self.model.forward(seq_input, seq_len)
            loss = criterion(output.transpose(1, 2), seq_output)
            loss.backward()
            optimizer.step()
            losses.append(loss.item())
        return losses



    def evaluate(self, dataloader, criterion):
        """
        Returns the test/valid loss
        """
        losses = []
        for seq_input, seq_output, seq_len in dataloader:
            self.model.eval()
            
            seq_input, seq_output, seq_len = Variable(seq_input), Variable(seq_output), Variable(seq_len)
            seq_input, seq_output, seq_len = seq_input.cuda(), seq_output.cuda(), seq_len.cuda()
            
            output, _ = self.model.forward(seq_input, seq_len)
            loss = criterion(output.transpose(1, 2), seq_output)
            losses.append(loss.item())
            
        return losses 
     


        