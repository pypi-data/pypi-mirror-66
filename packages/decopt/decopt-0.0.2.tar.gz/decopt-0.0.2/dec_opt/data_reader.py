class DataReader:
    def __init__(self, data_set:str = 'mnist'):
        self.data_set = data_set

    def _get_data(self):
        raise NotImplementedError
