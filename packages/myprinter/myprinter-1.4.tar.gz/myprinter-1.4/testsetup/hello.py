#!/usr/bin/env python3
import os

from testsetup.utilts import Printer


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIR = os.path.join(CURRENT_DIR, 'config')

def main():
    print('I will print the config/t.json.')
    p = Printer()
    json_file = os.path.join(CONFIG_DIR, 't.json')
    with open(json_file, 'r') as f:
        l = f.readlines()
        p.echo(l)

if __name__ == '__main__':
    main()




