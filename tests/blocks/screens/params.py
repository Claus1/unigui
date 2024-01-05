
from unigui import *
order = 2
name = 'Parameters'

def get_params(button, _):
    return Info(str(block.params))

block = ParamBlock('System parameters', Button('Show server params', get_params), 
    per_device_eval_batch_size=16,
    num_train_epochs=10, 
    warmup_ratio=0.1, 
    logging_steps=10, 
    device = ['cpu', 'gpu'],
    load_best = True)


blocks = [block]