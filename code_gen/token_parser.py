

class Token:
    IDENTIFIER = 'IDENTIFIER'
    NUMBERAL = 'NUMBERAL'
    ASSIGNMENT = 'ASSIGNMENT'
    OPERATOR = 'OPERATOR'
    END_STATEMENT = 'END_STATEMENT'
    
    def __init__(self,label:str,type:str):
        self.label = label
        self.type = type
    @classmethod
    def fromFlex(cls,text:str):
        text = text[1:-2]
        _type, label = text.split(',',1)
        return cls(label,_type)
        

def token2statement(lines:list[str]):
    tokens = list(map(lambda line: Token.fromFlex(line), lines))
    
    for token in tokens:
        