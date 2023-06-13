import numpy as np
import torch
from PIL import Image
from torch import nn
from torchvision import transforms
from efficientnet_pytorch.model import EfficientNet
from predict.nets.model_bira_net_resnet import BiraNet_ResNet
from predict.nets.model_ra import KeNet

cuda = False


class DO_net(object):
    def __init__(self):
        self.model = None

    def get_efficientnet(self, name, pretrained, model_path, num_classes):
        """Constructs a EfficientNetB5 model for FastAI.
        Args:
            pretrained (bool): If True, returns a model pre-trained on ImageNet
            :param num_classes: 分类的输出类别数
            :param name: efficientnet的名称b0---b8
            :param pretrained: True使用预训练网络，False不使用预训练
            :param model_path: 网络模型地址
            :return:    model
        """
        self.model = EfficientNet.from_name(f'efficientnet-{name}', num_classes=num_classes)
        if pretrained:
            model_state = torch.load(model_path)
            # load original weights apart from its head
            if '_fc.weight' in model_state.keys():
                model_state.pop('_fc.weight')
                model_state.pop('_fc.bias')
                res = self.model.load_state_dict(model_state, strict=False)
                print('Loaded pretrained')
                assert str(res.missing_keys) == str(['_fc.weight', '_fc.bias']), 'issue loading pretrained weights'
            else:
                # A basic remapping is required
                from collections import OrderedDict
                mapping = {i: o for i, o in zip(model_state.keys(), self.model.state_dict().keys())}
                mapped_model_state = OrderedDict([
                    (mapping[k], v) for k, v in model_state.items() if not mapping[k].startswith('_fc')
                ])
                res = self.model.load_state_dict(mapped_model_state, strict=False)
        return self.model

    def get_net(self, path):
        self.model = torch.load(path)
        return self.model

    def get_Kenet(self, path):
        self.model = KeNet(6, False)

        model_path = path
        model_state = torch.load(model_path)
        self.model.load_state_dict(model_state)

        return self.model

    def get_BIRA(self,path):
        self.model = BiraNet_ResNet(512, 6)

        model_path = path
        model_state = torch.load(model_path)
        self.model.load_state_dict(model_state)

        return self.model

    def predict(self, file_name):
        """
            predict the img at the filepath
        :param file_name: 图片名称
        :return: {'label':0-5(type=int),
                  'probability':(type=float),
                  'text':(type=str)
                  }
        """
        filepath = 'uploads/' + file_name

        img = Image.open(filepath)
        img = img.resize((256, 256), Image.BILINEAR)
        img = np.array(img)

        to_tensor = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
        ])
        img = to_tensor(img)
        img = torch.unsqueeze(img, 0)  # 给最高位添加一个维度，也就是batchsize的大小

        if cuda:
            img = img.cuda()

        self.model.eval()

        preds = self.model(img).detach().numpy()
        print(preds)

        label = int(np.argmax(preds))

        grading_list = ["无明显病变", "轻度非增殖期", "中度非增殖期", "重度非增殖期", "增殖期","高危增殖期"]

        result = {}
        key1 = 'label'
        key2 = 'probability'
        key3 = 'text'

        result.update({key1: grading_list[label]})  # 返回label

        # 计算指数值
        exp_values = np.exp(preds)
        # print(exp_values)

        # 对指数值进行归一化
        softmax_values = exp_values / np.sum(exp_values)
        # print(softmax_values)

        result.update({key2: softmax_values[0][label].astype(np.float64)})  # 返回置信度,感觉softmax不是很靠谱。。

        # 返回医疗建议
        suggest = ["无病变或正常视网膜表现。,建议进行定期眼睛检查以监测视网膜健康状况，并保持良好的眼睛卫生和健康生活方式。",
                   "微小病变，可能包括微血管瘤、硬性渗出等。在这种情况下，通常建议继续定期眼睛检查，并根据需要进行进一步的检查或治疗，以确保病变不进一步恶化。",
                   "中度病变，可能包括中等大小的血管瘤、出血或渗出。此时，可能需要更频繁的眼睛检查，并根据病情决定是否需要治疗，如激光光凝或注射药物。",
                   "严重病变，可能包括大型血管瘤、出血或渗出明显增多。在这种情况下，通常需要更加紧密的随访和治疗，以防止进一步视力损害。治疗可能包括激光光凝、注射药物或其他手术干预。",
                   "晚期病变，可能包括视网膜脱离或其他严重并发症。在这种情况下，可能需要紧急的眼科治疗，如手术修复视网膜脱离。"]
        result.update({key3: suggest[label]})  # 返回建议

        print(result)

        return result


if __name__ == '__main__':
    do_RA = DO_net()

    do_RA.get_Kenet('predict/models/train_all_epoch_017_acc_0.8661.pth')
    do_RA.predict('../static/label/007-0004-000.jpg')
