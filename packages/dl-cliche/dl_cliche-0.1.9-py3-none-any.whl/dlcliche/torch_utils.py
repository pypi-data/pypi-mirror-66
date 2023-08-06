from .utils import *
import numpy as np
import torch
import torch.nn as nn


class LossFlooding(nn.Module):
    """Flooding wrapper.

    Example:
        >>> # Wrap CrossEntropyLoss with Flooding.
        >>> criteria = LossFlooding(nn.CrossEntropyLoss(), my_flooding_b)

    .. _Do We Need Zero Training Loss After Achieving Zero Training Error?: https://arxiv.org/abs/2002.08709
    """
    def __init__(self, criteria, b):
        super().__init__()
        self.criteria = criteria
        self.b = b

    def forward(self, input, target):
        loss = self.criteria(input, target)
        loss = (loss - self.b).abs() + self.b
        return loss


class IntraBatchMixup():
    """Mixup class that transform input and target, and runs loss calculation.
    Works with every single batch, requires small changes with training process.

    Example:
        >>> batch_mixer = IntraBatchMixup(nn.CrossEntropyLoss(), alpha=your_alpha)
        >>> # training
        >>> for inputs, labels in train_loader:
        >>>     inputs, stacked_labels = batch_mixer.transform(inputs, labels, train=True)
        >>>     outputs = model(inputs)
        >>>     loss = batch_mixer.criterion(outputs, stacked_labels)
        >>> # validation
        >>> for inputs, labels in val_loader:
        >>>     inputs, stacked_labels = batch_mixer.transform(inputs, labels, train=False)
        >>>     outputs = model(inputs)
        >>>     loss = batch_mixer.criterion(outputs, stacked_labels)

    Inspired by fast.ai: https://github.com/fastai/fastai/blob/master/fastai/callbacks/mixup.py
        "Implements [mixup](https://arxiv.org/abs/1710.09412) training method"

    Notes:
        Batch size have to be more than 2, the larger the better w.r.t. mix diversity.
    """

    def __init__(self, criterion, alpha:float=0.4):
        self.loss_func = _IntraBatchMixupLoss(criterion)
        self.alpha = alpha

    def transform(self, inputs, targets, train:bool):
        "Applies mixup to `inputs` and `targets` if `train`."

        if not train or self.alpha == 0.0:
            return inputs, [targets, targets,
                            torch.ones((targets.size(0)), dtype=torch.float).to(inputs.device)]

        lambd = np.random.beta(self.alpha, self.alpha, targets.size(0))
        lambd = np.concatenate([lambd[:,None], 1-lambd[:,None]], 1).max(1)
        lambd = inputs.new(lambd)
        shuffle = torch.randperm(targets.size(0)).to(inputs.device)

        x1, y1 = inputs[shuffle], targets[shuffle]
        out_shape = [lambd.size(0)] + [1 for _ in range(len(x1.shape) - 1)]

        mixed_inputs = (inputs * lambd.view(out_shape) + x1 * (1-lambd).view(out_shape))
        stacked_targets = [targets, y1, lambd]
        return mixed_inputs, stacked_targets

    def criterion(self, outputs, stacked_targets, outputs2=None):
        return self.loss_func(outputs, stacked_targets, outputs2=outputs2)


class _IntraBatchMixupLoss():
    """Loss wrapper for Mixup.

    Notes:
        For use with IntraBatchMixup only, targets need to be stacked by the class.
        Criterion cannot be reused; `reduction` attribute will be overwritten in this class.
    """

    def __init__(self, criterion):
        assert hasattr(criterion, 'reduction'), 'Need usual loss function that have attr "reduction".'
        assert criterion.reduction != 'none', 'Cannot reuse loss function, re-instantiate pls.'
        # replace criterion's `reduction` with `none`, and keep the original setting.
        self.criterion = criterion
        self.reduction = criterion.reduction
        setattr(self.criterion, 'reduction', 'none')

    def __call__(self, outputs, stacked_targets, outputs2=None):
        org_targets, counter_targets, lambd = stacked_targets
        loss1 = self.criterion(outputs, org_targets.long())
        loss2 = self.criterion(outputs if outputs2 is None else outputs2, counter_targets.long())
        in_shape = [lambd.size(0)] + [1 for _ in range(len(outputs.shape) - 1)]
        lambd = lambd.view(in_shape)
        d = loss1 * lambd + loss2 * (1-lambd)
        if self.reduction == 'mean':    return d.mean()
        elif self.reduction == 'sum':   return d.sum()
        return d


def torch_show_trainable(model):
    """
    Print 'Trainable' or 'Frozen' for all elements in a model.
    Thanks to https://discuss.pytorch.org/t/how-the-pytorch-freeze-network-in-some-layers-only-the-rest-of-the-training/7088/15
    """
    for name, child in model.named_children():
        for param in child.parameters():
            print('Trainable' if param.requires_grad else 'Frozen', '@', str(child).replace('\n', '')[:80])
        torch_show_trainable(child)


def torch_set_trainable(model, flag):
    for param in model.parameters():
        param.requires_grad = flag


def to_raw_image(torch_img, uint8=False, denorm=True):
    """Convert image tensor to numpy array.

    Args:
        torch_img (torch.Tensor): Image or batch of images to convert.
            NCHW, CHW, or HW formats are acceptable.
        uint8: If True, multiply 255 and convert to uint8.
        denorm: If True, de-normalize by fixed (mean, std) = (0.5, 0.5).

    Returns:
        Converted numpy array image.
    """

    # transpose channels.
    if len(torch_img.shape) == 4: # batch color image N,C,H,W
        img = torch_img.permute(0, 2, 3, 1)
    elif len(torch_img.shape) == 3: # one color image C,H,W
        img = torch_img.permute(1, 2, 0)
    elif len(torch_img.shape) == 2: # one mono image H,W
        img = torch_img
    else:
        raise ValueError(f'image has wrong shape: {len(torch_img.shape)}')
    # single channel mono image (H,W,1) to be (H,W).
    if img.shape[-1] == 1:
        img = img.view(img.shape[:-1])
    # send to the earth, and denorm.
    img = img.detach().cpu().numpy()
    if denorm:
        img = img * 0.5 + 0.5
    if uint8:
        img = (img * 255).astype(np.uint8)
    return img
