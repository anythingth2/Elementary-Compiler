from code_gen import code_generator, expression, data_type
x = data_type.DataType('chichachai', data_type.DataType.db)
y = data_type.DataType('chichachEYASDADai', data_type.DataType.db)

generator = code_generator.CodeGenerator('test_lang.token',)
generator.generate()
