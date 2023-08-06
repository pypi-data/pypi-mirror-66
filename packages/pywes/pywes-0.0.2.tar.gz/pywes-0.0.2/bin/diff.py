#!/usr/bin/env python3
#coding:utf-8

import sys

def diff(test,correct):
    try:
        test_lines = open(test).readlines()
        correct_lines = open(correct).readlines()
        for test, correct in zip(test_lines, correct_lines):
            if test != correct:
                print ("Oh no! Expected %r; got %r." % (correct, test))
                break
            else:
                len_diff = len(test_lines) - len(correct_lines)
                if len_diff > 0:
                    print ("Test file had too much data.")
                elif len_diff < 0:
                    print ("Test file had too little data.")
                else:
                    print ("Everything was correct!")
    except IOError:
        print('file does not exist')
        sys.exit()

if __name__ == '__main__':
    test,correct=sys.argv[1],sys.argv[2]
    diff(test,correct)