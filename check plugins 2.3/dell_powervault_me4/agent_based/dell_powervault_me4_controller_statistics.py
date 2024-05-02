#!/usr/bin/env python3
"""Dell ME4 controller statistics check"""

# (c) Andreas Doehler <andreas.doehler@bechtle.com/andreas.doehler@gmail.com>
# License: GNU General Public License v2

from typing import Any, Mapping

from cmk.base.plugins.agent_based.agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
)

from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    render,
    register,
    Result,
    State,
    Service,
    Metric,
)

from .utils.dell_powervault_me4 import parse_dell_powervault_me4

register.agent_section(
    name="dell_powervault_me4_controller_statistics",
    parse_function=parse_dell_powervault_me4,
)


def discovery_dell_powervault_me4_controller_statistics(section) -> DiscoveryResult:
    """for every controller one service is dicovered"""
    for item in section:
        yield Service(item=item)


def check_dell_powervault_me4_controller_statistics(
    item: str, params: Mapping[str, Any], section
) -> CheckResult:
    """check the state of the controller"""
    data = section.get(item, {})
    if not data:
        return
    iops = data.get("iops")
    bytespersecond = data.get("bytes-per-second-numeric")
    data_read = data.get("data-read")
    data_write = data.get("data-written")
    message = f"Written data {data_write} and read data {data_read}, \
                IOPS {iops}/s, Bytes {render.bytes(bytespersecond)}/s"
    yield Metric("iops", iops)
    yield Metric("bytes", bytespersecond)
    yield Result(state=State(0), summary=message)


register.check_plugin(
    name="dell_powervault_me4_controller_statistics",
    service_name="Controller Stats %s",
    sections=["dell_powervault_me4_controller_statistics"],
    check_default_parameters={},
    discovery_function=discovery_dell_powervault_me4_controller_statistics,
    check_function=check_dell_powervault_me4_controller_statistics,
    check_ruleset_name="dell_powervault_me4_controller_statistics",
)
