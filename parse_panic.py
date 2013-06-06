#!/usr/bin/env python

import re
import sys
from os import system


def isReg(maybe_reg):
    return maybe_reg.lower() in isReg.registers
isReg.registers=(
        'pc', 'lr', 'psr', 'sp', 'ip', 'fp', 
        'r10', 'r9', 'r8', 'r7', 'r6', 'r5', 
        'r4', 'r3', 'r2', 'r1', 'r0',)

def main(queue):
    queue.reverse()
    current_reg = None
    current_offset = None
    outbytes = list()

    while 1:
        line = None
        try:
            line = queue.pop()
        except IndexError:
            break

        matches_dump = re.match('^\[.*\] (.*)  ([0-9a-fA-F ]+)\s*$', line)
        matches_new_reg = re.match('^\[.*\] (.*): (0x[0-9a-fA-F]+):\s*$',line)
        #                                    ^      ^
        #                                    |      |- (2) address
        #                                    |- (1) register
        if matches_new_reg:
            match = matches_new_reg
            if isReg(match.group(1)):
                reg = match.group(1)
                addr = match.group(2)
                current_reg = reg
                current_offset = addr

        elif matches_dump:
            outbytes.append( ''.join(matches_dump.group(2).split()))

    print "register %s starting @ address %s" % (reg, addr)
    sys.stdout.flush()
    system("rasm2 -e -a arm -o %s -D %s" % 
            (current_offset, ''.join(outbytes)))

def test():
    mystr="""foo
    [   95.487840] LR: 0xc03831b8:
    [   95.495002] 31b8  e3a03003 e5cb3001 e59f3260 e5933318 e5930010 e3500000 0a000001 e28b1002
    [   95.513405] 31d8  ebffcf05 e1a02005 e5b23024 e1520003 e243301c e58d201c 0a000019 e28ba002
    [   95.531806] 31f8  e1a09003 e5990004 e3500000 0a000001 e1a0100a ebffcef8 e1a08009 e5b83024
    [   95.551064] 3218  e1580003 e2436040 0a000008 e5960004 e1a0100a e3500000 0a000000 ebffceee
    [   95.569550] 3238  e5966040 e1580006 e2466040 1afffff6 e599901c e59d301c e1530009 e249901c
    [   95.588830] 3258  1affffe7 e3a03000 e08b2083 e5d21002 e5d22003 e1912402 1a000006 e3530000
    [   95.608072] 3278  0affff65 e2833001 e1a06083 e6ef6076 e5cb6000 eafffeed e2833001 e353007f
    [   95.627327] 3298  1afffff0 eafffff6 e59f2180 e5923364 e3530000 0a00003b e28d0030 e3a010ff
    """
    main(mystr)

if __name__ == "__main__":
    main(sys.stdin.readlines())
