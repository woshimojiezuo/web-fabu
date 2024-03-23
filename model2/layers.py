import torch.nn as nn
import torch
class Ms(nn.Module):
    def __init__(self, in_channel, out_channel, stride=1, padding=0, activate ='relu'):
        super(Ms, self).__init__()
        self.in_channel = in_channel
        self.out_channel = out_channel
        self.stride = stride
        self.padding = padding
        #self.kernel_size = kernel_size
        self.activate_func = nn.ReLU(inplace=True) if activate=='relu' else nn.Sigmoid()
        self.conv1 = nn.Sequential(nn.Conv2d(in_channel,in_channel,kernel_size=3,stride=1,padding=1),
                                   nn.BatchNorm2d(self.in_channel),
                                   self.activate_func
                                    )
        self.conv11 = nn.Sequential(nn.Conv2d(self.in_channel*4, self.out_channel, kernel_size=1, stride=1, padding=0),
                                   nn.BatchNorm2d(self.out_channel),
                                   self.activate_func
                                    )
    def forward(self, inputs):
        con1 = self.conv1(inputs)
        con2 = self.conv1(con1)
        con3 = self.conv1(con2)
        cat = torch.cat((con1,con2,con3,inputs),1)
        result = self.conv11(cat)
        return result

class Transconv(nn.Module):
    def __init__(self, in_channel, out_channel, kernel_size=2, stride=2, padding=0, activate='relu'):
        super(Transconv, self).__init__()
        self.in_channel = in_channel
        self.out_channel = out_channel
        self.stride = stride
        self.padding = padding
        self.kernel_size = kernel_size
        self.activate_func = nn.ReLU(inplace=True) if activate == 'relu' else nn.Sigmoid()
        self.transconv = nn.Sequential(nn.ConvTranspose2d(in_channel, out_channel, kernel_size=self.kernel_size, stride=self.stride, padding=self.padding),
                                   nn.BatchNorm2d(self.out_channel),
                                   self.activate_func
                                   )

    def forward(self, inputs):
        trans = self.transconv(inputs)
        return trans



class Conv11(nn.Module):
    def __init__(self, in_channel, out_channel, kernel_size=1, stride=1, padding=0, activate='relu'):
        super(Conv11, self).__init__()
        self.in_channel = in_channel
        self.out_channel = out_channel
        self.stride = stride
        self.padding = padding
        self.kernel_size = kernel_size
        self.activate_func = nn.ReLU(inplace=True) if activate == 'relu' else nn.Sigmoid()
        self.con = nn.Sequential(
            nn.Conv2d(in_channel, out_channel, kernel_size=self.kernel_size, stride=self.stride,
                               padding=self.padding),
            nn.BatchNorm2d(self.out_channel),
            self.activate_func
            )

    def forward(self, inputs):
        con = self.con(inputs)
        return con

if __name__ == '__main__':
    a = Ms(4,64,3,1,0).cuda()
    #a = Transconv(4, 4,).cuda()
    t = torch.randn((1, 4, 64, 64)).cuda()
    #a2 = Conv11(4, 12, ).cuda()
    z = a(t)
    print(z)