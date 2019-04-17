import abc

class Statement:

    @abc.abstractmethod
    def pre_define(self):
        pass
    
    @abc.abstractmethod
    def eval(self):
        pass
class printText(Statement):
    def __init__(self,text):
        self.text = text


    def eval(self):
        pass