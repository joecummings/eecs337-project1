#!/bin/bash

echo 'Please enter whichever Python interpreter provides you with Python 3:'
echo '[ python ] OR [ python3 ]'
read py

echo 'Running pre ceremony...'
$py -c 'import gg_api; gg_api.pre_ceremony()'

echo 'Running gg_api main()...'
$py gg_api.py

echo 'Running autograder...'
$py autograder.py

rm givencategories.csv

echo 'Done!'