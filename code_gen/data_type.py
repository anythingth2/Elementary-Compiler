class ImmediateValue:
    def eval(self):
        pass

class StringImmediateValue(ImmediateValue):
    def __init__(self,value:str):
        self.value = value
    def eval(self):
        return '"' + self.value.replace('\n', '", 10,"')+ '"'

class DataType:
    db = 'db'
    dw = 'dw'
    dd = 'dd'

    def __init__(self, label: str, size: str):
        self.label = label
        self.size = size

