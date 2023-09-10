from datasets import load_dataset
from lfqa_utils import *

eli5 = load_dataset('eli5')

kb = load_dataset("nodlnodl/kb", data_files='kb.json')

print(eli5['test_eli5'][11122])

print(kb['train'][45])

# training arguments
class ArgumentsQAR():
    def __init__(self):
        self.batch_size = 512
        self.max_length = 128
        self.checkpoint_batch_size = 32
        self.print_freq = 100
        self.pretrained_model_name = "sentence-transformers/paraphrase-TinyBERT-L6-v2"
        self.model_save_name = "eli5_retriever_model_l-8_h-768_b-512-512"
        self.learning_rate = 2e-4
        self.num_epochs = 10

qar_args = ArgumentsQAR()

# prepare torch Dataset objects
qar_train_dset = ELI5DatasetQARetriver(eli5['train_eli5'], training=True)
qar_valid_dset = ELI5DatasetQARetriver(eli5['validation_eli5'], training=False)

# load pre-trained BERT and make model
qar_tokenizer, qar_model = make_qa_retriever_model(
        model_name=qar_args.pretrained_model_name,
        from_file=None,
        device="cuda:0"
)

# train the model
model = train_qa_retriever(qar_model, qar_tokenizer, qar_train_dset, qar_valid_dset, qar_args)


