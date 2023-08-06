import torch
import hashlib
import time
from tqdm import tqdm
import sentencepiece as spm
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

def generate_protein(model, tokenizer, protein_start = '<gene86>', protein_len = 2000, temperature = 0.8):
    """
        Evaluation step (generating text using the learned model)
        
    """
    flag = False
    
    while not flag:
        # Number of characters to generate
        num_generate = protein_len

        # Converting our start string to numbers (vectorizing)
        input_eval = torch.tensor(tokenizer.EncodeAsIds(protein_start))
        input_eval = torch.autograd.Variable(input_eval.unsqueeze(0)).cuda()


        # Empty string to store our results
        text_generated = ''
        
        # Low temperatures results in more predictable text.
        # Higher temperatures results in more surprising text.
        # Experiment to find the best setting.
    
    
        # Here batch size == 1
        hidden = None
        for i in range(num_generate):
            flag = False
            predictions, hidden = model(input_eval, [input_eval.size(1)], hidden=hidden)
            predictions = predictions.view(-1).div(temperature).exp()
            check = False in torch.isfinite(predictions)
            if(not check):
                next_protein_int = torch.multinomial(predictions, 1)      
                next_protein_char = tokenizer.DecodeIds(next_protein_int.tolist())
            else:
                print("Inf")
                break
                
            if(next_protein_char == '</gene86>'):
                flag = True
                break

            text_generated += next_protein_char
            if(len(text_generated) >= protein_len):
                flag = True
                break

            input_eval = next_protein_int
            input_eval = torch.autograd.Variable(input_eval.unsqueeze(0)).cuda()

    return text_generated


def generate_synth_faa(model, tokenizer_path, output_faa_path, num_seq, protein_start, vocab_restrict=[False], temp=0.4, max_len=2119):
    
    hash = hashlib.sha1()
    hash.update(str(time.time()).encode('utf-8'))
    faa_filename = output_faa_path.joinpath(hash.hexdigest() + "_COG0086.faa")
    
    sp = spm.SentencePieceProcessor()
    sp.Load(str(tokenizer_path))
    
    if(vocab_restrict[0] == True):
        sp.set_vocabulary(vocab_restrict[1])
            
    with open(faa_filename,'a') as fp:
        print(f"Writing to file:{faa_filename}")
        for i in tqdm(range(num_seq)):
            model.eval()
            sample_seq = Seq(generate_protein(model, sp, protein_start, max_len, temp))
            sample_record = SeqRecord(sample_seq)
            hash.update(str(time.time()).encode('utf-8'))
            sample_record.id = hash.hexdigest() + '_COG0086'
            sample_record.description = f'Synthetic beta\' temp={temp}'
            SeqIO.write(sample_record, fp, "fasta") 
