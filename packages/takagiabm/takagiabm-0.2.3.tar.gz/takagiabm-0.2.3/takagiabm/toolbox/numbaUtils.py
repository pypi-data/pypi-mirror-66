
def fakeJit(func):  # 不带jit的时候,

    def wrapper(*args):
        result = func(*args)
        return result

    return func