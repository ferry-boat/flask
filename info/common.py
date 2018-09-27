# 过滤器的本质就是函数
def func_index_convert(index):
    index_dict = {1: "first", 2: "second", 3: "third"}
    return index_dict.get(index, "")