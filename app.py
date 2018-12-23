
from model.mem import Memory
from model.obf import Crossbar, OBFFullShared, OBFSeprated

obf_f = OBFFullShared(4,8,2070)

regs = obf_f.registers(1)

print(regs)
print(obf_f.toggle_rate())

obf_s = OBFSeprated(4,8,2070)
print(obf_s.registers(1))