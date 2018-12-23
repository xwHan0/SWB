
class module:
    def __init__(self, name=''):
        self.subs = []
        self.name = name

    def _registers_(self): return 0
    def _nandor_(self): return 0
    def _mux_(self): return 0
    def _gates_(self): return 0
    def _memory_(self): return 0
    def _toggle_rate_(self): return 1

    def append(self, mod, n=1):
        if isinstance(mod, module):
            self.subs.append( {'num':n, 'inst':mod} )
        else:
            raise Exception('Cannot cast object {0} to module.'.format(mod))

    def registers(self, inst_num=1):
        regs = [m.get('inst').registers(m.get('num',1)) for m in self.subs]
        regs = sum(iter(regs))
        return ( regs + self._registers_() ) * inst_num

    def memory(self, inst_num=1):
        mems = [m.get('inst').memory(m.get('num',1)) for m in self.subs]
        mems = sum(iter(mems))
        return ( mems + self._memory_() ) * inst_num

    def toggle_rate(self):
        regs = [m.get('inst').registers(m.get('num',1)) for m in self.subs] + [self._registers_()]
        rates = [m.get('inst').toggle_rate() for m in self.subs] + [self._toggle_rate_()]
        rate = sum( map(lambda x,y: x*y, regs, rates) ) / sum(iter(regs))
        return rate

