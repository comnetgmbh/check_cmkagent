#!/usr/bin/python

from modules import check_checkmk
import argparse

DATA_PATH = '/var/lib/check_cmkagent'

parser = argparse.ArgumentParser(description = 'Check for check_mk_agent')
parser.add_argument('-H', '--host', required = True)
parser.add_argument('-s', '--section', required = True)
parser.add_argument('-a', '--argument')
parser.add_argument('-w', '--warn')
parser.add_argument('-c', '--crit')
args = parser.parse_args()

def read_file(filename):
    with open(filename, 'r') as f:
        agent_output = []
        line = f.readline()
        while line:
            agent_output.append(line.rstrip().split())
            line = f.readline()
        return agent_output


def find_agent_section(filename, section):
    agent_output = read_file(filename)
    relevant_output = []
    is_relevant = False
    for line in agent_output:
        if len(line) > 0:
            if line[0].startswith('<<<'):
                if section in line[0]:
                    is_relevant = True
                else:
                    is_relevant = False
            elif is_relevant:
                relevant_output.append(line)
    return relevant_output


filename = DATA_PATH + '/' + args.host
relevant_output = find_agent_section(filename, args.section)

params = (args.warn, args.crit)
test = check_checkmk.Check_checkmk.check('Check_' + args.section, relevant_output, args.argument, params)
