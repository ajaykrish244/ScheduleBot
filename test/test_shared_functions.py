# From https://stackoverflow.com/questions/25827160/importing-correctly-with-pytest
# Change current working directory so test case can find the source files
import sys, os

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/../src"))

import os
from Event import Event
from datetime import datetime
from functionality.shared_functions import (
    add_event_to_file,
    read_event_file,
    read_type_file,
    add_event_to_file,
    turn_types_to_string,
)

import pytest


def test_read_type_file():
    read_type_file("Test")


def test_turn_types_to_string():
    turn_types_to_string("Test")

def test_read_event_file():
    read_event_file("Test")


def test_add_event_to_file():

    add_event_to_file("Test", Event("", datetime(2021, 9, 29, 20, 30), datetime(2021, 9, 29, 20, 45), "", "", ""))