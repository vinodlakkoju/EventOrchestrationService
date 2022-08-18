from typing import List


class BatchStates:
    def __init__(self):
        self.__batch_count = 0
        self.__batch_states = {}

    def resetStates(self):
        self.__batch_count = 0
        self.__batch_states = {}

    def initStates(self, batch_list: List):
        for item in batch_list:
            self.__batch_states[f'batch-{item}'] = False

    def setBatchState(self, batch_id: int, state: bool):
        self.__batch_states[f'batch-{batch_id}'] = state

    def getPendingBatchCount(self):
        count = 0
        for key, value in self.__batch_states.items():
            if not value:
                count += 1
        return count
