from torchvision import models
from PIL import Image
import torch
import torchvision.transforms as T
import numpy as np

from aim import track
import aim

aim.init(True)

fcn = models.segmentation.fcn_resnet101(pretrained=True).eval()

img = Image.open('./data/bird.jpg')

trf = T.Compose([T.Resize(256),
                 T.CenterCrop(224),
                 T.ToTensor(),
                 ])
trf_norm = T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

inp = trf(img)
norm_inp = trf_norm(inp).unsqueeze(0)

out = fcn(norm_inp)['out']
om = torch.argmax(out.squeeze(), dim=0).detach().cpu().numpy()

aim_img = track(aim.image, inp)
labels = {
    0: 'background',
    1: 'aeroplane',
    2: 'bicycle',
    3: 'bird',
    4: 'boat',
    5: 'bottle',
    6: 'bus',
    7: 'car',
    8: 'cat',
    9: 'chair',
    10: 'cow',
    11: 'diningtable',
    12: 'dog',
    13: 'horse',
    14: 'motorbike',
    15: 'person',
    16: 'pottedplant',
    17: 'sheep',
    18: 'sofa',
    19: 'train',
    20: 'tvmonitor',
}

bad_om = om.copy()
bad_om[50:50, 50:50] = 0

better_om = om.copy()
better_om[20:20, 50:50] = 0

track(aim.segmentation, 'seg', aim_img, mask=bad_om.tolist(), class_labels=labels)
track(aim.segmentation, 'seg', aim_img, mask=better_om.tolist(), class_labels=labels)
track(aim.segmentation, 'seg', aim_img, mask=om.tolist(), class_labels=labels)
