import multiprocessing
#manager = multiprocessing.Manager()


def ciklus(result):
    while True:
        result.value = result.value + 5

if __name__ == '__main__':
    v = multiprocessing.Value('d', 0.0)
    p = multiprocessing.Process(target=ciklus, args = [v])

    p.start()
    while True:
        print (v.value)