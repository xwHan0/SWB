from model.module import module

class Memory(module):
    def __init__(self, size, depth, name= '', **options):
        """Memory模型
        
        Arguments:
            module {[type]} -- [description]
            size {int} -- 位宽
            depth {int} -- 深度
        """
        super().__init__(name)
        self.size = size
        self.depth = depth
        self.opts = options

    def width(self):
        return self.size

    def _registers_(self):
        regs = 0
        regs += self.width() if self.opts.get('I1',True) else 0
        regs += self.width() if self.opts.get('O1',True) else 0
        return regs

    def _memory_(self): return self.size * self.depth

    def _toggle_rate_(self):
        w_regs = self.width() if self.opts.get('I1',True) else 0
        r_regs = self.width() if self.opts.get('O1',True) else 0
        w_rate = self.opts.get('wrate', 1.0)
        r_rate = self.opts.get('rrate', 1.0)
        return (w_rate * w_regs + r_rate * r_regs) / (w_regs + r_regs)

