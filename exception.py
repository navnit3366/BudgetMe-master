class TypeException:
    def int_type_exception(self, x):
        assert(type(x) == int), "value must be {}- recieved {} program haulting.".format(int, type(x))
    def float_type_exception(self, x):
        assert(type(x) == float), "value must be {}- recieved {} program haulting.".format(float, type(x))
    def str_type_exception(self, x):
        assert(type(x) == str), "value must be {}- recieved {} program haulting.".format(str, type(x))

    def int_except_output(self):
        print("TypeException: input type not valid, needs {}".format(int))
    def float_except_output(self):
        print("TypeException: input type not valid, needs {}".format(float))
    def str_except_output(self):
        print("TypeException: input type not valid, needs {}".format(str))