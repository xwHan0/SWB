from model.module import module
from model.utils import cal_mux_num

from math import ceil


class Crossbar(module):
    def __init__(self, inum, onum, name='', **options):
        """输出类型Crossbar模型
        
        Arguments:
            inum {int} -- XB的输入端口个数。若打平到channel，则每个channel都算一个
            onum {int} -- XB的输出端口个数。
        
        Keyword Arguments:
            typ {str = 'OXB'} -- 'IXB' | 'OXB'
            step {int = 1} -- 每隔多少个沟道打一拍
            shift {int = 0} -- 是否需要数据位宽内移位个数。MUX选择个数
            bits {int = 1} -- 位宽
        """
        super().__init__(name)
        self.inum = inum
        self.onum = onum
        self.opts = options


    def _registers_(self):
        if self.opts.get('typ', 'OXB') == 'OXB':
            regs = self.inum    # 每个沟道内部的2个Bank之间2选1
            regs += self.onum * ceil(self.inum/self.opts.get('step',1))     #每隔step个沟道打onum个寄存器
            regs += self.onum if self.opts.get('shift',0)!=0 else 0
        else:
            regs = self.onum    # 每个沟道内部选择完成后打1拍
            regs += self.inum * ceil(self.onum/self.opts.get('step',1))     #每隔step个沟道打onum个寄存器
            regs += self.inum if self.opts.get('shift',0)!=0 else 0
        return regs * self.opts.get('bits',1)

    def _nandor_(self):
        if self.opts.get('typ', 'OXB') == 'OXB':
            rst = self.onum * self.inum * 2     #每个输出一个与门和一个或门
        else:
            rst = 0
        return rst * self.opts.get('bits',1)

    def _mux_(self):
        if self.opts.get('typ', 'OXB') == 'OXB':
            rst = self.inum  # 每个沟道内部的2个Bank之间2选1
            rst += cal_mux_num(self.opts.get('shift',0)) * self.onum
        else:
            rst = cal_mux_num(self.inum) * self.onum
            rst += cal_mux_num(self.opts.get('shift',0)) * self.inum
        return rst * self.opts.get('bits',1)

    def _toggle_rate_(self):
        return self.opts.get('rate',1)

        
from model.mem import Memory

class OBFFullShared(module):
    def __init__(self, W, M, S):
        super().__init__('FullShared')

        self.W = W
        self.M = M
        self.S = S

        self.append( Crossbar(M/2*3,M/2,'oPreLoop', bits=S, rate=0.5) )
        self.append( Crossbar(M/2,M*3,'iPreLoop', shift=1, typ='IXB', bits=S, rate=0.5) )
        self.append( Crossbar(M*3,M,'oPostLoop', bits=S, rate=0.5) )
        self.append( Crossbar(M/2,M/2*3, 'iPostLoop', shift=1, bits=S, typ='IXB', rate=0.5), 2 )
        self.append( Memory(S, 8, 'DataMemory', I1=True, O1=True, wrate=0.25, rrate=0.25), M*6 )


    def _registers_(self):
        # Input打拍
        regs = self.S * (self.M/2 + self.M/4)
        regs += self.S * self.M / 2
        return regs


class OBFSeprated(module):
    def __init__(self, W, M, S):
        super().__init__('FullShared')

        self.W = W
        self.M = M
        self.S = S

        self.append( Crossbar(M/2*3,M/2,'oPreLoop', bits=S) )
        self.append( Crossbar(M/2,M/2*3,'iPreLoop', shift=1, typ='IXB', bits=S) )
        self.append( Crossbar(M/2*3,M/2,'oPostLoop', bits=S),2 )
        self.append( Crossbar(M/2,M/2*3, 'iPostLoop', shift=1, bits=S, typ='IXB'), 1 )
        self.append( Crossbar(M,M/2*3, 'iPostLoop', shift=1, bits=S, typ='IXB'), 1 )
        self.append( Memory(S, 8, 'DataMemory', I1=True, O1=True), M*6 )


    def _registers_(self):
        # Input打拍
        regs = self.S * (self.M/2 + self.M/4)
        regs += self.S * self.M / 2
        return regs