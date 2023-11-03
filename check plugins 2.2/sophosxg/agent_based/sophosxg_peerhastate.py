#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Matthias Binder 'hds@kpc.de' - K&P Computer Service- und Vertriebs-GmbH
# (c) Andreas Doehler 'andreas.doehler@bechtle.com'
# License: GNU General Public License v2

from typing import Dict
from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    register,
    Result,
    Service,
    State,
)
from cmk.base.plugins.agent_based.agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
)

Section = Dict[str, str]


def discover_sophosxg_peerhastate(section: Section) -> DiscoveryResult:
    if section:
        yield Service()


def check_sophosxg_peerhastate(section: Section) -> CheckResult:
    hastate = section.get("peerhastatus", "99")
    peerappkey = section.get("peerappkey")
    haconfigmode = section.get("haconfigmode")

    ha_states: Dict[str, tuple[str, int]] = {
        "0": ("Not Applicable", 1),
        "1": ("Auxiliary", 0),
        "2": ("Standalone", 2),
        "3": ("Primary", 0),
        "4": ("Faulty", 2),
        "5": ("Ready", 1),
    }

    ha_state_name, state = ha_states.get(hastate, ("Unknown", 3))

    summarytext = (
        f"HA Peer Device State: {ha_state_name}, "
        f"HA Peer App Key: {peerappkey}, "
        f"HA Peer Device Config Mode: {haconfigmode}"
    )

    yield Result(state=State(state), summary=summarytext)


register.check_plugin(
    name="sophosxg_peerhastate",
    sections=["sophosxg_hastate"],
    service_name="HA Peer State",
    discovery_function=discover_sophosxg_peerhastate,
    check_function=check_sophosxg_peerhastate,
)
