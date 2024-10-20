import argparse
from time import sleep

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-freq',dest='frequency')
    args=parser.parse_args()
    freq=int(args.frequency)
    while True:
        sleep(freq)
        print(f'waited {freq} seconds')