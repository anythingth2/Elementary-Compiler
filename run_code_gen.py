from code_gen import code_generator, expression, data_type
x = data_type.DataType('chichachai', data_type.DataType.db)
y = data_type.DataType('chichachEYASDADai', data_type.DataType.db)

generator = code_generator.CodeGenerator(
    [expression.DefineInitailizedVariable(x, data_type.StringImmediateValue('YEA\nG')),
     expression.DefineInitailizedVariable(y, data_type.StringImmediateValue('YEf\nsfsAG\n')),
        expression.printText(x)])
generator.generate()
