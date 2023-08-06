import torch
import numpy as np


def recurrence_plot(x, threshold):
    """
    x is a tensor or ndarray w/ shape (..., T). 
    first dims will go -1
    """
    _x = x
    if isinstance(x, np.ndarray):
        _x = torch.from_numpy(x)
    try:
        _x.to(torch.device('cuda'))
    except:
        pass

    ndim = len(_x.size())
    if ndim == 1:
        _x = _x.view((1, -1))
    n, t = _x.size()
    _m = _x

    return torch.norm(_x.expand((n, t, t)) - _x.expand((n, t, t)).transpose(1, 2), p=2, dim=0) < threshold

def recurrence_rate(rp, omit_diag=True):
    n = rp.size()[-1]
    rr = rp.sum().item() / n**2
    if omit_diag:
        return rr - 1./n
    else:
        return rr


