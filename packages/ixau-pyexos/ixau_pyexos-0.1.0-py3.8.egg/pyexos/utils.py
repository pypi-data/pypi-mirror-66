"""
pyexos - Extreme Networks Config Manipulation
Copyright (C) 2020 Internet Association of Australian (IAA)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import re


class NotImplementedException(Exception):
    """ CLI Command Exception """

    pass


class SSHException(Exception):
    """ CLI Command Exception """

    pass


class CLICommandException(Exception):
    """ CLI Command Exception """

    pass


class ConfigParseException(Exception):
    """ Config Parse Exception """

    pass


sharing_re = re.compile(
    r"(enable sharing (.*?) grouping (.*?) algorithm (.*?)$)", re.IGNORECASE
)
sharing_for_delete_re = re.compile(
    r"(enable sharing (.*?) grouping (.*?) algorithm)", re.IGNORECASE
)
acl_re = re.compile("(configure access-list (.*?) ports (.*?))", re.IGNORECASE)
vlan_re = re.compile(
    r"(configure vlan (.*?) add ports (.*?) (tagged|untagged))$", re.IGNORECASE
)
vlan_create_re = re.compile('create vlan "(.*?)"')
port_name_re = re.compile(
    r"(configure ports (.*?) (display-string|description-string)) (.*?)$",
    re.IGNORECASE,
)
port_name_for_delete_re = re.compile(
    r"(configure ports (.*?) (display-string|description-string))", re.IGNORECASE,
)
ip_re = re.compile(r"configure\svlan\sl0\sipaddress\s(.*?)\s255.255.255.255")
hostname_re = re.compile(r"configure\ssnmp\ssysName\s\"(.*?)\"")
community_re = re.compile(r"configure\ssnmpv3\sadd\scommunity\s\"(.*?)\"")
ospfarea_re = re.compile(r"create\sospf\sarea\s(.*?)$")
location_re = re.compile(r"configure\ssnmp\ssysLocation\s\"(.*?)\"")
virtuallink_re = re.compile(r"configure\sospf\sadd\svirtual-link\s(.*?)\s(.*?)$")
mplsprotocols_re = re.compile(r"enable mpls protocol (.*?)$")
partition_re = re.compile(r"configure ports (.*?) partition (.*?)$")
vpls_re = re.compile(r"create l2vpn vpls (.*?) fec-id-type pseudo-wire (.*?)$")
