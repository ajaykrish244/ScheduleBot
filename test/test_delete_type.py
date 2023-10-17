# From https://stackoverflow.com/questions/25827160/importing-correctly-with-pytest
# Change current working directory so test case can find the source files

import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/../src"))
import datetime
import string
from random import randint, choices
import pytest
from event_type import event_type

def test_delete_type():
    rows=[['hw1', '10:10 am', '12:10 pm'], ['hw2', '11:10 am', '12:20 pm']]
    msg_content1 = "hw1"
    msg_content2= "hw3"
    #assert delete_type(rows, msg_content1)== [[['hw2', '11:10 am', '12:20 pm']], 1, 1]