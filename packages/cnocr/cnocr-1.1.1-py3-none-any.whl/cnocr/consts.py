# coding: utf-8
import string
from .__version__ import __version__


# 模型版本只对应到第二层，第三层的改动表示模型兼容。
# 如: __version__ = '1.2.*'，对应的 MODEL_VERSION 都是 '1.2.0'
MODEL_VERSION = '.'.join(__version__.split('.', maxsplit=2)[:2]) + '.0'

EMB_MODEL_TYPES = ['conv', 'conv-lite', 'densenet', 'densenet-lite']
SEQ_MODEL_TYPES = ['lstm', 'gru', 'fc']

root_url = (
    'https://raw.githubusercontent.com/breezedeus/cnocr-models/master/models/%s'
    % __version__
)
# name: (epochs, url)
AVAILABLE_MODELS = {
    'conv-lstm': (50, root_url + '/conv-lstm.zip'),
    'conv-lite-lstm': (45, root_url + '/conv-lite-lstm.zip'),
    'conv-lite-fc': (27, root_url + '/conv-lite-fc.zip'),
    'densenet-lite-lstm': (42, root_url + '/densenet-lite-lstm.zip'),
    'densenet-lite-fc': (32, root_url + '/densenet-lite-fc.zip'),
}

# 候选字符集合
NUMBERS = string.digits + string.punctuation
ENG_LETTERS = string.digits + string.ascii_letters + string.punctuation
