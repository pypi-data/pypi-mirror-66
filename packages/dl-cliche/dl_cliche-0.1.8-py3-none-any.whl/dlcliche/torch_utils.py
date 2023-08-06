from .utils import *
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
