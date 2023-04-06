#!/bin/bash
#Example script for use with cron
source /home/<CHANGEME>/.bashrc
/usr/bin/nohup /<PATH_TO_PYTHON>/bin/python /<PATH_TO_SCRIPT>/delete_vmware_snapshots.py &
