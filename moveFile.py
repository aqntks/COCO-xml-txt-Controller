import os
import argparse


def main(opt):
    i, fromP, toP, count = 0, opt.fromP, opt.toP, opt.count

    files = os.listdir(fromP)
    for file in files:
        if i >= count: break
        os.system('mv ' + file + ' ' + toP)
        i += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--fromP', type=str, default='')
    parser.add_argument('--toP', type=str, default='')
    parser.add_argument('--count', type=int, default=3)
    option = parser.parse_args()
    main(opt=option)