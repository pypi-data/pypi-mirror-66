import sentencepiece as spm
import torch

class COG86_Dataset(torch.utils.data.Dataset):
    """COG0086 dataset."""

    def __init__(self, txt_path, tokenizer_path, vocab_restrict = [False]):
        """
        Args:
            path_txt_file (string): Path to the txt file that contains the seq.
        """


        with open(txt_path) as fp:
            genes = fp.readlines()
        
        self.sp = spm.SentencePieceProcessor()
        self.sp.Load(str(tokenizer_path))
        if(vocab_restrict[0] == True):
            self.sp.set_vocabulary(vocab_restrict[1])
            
        print("Processing data")
        self.genes_processed, self.genes_len = self.preprocess(genes)
        self.max_len = max(self.genes_len)
        print(f"Max length:{self.max_len}")
        print(f"Min length:{min(self.genes_len)}")
        
    def __len__(self):
        return len(self.genes_processed)
    
    def preprocess(self, genes):
        
        genes_as_ids = []
        genes_len = []
        for gene in genes:
            gene_as_ids = self.sp.EncodeAsIds(gene.rstrip())
            genes_len.append(len(gene_as_ids))
            genes_as_ids.append(torch.tensor(gene_as_ids))
        
        return genes_as_ids, genes_len

        
    def __getitem__(self, idx):
        return self.genes_processed[idx], self.genes_len[idx]

def collate_fn_padd(batch):
    '''
    Padds batch of variable length

    note: it converts things ToTensor manually here since the ToTensor transform
    assume it takes in images rather than arbitrary tensors.
    '''
    ## get sequence lengths
    seq, size = zip(*batch)
    seq, size = list(seq), torch.tensor(size)
    
    size_sorted, ind = torch.sort(size, descending = True)
    
    
    seq_input = [seq[i][:-1] for i in ind]
    seq_output = [seq[i][1:] for i in ind]
 
    seq_input = torch.nn.utils.rnn.pad_sequence(seq_input, batch_first=True)
    seq_output = torch.nn.utils.rnn.pad_sequence(seq_output, batch_first=True)
  
    return seq_input, seq_output, size_sorted - 1
    