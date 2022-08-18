import unittest as ut
from Orchestrator.BatchStates import BatchStates


class TestBatchStates(ut.TestCase):
    def setUp(self) -> None:
        self.__batch_state = BatchStates()

    def testResetStates(self):
        self.__batch_state.resetStates()
        expected = 0
        result = self.__batch_state.getPendingBatchCount()
        self.assertEqual(expected, result, "Test-1 Failed")  # add assertion here

    def testInitStates(self):
        self.__batch_state.initStates(batch_list=[1, 2, 3, 4, 5])
        expected = 0
        result = self.__batch_state.getPendingBatchCount()
        self.assertEqual(expected, result, "Test-2 Failed")  # add assertion here

    def testSetBatchState(self):
        self.__batch_state.initStates(batch_list=[1, 2, 3, 4, 5])
        self.__batch_state.setBatchState(1, True)
        self.__batch_state.setBatchState(2, True)
        expected = 3
        result = self.__batch_state.getPendingBatchCount()
        self.assertEqual(expected, result, "Test-2 Failed")  # add assertion here


if __name__ == '__main__':
    ut.main()
