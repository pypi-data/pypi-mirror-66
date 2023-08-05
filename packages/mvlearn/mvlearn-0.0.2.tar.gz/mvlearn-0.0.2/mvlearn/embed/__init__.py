from .gcca import GCCA
from .omnibus import Omnibus
from .mvmds import MVMDS
from .splitae import SplitAE
from .kcca import KCCA
from .dcca import DCCA, linear_cca, cca_loss, MlpNet, DeepPairedNetworks
from .utils import select_dimension

__all__ = [
    "GCCA",
    "Omnibus",
    "MVMDS",
    "SplitAE",
    "KCCA",
    "DCCA",
    "select_dimension",
]
