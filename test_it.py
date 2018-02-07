import os
import unittest

import pydffi

_HERE = os.path.dirname(os.path.abspath(__file__))
_THERE = os.path.abspath(os.path.join(_HERE, '../tis-104-real'))


class TIS:
    def __init__(self):
        pydffi.dlopen(_THERE + '/build/pc/tis104.so')
        self.FFI = pydffi.FFI()
        self.CU = self.FFI.cdef('''
#include "{0}/src/cpu.h"
#include "{0}/src/pipe_mock.h"
'''.format(_THERE))

    @property
    def NOOP(self):
        return self.CU.types.instr_t(op=self.CU.types.op_t.OP_NOP, 
                                     arg1=self.CU.types.arg_t.ARG_NONE, 
                                     arg2=self.CU.types.arg_t.ARG_NONE)

    @property
    def INCR(self):
       return self.CU.types.instr_t(op=self.CU.types.op_t.OP_ADD, 
                                    arg1=1, 
                                    arg2=self.CU.types.arg_t.ARG_NONE) 

    def program(self, instrs):
        instrArrayTy = self.FFI.arrayType(self.CU.types.instr_t, 15) 
        instrArr = pydffi.CArrayObj(instrArrayTy)

        for idx, instr in enumerate(instrs):
            instrArr.set(idx, instr)
        return self.CU.types.prgm_t(length=len(instrs), instrs=instrArr)


#@unittest.skip
class TestTIS104Real(unittest.TestCase):
    def test_it(self):
        tis = TIS()
        CU = tis.CU
        FFI = tis.FFI

        cpu = CU.types.cpu_t()
        
        prgm = tis.program([tis.INCR, tis.NOOP, tis.INCR, tis.NOOP])

        state = CU.types.state_t()
        CU.funcs.cpu_state_init(FFI.ptr(state))
        
        pipeArrTy = FFI.arrayType(CU.types.pipe_t, 4)

        inputArr = pydffi.CArrayObj(pipeArrTy)
        outputArr = pydffi.CArrayObj(pipeArrTy)
        for i in range(4):
            inputArr.set(i, CU.types.pipe_t())
            outputArr.set(i, CU.types.pipe_t())

        #(struct cpu_t *cpu, struct prgm_t *prgm, struct state_t *state, struct pipe_t *inputs[], struct pipe_t *outputs[]);
        CU.funcs.cpu_init(FFI.ptr(cpu), FFI.ptr(prgm), FFI.ptr(state), FFI.ptr(inputArr), FFI.ptr(outputArr))

        def p_cpu():
            print("PC: ", state.pc)
            print("ACC:", state.acc)
            print("BAK:", state.bak)
            print("RX: ", state.rx)
            print("TX:", state.tx)

        p_cpu()
        CU.funcs.cpu_step(FFI.ptr(cpu)) 
        p_cpu()
        CU.funcs.cpu_step(FFI.ptr(cpu))
        p_cpu()
        CU.funcs.cpu_step(FFI.ptr(cpu))
        p_cpu()
        CU.funcs.cpu_step(FFI.ptr(cpu))
        p_cpu()

@unittest.skip
class TestCFFI(unittest.TestCase):
    def test_it(self):
        pydffi.dlopen(_HERE + '/library.so')
        FFI = pydffi.FFI()
        CU = FFI.cdef('#include "{}/library.h"'.format(_HERE))

        foo = CU.types.Foo_s(bar=1)
        CU.funcs.by_ptr(FFI.ptr(foo))
        self.assertEqual(foo.bar, 2)

if __name__ == '__main__':
    unittest.main()