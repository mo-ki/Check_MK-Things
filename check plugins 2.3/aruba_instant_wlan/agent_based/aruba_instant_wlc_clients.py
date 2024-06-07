#!/usr/bin/env python3
'''Aruba instant WLC clients on SSID'''
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) Andreas Doehler <andreas.doehler@bechtle.com/andreas.doehler@gmail.com>

# License: GNU General Public License v2

from typing import List

from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    register,
    SNMPTree,
    startswith,
)
from cmk.base.plugins.agent_based.agent_based_api.v1.type_defs import StringTable
from cmk.plugins.lib.wlc_clients import ClientsTotal, WlcClientsSection


def parse_aruba_instant_wlc_clients(
    string_table: List[StringTable],
) -> WlcClientsSection[ClientsTotal]:
    """parse wlc client data"""
    section: WlcClientsSection[ClientsTotal] = WlcClientsSection()
    for ssid_name, ssid_state, num_clients_str in string_table[0]:
        if ssid_name == "":
            continue
        if int(ssid_state) == 1:
            continue
        num_clients = int(num_clients_str)
        section.total_clients += num_clients
        section.clients_per_ssid[ssid_name] = ClientsTotal(total=num_clients)
    return section


register.snmp_section(
    name="aruba_instant_wlc_clients",
    parsed_section_name="wlc_clients",
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.14823.1.2.111"),
    parse_function=parse_aruba_instant_wlc_clients,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.14823.2.3.3.1.1.7.1",
            oids=[
                "2",  # SSIDName
                "3",  # SSIDState
                "4",  # connected Clients
            ],
        )
    ],
)
