#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 <company_name>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The arg spec for the networkos facts module.
"""

class FactsArgs(object): #pylint: disable=R0903
    """ The arg spec for the networkos facts module
    """

    def __init__(self, **kwargs):
        pass

    argument_spec = {
        'gather_subset': dict(default=['all'], type='list')
    }
