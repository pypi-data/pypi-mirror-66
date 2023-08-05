try:
    import vamp
    vamp_imported = True
except Exception:
    vamp_imported = False

# Current nussl version
__version__ = '1.0.1'

class ImportErrorClass(object):
    def __init__(self, lib, **kwargs):
        raise ImportError(f'Cannot import {type(self).__name__} because {lib} is not installed')


from .core import AudioSignal, STFTParams
from .core import utils, efz_utils, play_utils, constants, mixing

from . import core
from . import evaluation
from . import datasets
from . import ml
from . import separation

