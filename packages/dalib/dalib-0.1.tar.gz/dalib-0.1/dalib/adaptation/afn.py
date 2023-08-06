import math
import torch.nn as nn
from dalib.modules.classifier import Classifier as ClassifierBase

__all__ = ['StepwiseAdaptiveFeatureNorm', 'ImageClassifier']


class StepwiseAdaptiveFeatureNorm(nn.Module):
    r"""Stepwise Adaptive Feature Norm proposed by `Larger Norm More Transferable:
    An Adaptive Feature Norm Approach for Unsupervised Domain Adaptation <https://arxiv.xilesou.top/abs/1811.07456>`_

    Parameters:
        - **delta_r** (float, optional): step size of :math:`\Delta r`.  Default: 1.

    Shape:
        - Input: :math:`(N, F)` where F means the dimension of input features.
        - Output: scalar.

    Examples::
        >>> loss = StepwiseAdaptiveFeatureNorm(delta_r=1.)
        >>> # features from source domain or target domain
        >>> features= torch.randn(10, 1024)
        >>> output = loss(feautures)
    """

    def __init__(self, delta_r=1.):
        super(StepwiseAdaptiveFeatureNorm, self).__init__()
        self.detal_r = delta_r

    def forward(self, features):
        radius = features.norm(p=2, dim=1).detach()
        radius += self.detal_r
        return ((features.norm(p=2, dim=1) - radius) ** 2).mean()


class L2PreservedDropout(nn.Module):
    """Dropout that preserves the L2-norm in both of the training and evaluation phases.

    Given a d-dimensional input vector :math:`x`, in the training phase, randomly zero the element
    with probability :math:`p` by samples.
    In the evaluation phase, scale the output by a factor of :math:`\dfrac{1}{\sqrt{1-p}}`.
    """

    def __init__(self, *args, **kwargs):
        super(L2PreservedDropout, self).__init__()
        self.dropout = nn.Dropout(*args, **kwargs)

    def forward(self, input):
        output = self.dropout(input)
        if self.training:
            output.mul_(math.sqrt(1 - self.dropout.p))
        return output


class ImageClassifier(ClassifierBase):
    def __init__(self, backbone, num_classes, bottleneck_dim=1000, dropout_p=0.5):
        bottleneck = nn.Sequential(
            nn.Linear(backbone.out_features, bottleneck_dim),
            nn.BatchNorm1d(bottleneck_dim, affine=True),
            nn.ReLU(inplace=True),
            L2PreservedDropout(dropout_p)
        )
        super(ImageClassifier, self).__init__(backbone, num_classes, bottleneck, bottleneck_dim)

    def get_parameters(self):
        params = [
            {"params": self.backbone.parameters(), "momentum": 0., 'lr_mult': 1.},
            {"params": self.bottleneck.parameters(), "momentum": 0.9, 'lr_mult': 1.},
            {"params": self.head.parameters(), "momentum": 0.9, 'lr_mult': 1.},
        ]
        return params
