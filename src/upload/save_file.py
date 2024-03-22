import os
cont = 0
def data_root():
    global cont 
    cont = cont + 1
    return os.path.join(
        os.path.split(__file__)[0],
        f'arhivo{cont}.xlsx')