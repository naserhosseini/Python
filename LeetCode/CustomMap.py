import os

from distlib.compat import raw_input


def cmap(funcs, arr):
    # Write your code here
    res = [eval(i) for i in arr]
    func = [eval(i) for i in funcs]
    out1 = list(map(func[0], res))
    out2 = list(map(func[1], out1))
    print(out2)

if __name__ == '__main__':


    result = cmap(['lambda x: x*x', 'lambda x: x+x'], ['1', '2', '3', '4'])
