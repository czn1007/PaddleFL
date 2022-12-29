import unittest
from multiprocessing import Manager
import numpy as np
import paddle.fluid as fluid
import paddle_fl.mpc as pfl_mpc
import test_op_base
from paddle_fl.mpc.data_utils.data_utils import get_datautils

aby3 = get_datautils('aby3')

class TestOpMul3_C0(test_op_base.TestOpBase):

    def mul3_C0(self, **kwargs):

        role = 0
        num = 100
        d_1 = np.load('data_C0_P0.npy',allow_pickle=True)
        d_2 = np.load('data_C0_P1.npy',allow_pickle=True)
        d_3 = np.load('data_C0_P2.npy', allow_pickle=True)

        pfl_mpc.init("aby3", role, "localhost", self.server, int(self.port))
        x = pfl_mpc.data(name='x', shape=[num], dtype='int64')
        y = pfl_mpc.data(name='y', shape=[num], dtype='int64')
        # math_mul = x * y
        math_mul = pfl_mpc.layers.elementwise_mul(x, y)
        exe = fluid.Executor(place=fluid.CPUPlace())
        results = exe.run(feed={'x': d_1, 'y': d_2}, fetch_list=[math_mul])
        results = exe.run(feed={'x': d_3, 'y': results[0]}, fetch_list=[math_mul])
        np.save('result_C0.npy', results[0])

    def test_mul3_C0(self):
        ret = self.multi_party_run0(target=self.mul3_C0)

if __name__ == '__main__':
    unittest.main()