#!/usr/bin/python

from modules import check_checkmk
import argparse

parser = argparse.ArgumentParser(description = 'Check for check_mk_agent')
parser.add_argument('-H', '--host', required = True)
parser.add_argument('-s', '--section', required = True)
parser.add_argument('-w', '--warn')
parser.add_argument('-c', '--crit')
args = parser.parse_args()

columns = ['2', '2', '3']
params = (args.warn, args.crit)
test = check_checkmk.Check_checkmk.check(args.section, columns, params)

