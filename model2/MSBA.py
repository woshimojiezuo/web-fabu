from model2.layers import *


class Msba(nn.Module):
    def __init__(self,in_channels=1):
        super(Msba,self).__init__()
        self.in_channels = in_channels

        filters = [64, 128, 256, 512]
        #下采样
        self.maxpool = nn.MaxPool2d(kernel_size=2)
        self.ms1 = Ms(self.in_channels,filters[0],)
        self.ms2 = Ms(filters[0], filters[1], )
        self.ms3 = Ms(filters[1], filters[2], )
        self.ms4 = Ms(filters[2], filters[3], )
        # 上采样
        self.transconv1 = Transconv(filters[3],filters[2],kernel_size=2, stride=2)
        self.transconv2 = Transconv(filters[2], filters[1], kernel_size=2, stride=2)
        self.transconv3 = Transconv(filters[1], filters[0], kernel_size=2, stride=2)
        self.ms5 = Ms(filters[2], filters[2], )
        #self.ms5 = Ms(filters[3], filters[2],)
        self.ms6 = Ms(filters[1], filters[1], )
        #self.ms6 = Ms(filters[2], filters[1],)
        self.ms7 = Ms(filters[0], filters[0], )
        #self.ms7 = Ms(filters[1], filters[0],)

        self.final_b=Conv11(filters[0],1,activate='sigmoid')
        self.final_r=Conv11(filters[0],1,activate='sigmoid')

    def forward(self, inputs):
        #主干部分
        ms1 = self.ms1(inputs)
        max1 = self.maxpool(ms1)
        ms2 = self.ms2(max1)
        max2 = self.maxpool(ms2)
        ms3 = self.ms3(max2)
        max3 = self.maxpool(ms3)
        ms4 = self.ms4(max3)

        transconv1 = self.transconv1(ms4)
        cat1 = transconv1 + ms3
        #cat1 = torch.cat((transconv1,ms3,),1)
        ms5 = self.ms5(cat1)

        transconv2 = self.transconv2(ms5)
        cat2 = transconv2 + ms2
        #cat2 = torch.cat((transconv2, ms2,), 1)
        ms6 = self.ms6(cat2)

        transconv3 = self.transconv3(ms6)
        cat3 = transconv3 + ms1
        #cat3 = torch.cat((transconv3, ms1,), 1)
        ms7 = self.ms7(cat3)

        final_b = self.final_b(ms7)
        final_r = self.final_r(ms7)

        return final_b,final_r


if __name__=='__main__':
    a = Msba().cuda()
    t = torch.randn((1, 1, 512, 512)).cuda()
    z=a(t)
    print(z)