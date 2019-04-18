from code_gen import code_generator, expression, data_type
generator = code_generator.CodeGenerator(
    [expression.DefineInitailizedVariable(data_type.DataType('chichachai', data_type.DataType.db), data_type.StringImmediateValue('YEAG')),
     expression.DefineUninitailizedVariable(data_type.DataType('chichachEYASDADai', data_type.DataType.db), data_type.StringImmediateValue('YEfsfsAG'))])
generator.generate()
