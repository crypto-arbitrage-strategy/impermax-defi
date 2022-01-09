import multiprocessing as mp
import time


def timer(interval, name):
    while True:
        print(f"I'm {name} and I'm starting, time is the {time.time()}")
        time.sleep(interval)

def main():
    p1 = mp.Process(target=timer, args=(1, "p1"))
    p2 = mp.Process(target=timer, args=(2, "p2"))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print(f"I'm main and I'm done, time is the {time.time()}")

if __name__ == "__main__":
    main()
