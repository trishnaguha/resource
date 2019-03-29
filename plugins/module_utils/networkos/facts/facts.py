#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 <company_name>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The facts class for networkos
this file validates each subset of facts and selectively
calls the appropriate facts gathering function
"""

from ansible_collections.trishnag.my_collection.plugins.module_utils. \
     networkos.argspec.facts.facts import FactsArgs
from ansible_collections.trishnag.my_collection.plugins.module_utils. \
     networkos.argspec.interfaces.interfaces import InterfacesArgs
from ansible_collections.trishnag.my_collection.plugins.module_utils. \
     networkos.facts.base import FactsBase
from ansible_collections.trishnag.my_collection.plugins.module_utils. \
     networkos.facts.interfaces.interfaces import InterfacesFacts

class Facts(FactsArgs, FactsBase): #pylint: disable=R0903
    """ The fact class for networkos
    """

    VALID_SUBSETS = [
        'net_configuration_interfaces',
    ]

    def get_facts(self, module, connection, gather_subset=None):
        """ Collect the facts for networkos

        :param module: The module instance
        :param connection: The device connection
        :param gather_subset: The facts subset to collect
        :rtype: dict
        :returns: the facts gathered
        """
        runable_subsets = set()
        exclude_subsets = set()
        if not gather_subset:
            gather_subset = ['all']

        for subset in gather_subset:
            if subset == 'all':
                runable_subsets.update(self.VALID_SUBSETS)
                continue
            if subset.startswith('!'):
                subset = subset[1:]
                if subset == 'all':
                    exclude_subsets.update(self.VALID_SUBSETS)
                    continue
                exclude = True
            else:
                exclude = False

            if subset not in self.VALID_SUBSETS:
                module.fail_json(msg='Bad subset')

            if exclude:
                exclude_subsets.add(subset)
            else:
                runable_subsets.add(subset)

        if not runable_subsets:
            runable_subsets.update(self.VALID_SUBSETS)

        runable_subsets.difference_update(exclude_subsets)
        self.ansible_facts['gather_subset'] = list(runable_subsets)

        for attr in runable_subsets:
            getattr(self, '_get_%s' % attr, {})(module, connection)

        return self.ansible_facts

    @staticmethod
    def _get_net_configuration_interfaces(module, connection):
        return InterfacesFacts(InterfacesArgs. \
               argument_spec, 'config', 'options').populate_facts(module, connection)
