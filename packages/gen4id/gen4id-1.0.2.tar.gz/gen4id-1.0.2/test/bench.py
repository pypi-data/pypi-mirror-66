from gen4id.increase_gen import MIXED
from gen4id import IncreaseGen, random_str


def bench_sync():
    ic = IncreaseGen(key_len=8, choose=random_str(MIXED))
    d = dict()
    for i in range(1000000):
        code = ic.encode(i)
        if d.get(code) is not None:
            print(f"duplicate key found, id is {i}, code is {code}")
            break
        print(f"id number : {i}, the code is {code}")
        d[code] = i
    # print(ic.encode(1))

if __name__ == '__main__':
    bench_sync()
