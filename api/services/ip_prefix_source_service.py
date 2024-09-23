"""
MIT License

Project: FortiIPSearch
File: ip_prefix_source_service.py
Copyright (c) 2024 Rahul Prajapati

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import Dict
import ipaddress


class IPSubnetTrieNode:
    """Node class"""

    def __init__(self):
        self._children = {}
        self._is_end_of_subnet = False
        self._service_details = None
        self._subnet = None

    @property
    def children(self) -> Dict:
        """Properties"""
        return self._children

    @property
    def is_end_of_subnet(self) -> bool:
        """Properties"""
        return self._is_end_of_subnet

    @property
    def service_details(self) -> str:
        """Properties"""
        return self._service_details

    @property
    def subnet(self) -> str:
        """Properties"""
        return self._subnet


class IPPrefixTransformerService:
    """
    Transform raw data to trie - efficient way.
    """

    def __init__(self):
        self._root = IPSubnetTrieNode()

    def insert_subnet(self, subnet: str, service_details: Dict[str, any]):
        """
        Insert a subnet into the Trie.
        """
        network = ipaddress.ip_network(subnet, strict=False)
        binary_subnet = self._ip_to_binary(network.network_address, network.prefixlen)

        node = self._root
        for bit in binary_subnet:
            if bit not in node.children:
                node.children[bit] = IPSubnetTrieNode()
            node = node.children[bit]
        node._service_details = service_details
        node._is_end_of_subnet = True
        node._subnet = subnet

    def search_ip(self, ip: str) -> Dict[str, any]:
        """
        Check if an IP address belongs to any subnet in the Trie.
        """
        ip_obj = ipaddress.ip_address(ip)
        binary_ip = self._ip_to_binary(ip_obj, 128 if ip_obj.version == 6 else 32)

        node = self._root
        matched_subnets = {}
        for bit in binary_ip:
            if bit in node.children:
                node = node.children[bit]
                if node.is_end_of_subnet:
                    # Create the subnet mask based on the matched prefix length
                    matched_subnets[node.subnet] = node.service_details
                    print(
                        f"Found IP {ip} in {node.subnet} service details {node.service_details}"
                    )
            else:
                break

        return matched_subnets

    @staticmethod
    def _ip_to_binary(ip, prefix_length) -> str:
        """
        Convert an IP address to binary string representation up to prefix_length.
        """
        ip_int = int(ipaddress.ip_address(ip))
        binary_ip = f"{ip_int:b}".zfill(128 if ip.version == 6 else 32)
        return binary_ip[:prefix_length]
