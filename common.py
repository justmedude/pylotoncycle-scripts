#!/usr/bin/env python

import pylotoncycle

import config


def get_connection():
    conn = pylotoncycle.PylotonCycle(config.username, config.password)
    return conn
