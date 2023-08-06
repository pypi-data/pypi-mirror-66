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

from netmiko import ConnectHandler
from netmiko import NetMikoAuthenticationException
from netmiko import NetMikoTimeoutException

from .utils import acl_re
from .utils import CLICommandException
from .utils import community_re
from .utils import ConfigParseException
from .utils import hostname_re
from .utils import ip_re
from .utils import location_re
from .utils import mplsprotocols_re
from .utils import NotImplementedException
from .utils import ospfarea_re
from .utils import partition_re
from .utils import port_name_for_delete_re
from .utils import port_name_re
from .utils import sharing_for_delete_re
from .utils import sharing_re
from .utils import SSHException
from .utils import virtuallink_re
from .utils import vlan_create_re
from .utils import vlan_re
from .utils import vpls_re


class EXOS(object):
    def __init__(
        self,
        config=[],
        ip=False,
        name=False,
        username=False,
        password=False,
        port=22,
        protocol="ssh",
        timeout=15,
        ssh_config_file=None,
    ):
        """
        Returns a new EXOS device, allowing connections & config manipulation

        :param config:          Start with a loaded config to parse (default: [])
        :param ip:              IP
        :param name:            Hostname
        :param username:        Username
        :param password:        Password
        :param port:            SSH, Telnet or REST port (default: 22)
        :param protocol:        Protocol: 'ssh', 'telnet', 'rest' (default: ssh)
        :param timeout:         Timeout (default: 15 sec)
        :param ssh_config_file: Path to SSH Config File (default: None)
        :return:                EXOS Device
        """
        self.config = []
        self.ports = []
        self.snmp_community = ""
        self.ospf_areas = []
        self.location = ""
        self.ospf_virtual_links = []
        self.mpls_protocols = []
        self.port_partitions = []
        self.vpls = []
        self.vlans = []

        self.ip = ip
        self.name = name
        self.username = username
        self.password = password
        self.port = port
        self.protocol = protocol
        self.timeout = timeout
        self.ssh_config_file = ssh_config_file

        self.device = None

        if config:
            self.load_config(config)

    def _is_int(self, v):
        try:
            int(v)
        except ValueError:
            return False
        return True

    def _process_config(self):
        """
        A helper method that tries to process raw configuration into a usable state for auditing.

        :return:  None
        """
        self.ip = [
            m.group(1) for m in (ip_re.match(line) for line in self.config) if m
        ][0]
        self.name = [
            m.group(1) for m in (hostname_re.match(line) for line in self.config) if m
        ][0]
        self.snmp_community = [
            m.group(1) for m in (community_re.match(line) for line in self.config) if m
        ][0]
        self.ospf_areas = [
            m.group(1) for m in (ospfarea_re.match(line) for line in self.config) if m
        ]
        self.location = "".join(
            [m.group(1) for m in (location_re.match(line) for line in self.config) if m]
        )
        self.ospf_virtual_links = [
            {"peer": m.group(1), "area": m.group(2)}
            for m in (virtuallink_re.match(line) for line in self.config)
            if m
        ]
        self.mpls_protocols = [
            m.group(1)
            for m in (mplsprotocols_re.match(line) for line in self.config)
            if m
        ]
        self.port_partitions = [
            {"port": m.group(1), "partition": m.group(2)}
            for m in (partition_re.match(line) for line in self.config)
            if m
        ]

        for match in [m for m in (vpls_re.match(line) for line in self.config) if m]:
            vpls_vlan_re = re.compile(
                f"configure l2vpn vpls {match.group(1)} add service vlan (.*?)$"
            )
            vpls_peer_core_re = re.compile(
                f"configure l2vpn vpls {match.group(1)} add peer (.*?) core full-mesh"
            )
            vpls_peer_spoke_re = re.compile(
                f"configure l2vpn vpls {match.group(1)} add peer (.*?) spoke"
            )

            vlan = [
                m.group(1)
                for m in (vpls_vlan_re.match(line) for line in self.config)
                if m
            ]
            if vlan:
                vlan = vlan[0]

            peers_core = [
                {"ip": m.group(1), "type": "core", "type2": "full-mesh"}
                for m in (vpls_peer_core_re.match(line) for line in self.config)
                if m
            ]
            peers_spoke = [
                {"ip": m.group(1), "type": "spoke", "type2": ""}
                for m in (vpls_peer_spoke_re.match(line) for line in self.config)
                if m
            ]
            vpls = {
                "name": match.group(1),
                "pwid": match.group(2),
                "vlan": vlan,
                "peers": peers_core + peers_spoke,
            }
            self.vpls.append(vpls)

        for vlan_name in [
            m.group(1)
            for m in (vlan_create_re.match(line) for line in self.config)
            if m
        ]:
            vlan = {
                "name": vlan_name,
                "tag": "",
                "ip": "",
                "bfd": False,
                "acl": "",
                "loopback": False,
                "ipforwarding": False,
                "disable_snooping": False,
                "disable_igmp": False,
                "tagged_ports": [],
                "untagged_ports": [],
                "ospf": {
                    "enable": False,
                    "area": "",
                    "type": "",
                    "priority": None,
                    "cost": None,
                },
                "mpls": {"enable": False, "ldp": False, "rsvp": False},
            }
            for cmd in self.config:
                if vlan_name in cmd:
                    if " tag " in cmd:
                        vlan["tag"] = cmd.split(" tag ")[1]
                    if " ipaddress " in cmd:
                        vlan["ip"] = cmd.split(" ipaddress ")[1]
                    if "enable loopback-mode vlan" in cmd:
                        vlan["loopback"] = True
                    if 'enable bfd vlan "' + vlan_name in cmd:
                        vlan["bfd"] = True
                    if 'disable igmp vlan "' + vlan_name in cmd:
                        vlan["disable_igmp"] = True
                    if 'disable igmp snooping vlan "' + vlan_name in cmd:
                        vlan["disable_snooping"] = True
                    if "enable ipforwarding vlan" in cmd:
                        vlan["ipforwarding"] = True
                    if " add ports " in cmd:
                        if " tagged" in cmd:
                            vlan["tagged_ports"] = vlan[
                                "tagged_ports"
                            ] + self.expandports(
                                cmd.split("add ports")[1].split("tagged")[0]
                            )
                        else:
                            vlan["untagged_ports"] = vlan[
                                "untagged_ports"
                            ] + self.expandports(
                                cmd.split("add ports")[1].split("untagged")[0]
                            )
                    if "configure access-list NoiseFilterProfile" in cmd:
                        vlan["acl"] = cmd.split(" ")[2]
                    if "enable mpls vlan" in cmd:
                        vlan["mpls"]["enable"] = True
                    if "enable mpls rsvp-te vlan" in cmd:
                        vlan["mpls"]["rsvp"] = True
                    if "enable mpls ldp vlan" in cmd:
                        vlan["mpls"]["ldp"] = True
                    if "configure ospf add vlan" in cmd:
                        vlan["ospf"]["enable"] = True
                        vlan["ospf"]["area"] = (
                            cmd.split("area")[1].split(" ")[1].strip()
                        )
                        if "point-to-point" in cmd:
                            vlan["ospf"]["type"] = "point-to-point"
                        elif "passive" in cmd:
                            vlan["ospf"]["type"] = "passive"
                    if "configure ospf vlan" in cmd:
                        if " cost " in cmd:
                            vlan["ospf"]["cost"] = cmd.split(" cost ")[1]
                        if " priority " in cmd:
                            vlan["ospf"]["priority"] = cmd.split(" priority ")[1]

            self.vlans.append(vlan)

        port_scratch = {}
        for match in [
            m for m in (port_name_re.match(line) for line in self.config) if m
        ]:
            port = match.group(2)
            if port not in port_scratch.keys():
                port_scratch[port] = {
                    "interface": port,
                    "description": "",
                    "display": "",
                    "sharing": {"enable": False, "grouping": [], "algorithm": "",},
                }

            if match.group(3) == "description-string":
                port_scratch[port]["description"] = match.group(4).replace('"', "")
            if match.group(3) == "display-string":
                port_scratch[port]["display"] = match.group(4)

        for match in [m for m in (sharing_re.match(line) for line in self.config) if m]:
            port = match.group(2)
            if port in port_scratch.keys():
                port_scratch[port]["sharing"] = {
                    "enable": True,
                    "grouping": self.expandports(match.group(3)),
                    "algorithm": match.group(4),
                }

        self.ports = list(port_scratch.values())

    def _compresslist(self, port_list):
        """
        A helper function for the compressports method that does the hard work

        :param port_list:
        :return:
        """
        port_list = list(map(int, port_list))
        result = []
        i = 0
        n = len(port_list)
        port_list.sort()
        while i < n:
            j = i
            while (j + 1 < n) and (port_list[j + 1] == port_list[j] + 1):
                j += 1

            if i == j:
                result.append(port_list[i])
                i += 1
            else:
                result.append(f"{port_list[i]}-{port_list[j]}")
                i = j + 1

        return result

    def _regex_search_list(self, search_term, search_list, expression):
        """
        A helper method to search a list of strings for a regular expression

        :param search_term:
        :param search_list:
        :param expression:
        :return:
        """
        found = False
        search_match = expression.match(search_term)
        if search_match:
            for item in search_list:
                match_item = expression.match(item)
                if match_item:
                    if match_item.group() == search_match.group():
                        found = True
                        continue

        return found

    def get_delete_command(self, cmd):
        """
        Takes an exos command, and returns the corresponding command to remove / nullify the command

        :param cmd: The create / configure command to remove from the switch
        :return:    The command to
        """
        if "rate-limit flood" in cmd:
            return " ".join(cmd.split(" ")[:-1] + ["no-limit"])

        if "enable sharing" in cmd:
            return " ".join(cmd.split(" ")[:3]).replace("enable", "disable")

        if "create vlan" in cmd or "create meter" in cmd:
            return cmd.replace("create", "delete")

        if "configure vlan" in cmd:
            if "tagged" in cmd:
                return cmd.replace("add", "delete")
            if "untagged" in cmd:
                return cmd.replace("add", "delete")
            if "ipaddress" in cmd:
                return (
                    cmd.replace("configure", "unconfigure").split("ipaddress")[0]
                    + "ipaddress"
                )

        if (
            "disable igmp snooping vlan" in cmd
            or "disable igmp vlan" in cmd
            or "disable lldp ports" in cmd
            or "disable edp ports" in cmd
            or "disable learning port" in cmd
            or "disable learning vlan" in cmd
            or "disable port" in cmd
            or "disable snmp access" in cmd
            or "disable jumbo-frame ports" in cmd
        ):
            return cmd.replace("disable", "enable")

        if (
            "configure ssh2 enable" in cmd
            or "enable cdp port" in cmd
            or "enable snmp access" in cmd
            or "enable web" in cmd
            or "enable dhcp vlan" in cmd
            or "enable jumbo-frame ports" in cmd
            or "enable ipforwarding vlan" in cmd
            or "enable bfd vlan" in cmd
            or "enable mpls vlan" in cmd
            or "enable mpls ldp vlan" in cmd
            or "enable mpls bfd vlan" in cmd
        ):
            return cmd.replace("enable", "disable")

        if "create fdbentry" in cmd or "create fdb" in cmd:
            return cmd.replace("create", "delete").split("port")[0].strip()

        if "enable sflow ports" in cmd:
            return " ".join(cmd.split(" ")[:-1]).replace("enable", "disable")

        if "description-string" in cmd:
            return (
                cmd.replace("configure", "unconfigure").split("description-string")[0]
                + "description-string"
            )

        if "display-string" in cmd:
            return (
                cmd.replace("configure", "unconfigure").split("display-string")[0]
                + "display-string"
            )

        if "configure sharing" in cmd and "lacp system-priority" in cmd:
            # No cmd here - as sharing probably disabled first due to how its used.
            return False

        if "configure vlan" in cmd and "tag" in cmd:
            # Not returning - deleting tag is not something exos can do! Change is OK.
            return False

        if "configure timezone name" in cmd:
            # W/E not critical
            return False

        if "create l2vpn vpws" in cmd:
            return cmd.replace("create", "delete").split("fec-id-type")[0]

        if "configure l2vpn vpws" in cmd:
            if "add peer" in cmd:
                return cmd.replace("add", "delete").split("peer")[0] + "peer"
            if "add service vlan" in cmd:
                return cmd.replace("add service vlan", "delete service vlan")
            if "add service vman" in cmd:
                return cmd.replace("add service vman", "delete service vman")

            if "mtu" in cmd:
                return False

        if "create account" in cmd:
            return (
                cmd.replace("create", "delete")
                .replace("user", "")
                .replace("admin", "")
                .replace("  ", " ")
                .split("encrypted")[0]
                .strip()
            )

        if "configure ospf add vlan" in cmd:
            return cmd.replace("add vlan", "delete vlan").split("area")[0]

        if "configure ospf vlan" in cmd:
            if " cost " in cmd:
                return cmd.split(" cost ")[0] + " automatic"
            if " bfd on" in cmd:
                return cmd.replace("bfd on", "bfd off")

        if "configure ports" in cmd:
            if "partition" in cmd:
                # Eh - you cannot change port partitions, the new one takes effect
                return False

        if "create l2vpn vpls" in cmd:
            return " ".join(cmd.replace("create", "delete").split(" ")[:4])

        if "configure l2vpn vpls" in cmd:
            if "add service vlan" in cmd:
                return cmd.replace("add service vlan", "delete service vlan")
            if "add peer" in cmd:
                return " ".join(cmd.replace("add peer", "delete peer").split(" ")[:-2])

            if "mtu" in cmd:
                return cmd.split("mtu")[0] + "mtu 1500"

        if "configure meter" in cmd:
            # Can only update meters
            return False

        if "configure sflow ports" in cmd:
            if "sample-rate" in cmd:
                return cmd.replace("configure", "unconfigure").split("sample-rate")[0]
            return False

        if "configure access-list" in cmd:
            if "ports " in cmd and "ingress" in cmd:
                return str(
                    re.sub("access-list (.*?) ports", "access-list ports", cmd)
                ).replace("configure", "unconfigure")

        if "configure mpls add vlan" in cmd:
            return cmd.replace("add vlan", "delete vlan")

        ## Command not known - return with XX prepended to isolate these commands.
        raise NotImplementedException("Cannot process: {}".format(cmd))

    def expandports(self, port_list):
        """
        Takes an arbitrary string of compressed ports and expands them to a list of single ports

        :param port_list:   A list of ports to compress (e.g. '1-3,5-6,9-10')
        :return:            Compressed list of ports (e.g. 1,2,3,5,6,9,10)
        """
        new_list = []
        ports = port_list.split(",")

        for p in ports:
            if "-" in p:
                if ":" in p:
                    mod, po = p.split(":")
                    s, e = po.split("-")
                    for i in list(range(int(s), int(e) + 1)):
                        new_list.append(str(mod) + ":" + str(i))
                else:
                    s, e = p.split("-")
                    new_list = new_list + [
                        str(p) for p in list(range(int(s), int(e) + 1))
                    ]

            else:
                new_list.append(p.strip())

        return new_list

    def compressports(self, port_list):
        """
        Takes an arbitrary list of ports and returns a compressed list

        :param port_list:   A list of ports to compress (e.g. 1,2,3,5,6,9,10)
        :return:            Compressed list of ports (e.g. 1-3,5-6,9-10)
        """
        stack = {0: []}
        for item in port_list:
            if self._is_int(item):
                stack[0].append(item)
            else:
                if ":" in item:
                    module, port = item.split(":", 1)
                    module = int(module)
                    if module not in stack.keys():
                        stack[module] = []

                    stack[module].append(port)

        final_list = []
        modules = list(stack.keys())
        modules.sort()
        for module in modules:
            ports = self._compresslist(stack[module])
            if module != 0:
                ports = [f"{module}:{p}" for p in ports]

            final_list = final_list + ports

        return list(map(str, final_list))

    def load_config(self, config):
        """
        Processes the running configuration loaded from the device, or from a flat file on create.

        :param config:  The raw device configuration
        :return:        None
        :raises:        ConfigParseException
        """
        self.config = []

        config = [
            line.strip() for line in config if line.strip() and not line.startswith("#")
        ]

        for line in config:
            match_vlan_re = vlan_re.match(line)
            if match_vlan_re:
                match_vlan = match_vlan_re.group(2)
                match_ports = self.expandports(match_vlan_re.group(3))
                match_tag = match_vlan_re.group(4)
                if match_ports:
                    line = False
                    for port in match_ports:
                        self.config.append(
                            "configure vlan {} add ports {} {}".format(
                                match_vlan, port, match_tag
                            )
                        )

            if line:
                self.config.append(line)

        try:
            self._process_config()
        except (ValueError, IndexError, IOError) as error:
            raise ConfigParseException(
                "Could not parse switch config: {}".format(error)
            )

    def diff_config_merge(self, new_config):
        """
        Builds a diff of the current config to the new config, to merge existing lines.
        e.g. Allowing running "create vlan XX" twice, without getting a CLI Config Error

        :param new_config:  A complete switch configuration
        :return:            A diff of changes from the running configration to merge the new config
        """
        if self.config is None:
            return False

        running_config = self.config
        candidate_config = running_config + [
            line.strip()
            for line in new_config
            if line.strip() and line.strip()[0] != "#"
        ]
        final_config = []

        for cmd in candidate_config:
            if cmd in running_config:
                continue

            if "enable sharing" in cmd:
                if self._regex_search_list(cmd, running_config, sharing_for_delete_re):
                    continue

            if "configure access-list" in cmd:
                if self._regex_search_list(cmd, running_config, acl_re):
                    continue

            final_config.append(cmd)

        return final_config

    def diff_config_replace(self, new_config, skip_lines=[]):
        """
        Builds a delta configuration that can be applied to transition the switch from the running config, to the new config. A 'Config Merge Replace' in any sane vendor.

        :param new_config:  A complete switch configuration
        "param skip_lines:  A list of any config lines you DO NOT WANT IN THE DIFF - Useful to remove things before applying.
        :return:            A list of changes to apply to the switch to transition to the new config.
        """
        to_delete = []
        new_config = [
            line.strip()
            for line in new_config
            if line.strip() and line.strip() not in skip_lines
        ]

        for cmd in self.config:
            # Don't care about the cmd, if it's in the existing running config
            if cmd in new_config:
                continue

            # We dont want to delete anything that is just being changed
            # Port Checks
            if self._regex_search_list(cmd, new_config, port_name_for_delete_re):
                continue

            # Only delete sharing *if required*
            # This will NOT change the sharing type, because reasons and brownfield network
            if self._regex_search_list(cmd, new_config, sharing_for_delete_re):
                continue

            cmd = self.get_delete_command(cmd)
            if cmd:
                to_delete.append(cmd)

        # Before we return from here, we need to fix the order of some of the commands. #JustExtremeThings
        # Create / Configure / Unconfigure etc before any delete.
        to_delete_scratch = {
            "configure": [],
            "unconfigure": [],
            "enable": [],
            "disable": [],
            "create": [],
            "delete": [],
        }
        for cmd in to_delete:
            to_delete_scratch[cmd.split(" ")[0]].append(cmd)

        changes = []
        for cmd_type in to_delete_scratch.keys():
            changes = changes + to_delete_scratch[cmd_type]

        # Finally, get a list of _new_ commands to put on the box, if any
        # Will just use the merge routine to generate these
        new_cmds = self.diff_config_merge(new_config)
        return changes + new_cmds

    def open(self):
        """
        Opens a connection to the device

        :return: None
        :raises: SSHException
        """
        exos_type = {"ssh": "extreme", "telnet": "extreme_telnet"}
        try:
            self.device = ConnectHandler(
                device_type=exos_type[self.protocol],
                ip=self.ip,
                port=self.port,
                username=self.username,
                password=self.password,
                ssh_config_file=self.ssh_config_file,
            )

        except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
            raise SSHException(e)

    def close(self):
        """
        Closes connection to the device if open

        :return:    None
        """
        if hasattr(self.device, "remote_conn"):
            self.device.remote_conn.close()

    def is_alive(self):
        """
        Check if connection to device is alive

        :return:    Boolean
        """
        if self.device:
            return self.device.remote_conn.transport.is_active()

        return False

    def get_running_config(self):
        if not self.is_alive():
            self.open()

        try:
            running_config = self.send_command(
                "show configuration", save=False, delay_factor=30
            )
        except CLICommandException:
            raise

        self.load_config(running_config.splitlines())

        return self.config

    def send_command(self, command, save=True, delay_factor=1):
        """
        Send a single command to the device

        :param command:         (String) Configuration Statements to apply to switch
        :param save:            (Boolean) Save configuration
        :param delay_factor:    (Int) Netmiko Delay Factor (default: 1)
        :return:                (String) Output from device
        :raises:                CLICommandException, SSHException
        """
        if not self.is_alive():
            self.open()

        output = self.device.send_command(command, delay_factor=delay_factor)
        if (
            "%% Invalid" in output
            or "%% A number" in output
            or "%% Incomplete command" in output
        ):
            msg = f'Error sending command: "{command}" - ({output})'
            raise CLICommandException(msg)

        if save:
            output = output + self.device.save_config()

        return output

    def send_config_set(self, config=[], save=True):
        """
        Send a configuration set to the device

        :param config:  (List) Configuration Statements to apply to switch
        :param save:    (Boolean) Save configuration
        :return:        (List) A list of cli output for each command
        :raises:        CLICommandException, SSHException
        """
        if not self.is_alive():
            self.open()

        output = []
        try:
            for cmd in config:
                result = self.send_command(command=cmd, save=False)
                output.append({"command": cmd, "output": result})
        except CLICommandException:
            if save:
                self.device.save_config()
            raise

        if save:
            output.append(
                {"cmd": "save configuration", "output": self.device.save_config(),}
            )

        return output
