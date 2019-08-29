#!/usr/bin/env python3

import os
import sys
from libnmap.parser import NmapParser
import subprocess as su


class NmapParserFunk:
    def __init__(self, target):
        self.target = target
        self.services = []
        self.tcp_ports = []
        self.http_ports = []
        self.ssl_ports = []
        self.smb_ports = []
        self.dns_ports = []
        self.nmap_services = []
        self.proxy_ports = []
        self.ssh_ports = []
        self.ssh_version = []
        self.oracle_tns_ports = []
        self.ftp_ports = []
        self.smtp_ports = []
        self.ldap_ports = []
        self.java_rmi_ports = []
        self.cups_ports = []
        self.rpc_ports = []
        self.nfs_ports = []
        self.udp_ports = []
        ######## Proxy Ports #########
        self.proxy_nmap_services = []
        self.proxy_services = []
        self.proxy_tcp_ports = []
        self.proxy_http_ports = []
        self.proxy_ssl_ports = []
        self.proxy_smb_ports = []
        self.proxy_dns_ports = []
        self.proxy_nmap_services = []
        self.proxy_ports2 = []
        self.proxy_ssh_ports = []
        self.proxy_ssh_version = []
        self.proxy_oracle_tns_ports = []
        self.proxy_ftp_ports = []
        self.proxy_smtp_ports = []
        self.proxy_ldap_ports = []
        self.proxy_java_rmi_ports = []
        self.proxy_cups_ports = []
        self.proxy_rpc_ports = []
        self.proxy_nfs_ports = []

    def openPorts(self):
        report = NmapParser.parse_fromfile(
            f"/root/Documents/VULNHUB/boxes/JEROME/nmap/full-tcp-scan-192.168.11.174.xml"
            # f"{self.target}-Report/nmap/top-ports-{self.target}.xml"
        )
        self.nmap_services += report.hosts[0].services
        self.nmap_services = sorted(self.nmap_services, key=lambda s: s.port)
        # print(self.nmap_services)
        ignored_windows_http_ports = [5985, 47001]
        for service in self.nmap_services:
            if "open" not in service.state:
                continue
            self.services.append(
                (
                    service.port,
                    service.service,
                    service.tunnel,
                    service.cpelist,
                    service.banner,
                )
            )
            for service in self.services:
                if service[0] not in self.tcp_ports:
                    self.tcp_ports.append(service[0])
                if "ssl" in service[2]:
                    if service[0] not in self.ssl_ports:
                        self.ssl_ports.append(service[0])
                if "http" in service[1]:
                    if "ssl" not in service[2]:
                        if service[0] not in ignored_windows_http_ports:
                            if service[0] not in self.http_ports:
                                self.http_ports.append(service[0])
                if "netbios-ssn" in service[1]:
                    if service[0] not in self.smb_ports:
                        self.smb_ports.append(service[0])
                if "microsoft-ds" in service[1]:
                    if service[0] not in self.smb_ports:
                        self.smb_ports.append(service[0])
                if "domain" in service[1]:
                    if service[0] not in self.dns_ports:
                        self.dns_ports.append(service[0])
                if "http-proxy" in service[1]:
                    if service[0] not in self.proxy_ports:
                        self.proxy_ports.append(service[0])
                if "ssh" in service[1]:
                    if service[0] not in self.ssh_ports:
                        self.ssh_ports.append(service[0])
                    if service[4] not in self.ssh_version:
                        self.ssh_version.append(service[4])
                if "oracle-tns" in service[1]:
                    if service[0] != 49160:
                        if service[0] not in self.oracle_tns_ports:
                            self.oracle_tns_ports.append(service[0])
                if "ftp" in service[1]:
                    if service[0] not in self.ftp_ports:
                        self.ftp_ports.append(service[0])
                if "smtp" in service[1]:
                    if service[0] not in self.smtp_ports:
                        self.smtp_ports.append(service[0])
                if "rpcbind" in service[1]:
                    if service[0] not in self.nfs_ports:
                        self.nfs_ports.append(service[0])
                if "msrpc" in service[1]:
                    if service[0] not in self.rpc_ports:
                        self.rpc_ports.append(service[0])
                if "ldap" in service[1]:
                    if service[0] not in self.ldap_ports:
                        self.ldap_ports.append(service[0])
                if "BaseHTTPServer" in service[4]:
                    if service[0] not in self.http_ports:
                        self.http_ports.append(service[0])

        # print("HTTP PORTS:", self.http_ports)
        # print("ORACLE PORTS:", self.oracle_tns_ports)
        # print("OPEN TCP PORTS:", self.tcp_ports)
        # print("SSL:", self.ssl_ports)
        # print("SMB:", self.smb_ports)
        # print("DNS:", self.dns_ports)
        # print("Services:", self.services)
        # print("SSH:", self.ssh_ports)
        # print("SSH VERSION:", self.ssh_version)
        # print("Proxy Ports:", self.proxy_ports)

    def openProxyPorts(self):
        self.openPorts()
        proxy_report = NmapParser.parse_fromfile(
            f"/root/Documents/VULNHUB/boxes/JEROME/nmap/proxychainScanTopPorts.xml"
            # f"{self.target}-Report/nmap/proxychain-top-ports.xml"
        )
        self.proxy_nmap_services += proxy_report.hosts[0].services
        self.proxy_nmap_services = sorted(
            self.proxy_nmap_services, key=lambda s: s.port
        )
        ignored_windows_http_ports = [5985, 47001]
        for service in self.proxy_nmap_services:
            if "open" not in service.state:
                continue
            self.proxy_services.append(
                (
                    service.port,
                    service.service,
                    service.tunnel,
                    service.cpelist,
                    service.banner,
                )
            )
            for service in self.proxy_services:
                if service[0] not in self.proxy_tcp_ports:
                    self.proxy_tcp_ports.append(service[0])
                if "ssl" in service[2]:
                    if service[0] not in self.proxy_ssl_ports:
                        self.proxy_ssl_ports.append(service[0])
                if "http" in service[1]:
                    if "ssl" not in service[2]:
                        if service[0] not in ignored_windows_http_ports:
                            if service[0] not in self.proxy_http_ports:
                                self.proxy_http_ports.append(service[0])
                if "netbios-ssn" in service[1]:
                    if service[0] not in self.proxy_smb_ports:
                        self.proxy_smb_ports.append(service[0])
                if "microsoft-ds" in service[1]:
                    if service[0] not in self.proxy_smb_ports:
                        self.proxy_smb_ports.append(service[0])
                if "domain" in service[1]:
                    if service[0] not in self.proxy_dns_ports:
                        self.proxy_dns_ports.append(service[0])
                if "http-proxy" in service[1]:
                    if service[0] not in self.proxy_ports2:
                        self.proxy_ports2.append(service[0])
                if "ssh" in service[1]:
                    if service[0] not in self.proxy_ssh_ports:
                        self.proxy_ssh_ports.append(service[0])
                    if service[4] not in self.proxy_ssh_version:
                        self.proxy_ssh_version.append(service[4])
                if "oracle-tns" in service[1]:
                    if service[0] != 49160:
                        if service[0] not in self.proxy_oracle_tns_ports:
                            self.proxy_oracle_tns_ports.append(service[0])
                if "ftp" in service[1]:
                    if service[0] not in self.proxy_ftp_ports:
                        self.proxy_ftp_ports.append(service[0])
                if "smtp" in service[1]:
                    if service[0] not in self.proxy_smtp_ports:
                        self.proxy_smtp_ports.append(service[0])
                if "rpcbind" in service[1]:
                    if service[0] not in self.proxy_nfs_ports:
                        self.proxy_nfs_ports.append(service[0])
                if "msrpc" in service[1]:
                    if service[0] not in self.proxy_rpc_ports:
                        self.proxy_rpc_ports.append(service[0])
                if "ldap" in service[1]:
                    if service[0] not in self.proxy_ldap_ports:
                        self.proxy_ldap_ports.append(service[0])
                if "BaseHTTPServer" in service[4]:
                    if service[0] not in self.proxy_http_ports:
                        self.proxy_http_ports.append(service[0])

        # print("HTTP PORTS:", self.proxy_http_ports)
        # print("ORACLE PORTS:", self.proxy_oracle_tns_ports)
        # print("OPEN TCP PORTS:", self.proxy_tcp_ports)
        # print("SSL:", self.proxy_ssl_ports)
        # print("SMB:", self.proxy_smb_ports)
        # print("DNS:", self.proxy_dns_ports)
        # print("Services:", self.proxy_services)
        # print("SSH:", self.proxy_ssh_ports)
        # print("SSH VERSION:", self.proxy_ssh_version)
        # print("Proxy Ports2:", self.proxy_ports2)
