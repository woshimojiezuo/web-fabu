import torch
from torch.utils.data import Dataset, DataLoader
import os
import numpy as np
import torchvision
from torchvision.io import image
from PIL import Image,ImageDraw
from torchvision import transforms

# 自定义Dataset的基本模板
class MyDataset(Dataset):  # 自定义一个类
    def __init__(self, imgdir, labeldir1,labeldir2, transform=None):  # 初始化，把数据作为一个参数传递给类；
        self.transform = transform
        self.imgdir = imgdir
        self.labeldir1 = labeldir1
        self.labeldir2 = labeldir2
        self.get_filelist()
    def get_filelist(self):
        filelist = os.listdir(self.imgdir)
        labellist1 = os.listdir(self.labeldir1)
        labellist2 = os.listdir(self.labeldir2)
        a = []
        for file in filelist:
            name = os.path.basename(file)
            name, _ = os.path.splitext(name)
            for i in labellist1:
                if name in i:
                    abdir_file = os.path.join(self.imgdir,file)
                    abdir_label1 = os.path.join(self.labeldir1, i)
                    abdir_label2 = os.path.join(self.labeldir2, i)
                    a.append([abdir_file,abdir_label1,abdir_label2])
        self.data = a
        # image_filelist = [os.path.join(self.imgdir,x) for x in filelist]
        # label_filelist = [os.path.join(self.labeldir, x) for x in labellist]
        # data = [[x, y] for x, y in zip(image_filelist,label_filelist)]
        # #self.data = data
    def get_tensor(self,imgdir,labeldir1,labeldir2):
        img = Image.open(imgdir)
        img = img.convert('L')
        img = np.array(img)
        img = torch.tensor(img)
        img = img.unsqueeze(0)

        label1 = Image.open(labeldir1)
        label1 = label1.convert('L')
        label1 = np.array(label1)
        label1 = torch.tensor(label1)
        label1 = label1.unsqueeze(0)

        label2 = Image.open(labeldir2)
        label2 = label2.convert('L')
        label2 = np.array(label2)
        label2 = torch.tensor(label2)
        label2 = label2.unsqueeze(0)

        IMG_LA = torch.cat((img, label1, label2), 0)
        IMG_LA = IMG_LA.type(torch.float32)
        if self.transform is not None:
            IMG_LA = self.transform(IMG_LA)/255
        i_l_list = torch.chunk(IMG_LA, 3, 0)
        inputs = i_l_list[0]
        labels1 = i_l_list[1]
        labels2 = i_l_list[2]
        return inputs.type(torch.float32).cuda(),labels1.type(torch.float32).cuda(),labels2.type(torch.float32).cuda()
    def __len__(self):
        return len(self.data)  # 返回数据的长度

    def __getitem__(self, idx):
        dir = self.data[idx]
        image,label1,label2 = self.get_tensor(dir[0],dir[1],dir[2])
        return image, label1,label2
    # return self.data[idx]  #根据索引返回数据

class Mytest(Dataset):  # 自定义一个类
    def __init__(self, data_testdir,transform=None):  # 初始化，把数据作为一个参数传递给类；
        self.cuda = torch.cuda.is_available()
        self.data_testdir = data_testdir
        self.get_filelist()
        self.transform = transform
    def get_filelist(self):
        filelist = os.listdir(self.data_testdir)
        image_filelist = [os.path.join(self.data_testdir,x) for x in filelist]
        self.img_test = image_filelist
    def get_tensor(self,dir):
        img = Image.open(dir)
        img = img.convert('L')
        img = np.array(img)
        img = torch.tensor(img)/255
        img = img.unsqueeze(0)
        if self.transform is not None:
            img = self.transform(img)
        if self.cuda:
            img = img.type(torch.float32).cuda()
        else:
            img = img.type(torch.float32)
        return img
    def __len__(self):
        return len(self.img_test)  # 返回数据的长度

    def __getitem__(self, idx):
        dir = self.img_test[idx]
        image = self.get_tensor(dir)
        return image,dir
    # return self.data[idx]  #根据索引返回数据

def backimg(tensor,noraml = True,threshold=0):
    if noraml:
        tensor = (tensor*0.229+0.5)*255
    else:
        tensor = tensor*255
    #tensor = torchvision.transforms.Resize(512)(tensor)
    # torch.where(tensor < 0, 0, tensor)
    if threshold:
        tensor = torch.where(tensor < 255*threshold, 255, 0)
    # torch.where(tensor > 255, 255, tensor)
    #tensor = torch.where(tensor < 150, 0, 255)
    #tensor = torch.where(tensor >= 120, 255, tensor)
    tensor = tensor.squeeze(0)
    tensor = tensor.permute(1, 2, 0)
    tensor = tensor.cpu()
    array = tensor.detach().numpy()
    array = np.uint8(array)
    return array

def tensor_show(tensor):
    tensor = tensor.squeeze(0)
    tensor = tensor.permute(1, 2, 0)
    array = tensor.cpu().detach().numpy()
    array = np.uint8(array)
    im = Image.fromarray(array[:, :, 0])
    im.show()


class Mytest_for_uploadfile(Dataset):  # 自定义一个类
    def __init__(self, uploadfile:list,transform=None):  # 初始化，把数据作为一个参数传递给类；
        self.cuda = torch.cuda.is_available()
        self.uploadfile = uploadfile
        self.transform = transform
    def get_tensor(self,upload):
        img = Image.open(upload)
        img = img.convert('L')
        img = np.array(img)
        img = torch.tensor(img)/255
        img = img.unsqueeze(0)
        if self.transform is not None:
            img = self.transform(img)
        if self.cuda:
            img = img.type(torch.float32).cuda()
        else:
            img = img.type(torch.float32)
        return img
    def __len__(self):
        return len(self.uploadfile)  # 返回数据的长度
    def __getitem__(self, idx):
        upload = self.uploadfile[idx]
        image = self.get_tensor(upload)
        return image,upload.name


if __name__ == '__main__':
    from torchvision import transforms
    import numpy as np

    data_transform = transforms.Compose(
        [transforms.RandomRotation(30),
         transforms.RandomCrop(512),
         transforms.RandomHorizontalFlip(0.5),
         transforms.RandomVerticalFlip(0.5),
         transforms.Resize(512), ])
    # transforms.Normalize(0.5, 0.229)])

    DATA = MyDataset(imgdir='../data/rock/image',
                     labeldir1='../data/rock/label',
                     labeldir2='../data/rock/label3',
                     transform=data_transform)

    data_loader = DataLoader(DATA, batch_size=1, shuffle=True)
    for step,data in enumerate(data_loader):
        inputs = data[0]
        labels1 = data[1]
        labels2 = data[2]
        tensor_show(inputs * 255)
        tensor_show(labels1 * 255)
        tensor_show(labels2 * 255)
    def count_mean_std():
        pass
