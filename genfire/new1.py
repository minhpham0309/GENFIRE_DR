try:
    my_variable
except NameError as e:
    print(str(e))
    my_variable = 10;
    print(my_variable)	
else:
    print(my_variable)
    