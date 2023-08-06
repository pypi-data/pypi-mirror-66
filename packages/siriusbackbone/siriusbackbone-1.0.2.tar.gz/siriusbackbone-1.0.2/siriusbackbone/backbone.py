import torch
import torch.nn as nn
import torchvision.models._utils as mutils
import torchvision.models as pretrains



class BackBone(nn.Module):
    def __init__(self, net, maps, return_layers, pretrained=False):
        super().__init__()
        self.net = getattr(pretrains, net)(pretrained=pretrained)
        self.backbone = mutils.IntermediateLayerGetter(self.net, maps)
        self.return_layers = return_layers

    def forward(self, x):
        res = self.backbone(x)
        res = list(map(lambda key: res[key], self.return_layers))
        return res


def mobilenet_v2(pretrained=False):
    return BackBone('mobilenet_v2', {'features': 'backbone'}, ['backbone'], pretrained=pretrained)

def mobilenet(pretrained=False):
    return BackBone('mobilenet', {'features': 'backbone'}, ['backbone'], pretrained=pretrained)

ResnetMaps = { 'layer1': 'layer1', 'layer2': 'layer2', 'layer3': 'layer3', 'layer4': 'layer4'}


def resnet18(return_layers, pretrained=False):
    return BackBone('resnet18', ResnetMaps, return_layers, pretrained=pretrained)

def resnet34(return_layers, pretrained=False):
    return BackBone('resnet34', ResnetMaps, return_layers, pretrained=pretrained)

def resnet50(return_layers, pretrained=False):
    return BackBone('resnet50', ResnetMaps, return_layers, pretrained=pretrained)

def resnet101(return_layers, pretrained=False):
    return BackBone('resnet101', ResnetMaps, return_layers, pretrained=pretrained)


if __name__ == '__main__':
    x = torch.randn(1, 3, 800, 800)
    net = resnet18(['layer1', 'layer2'])
    with torch.no_grad():
        res = net(x)
    for r in res:
        print(r.shape)

    x = torch.randn(1, 3, 128, 128)
    net = mobilenet_v2()
    with torch.no_grad():
        res = net(x)
    for r in res:
        print(r.shape)
