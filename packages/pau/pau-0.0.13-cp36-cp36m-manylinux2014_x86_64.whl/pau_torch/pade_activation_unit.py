import torch.nn as nn

try:
    from pau_torch.pade_cuda_functions import *
except:
    print('error importing pade_cuda, is cuda not avialable?')

from pau_torch.pade_pytorch_functions import *

init_w_numerator = [5.49891645e-02, 5.05004092e-01, 1.24178396e+00, 1.25790914e+00, 5.18128693e-01, 7.84309418e-02]
init_w_denominator = [1.76585345e-05, 2.49089658e+00, 8.24388417e-07, 1.55309717e-01]


class PAU(nn.Module):

    def __init__(self, w_numerator=init_w_numerator, w_denominator=init_w_denominator, cuda=True, version="B"):
        super(PAU, self).__init__()

        self.weight_numerator = nn.Parameter(torch.FloatTensor(w_numerator), requires_grad=True)
        self.weight_denominator = nn.Parameter(torch.FloatTensor(w_denominator), requires_grad=True)

        if cuda:
            if version == "A":
                pau_func = PAU_CUDA_A_F
            elif version == "B":
                pau_func = PAU_CUDA_B_F
            elif version == "C":
                pau_func = PAU_CUDA_C_F
            elif version == "D":
                pau_func = PAU_CUDA_D_F
            else:
                raise ValueError("version %s not implemented" % version)

            self.activation_function = pau_func.apply
        else:
            if version == "A":
                pau_func = PAU_PYTORCH_A_F
            elif version == "B":
                pau_func = PAU_PYTORCH_B_F
            elif version == "C":
                pau_func = PAU_PYTORCH_C_F
            elif version == "D":
                pau_func = PAU_PYTORCH_D_F
            else:
                raise ValueError("version %s not implemented" % version)

            self.activation_function = pau_func

    def forward(self, x):
        out = self.activation_function(x, self.weight_numerator, self.weight_denominator, self.training)
        return out
