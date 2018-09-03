# check_cmkagent

## About
check_cmkagent reads Check_MK agent output dumps found in
/var/lib/check_cmkagent and runs service-specific checks based on the data found
there.
It is designed to be configured via the thruk-check_cmkagent frontend.

## Usage
```
check_cmkagent -H HOST -s SECTION [-a ENTITY] [-w WARNING_THRESHOLD] [-c CRITICAL_THRESHOLD]

Options:
    -H HOST               Hostname / IP of host to check
                          Has to match *exactly* your check_cmkagent_active
                          invocation
    -s SECTION            What agent section to act upon. For example 'df'
    -a ENTITY             What instance/entity to act upon. For example '/home/'
    -w WARNING_THRESHOLD  Warning threshold level
    -c CRITICAL_THRESHOLD Critical threshold level
```

## Author & Copyright
Copyright 2018 Nikolas Hagemann, comNET GmbH <nikolas.hagemann@comnetgmbh.com>

Copyright 2018 Rika Lena Denia, comNET GmbH <rika.denia@comnetgmbh.com>
