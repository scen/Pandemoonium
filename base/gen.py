#!/usr/bin/python

import random
import subprocess
import sys
import re

PROC_NAME = ["./mm-null", "test.dat"]

PLAYERS = [
    "../bots/Random/Random",
    #"../bots/Follower/Follower",
    "../bots/Probability/Probability",
    "../bots/Greedy/Greedy",
    "../bots/MyAwesomeBot/MyAwesomeBot",
    "../bots/Other/bossbotzz",
    "../bots/Other/avgbot"
	]

num_players = len(PLAYERS)

random.seed()

def gen():
    f = open("test.dat", "w")
    num_cows = random.randint(3, 100)
    num_rounds = 1000
    MAX_MILK = random.randint(100, 10000000)
    
    f.write("{} {}\n".format(num_cows, num_rounds))

    for i in xrange(0, num_cows):
        f.write(str(random.randint(num_players, MAX_MILK)) + " ")

    f.write("\n\n{}\n".format(num_players))

    for i in xrange(0, num_players):
        f.write(PLAYERS[i] + "\n")
    f.close()

def readfromstdout(proc):
    ret = ""
    while True:
        line = proc.stdout.readline()
        if line != '':
            ret = ret + line
        else:
            break
    return ret.rstrip()

def execAndReadStdout(procname):
	proc = subprocess.Popen(procname, stdout=subprocess.PIPE)
	return readfromstdout(proc)


def run_regex(txt):
    re1='(WINNER)'	# Word 1
    re2='( )'	# White Space 1
    re3='(:)'	# Any Single Character 1
    re4='(:)'	# Any Single Character 2
    re5='( )'	# White Space 2
    re6='(([a-zA-Z0-9]*))'	# Alphanum 1
    #print txt
    rg = re.compile(re1+re2+re3+re4+re5+re6,re.IGNORECASE|re.DOTALL)
    m = rg.search(txt)
    if m:
        word1=m.group(1)
        ws1=m.group(2)
        c1=m.group(3)
        c2=m.group(4)
        ws2=m.group(5)
        alphanum1=m.group(6)
        return alphanum1
    return "failed"

win_dict = {}

for x in xrange(0, int(sys.argv[1])):
    gen()
    output =  execAndReadStdout(PROC_NAME)
    print "* finished running game " + str(x+1) + "."
    winner = run_regex(output.split('\n')[-1])
    if not winner in win_dict:
        win_dict[winner] = 0
    win_dict[winner] += 1

print "RESULTS: "

for key in win_dict:
    print(key + ": " + str(win_dict[key]))

    
