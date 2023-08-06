import pickle
import codecs

def get_vocab_size(model):
    if '-' in model:
        vocab_size=int(model.split("-")[-1])
    else:
        vocab_size=10
    return vocab_size

def dict_to_list(dictionary):
    vector  = []
    for key in sorted(dictionary):
        vector.append(dictionary[key])
    pickled = codecs.encode(pickle.dumps(vector), "base64").decode()
    return pickled
