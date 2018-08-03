#!/usr/bin/python

from modules import check_checkmk

columns = ['2', '2', '3']
params = (2, 3)
test = check_checkmk.Check_checkmk.check('Check_df', columns, params)

