#!/usr/bin/env python3

import os
import time
from sty import fg, bg, ef, rs, RgbFg
from lib import nmapParser
import subprocess as s
import glob


class EnumWeb:
    def __init__(self, target):
        self.target = target
        self.processes = ""
        self.cms_processes = ""
        self.proxy_processes = ""

    def Scan(self):
        np = nmapParser.NmapParserFunk(self.target)
        np.openPorts()
        http_ports = np.http_ports
        cwd = os.getcwd()
        if len(http_ports) == 0:
            pass
        else:
            a = f"{fg.cyan} Enumerating HTTP Ports, Running the following commands: {fg.rs}"

            print(a)
            if not os.path.exists(f"{self.target}-Report/web"):
                os.makedirs(f"{self.target}-Report/web")
            if not os.path.exists(f"{self.target}-Report/aquatone"):
                os.makedirs(f"{self.target}-Report/aquatone")
            http_string_ports = ",".join(map(str, http_ports))
            for port in http_ports:
                if not os.path.exists(
                    f"{self.target}-Report/web/eyewitness-{self.target}-{port}"
                ):
                    os.makedirs(
                        f"{self.target}-Report/web/eyewitness-{self.target}-{port}"
                    )
                commands = (
                    f"whatweb -v -a 3 http://{self.target}:{port} | tee {self.target}-Report/web/whatweb-{self.target}-{port}.txt",
                    f"cd /opt/EyeWitness && echo http://{self.target}:{port} >eyefile.txt && ./EyeWitness.py --threads 5 --ocr --no-prompt --active-scan --all-protocols --web -f eyefile.txt -d {cwd}/{self.target}-Report/web/eyewitness-{self.target}-{port} && cd - &>/dev/null",
                    f"wafw00f http://{self.target}:{port} | tee {self.target}-Report/web/wafw00f-{self.target}-{port}.txt",
                    f"curl -sSik http://{self.target}:{port}/robots.txt -m 10 -o {self.target}-Report/web/robots-{self.target}-{port}.txt &>/dev/null",
                    f"python3 /opt/dirsearch/dirsearch.py -u http://{self.target}:{port} -t 50 -e php,asp,aspx,txt,html -w wordlists/dicc.txt -x 403,500 --plain-text-report {self.target}-Report/web/dirsearch-{self.target}-{port}.log",
                    # f"python3 /opt/dirsearch/dirsearch.py -u http://{self.target}:{port} -t 80 -e php,asp,aspx,html,txt -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x 403,500 --plain-text-report {self.target}-Report/web/dirsearch-dlistmedium-{self.target}-{port}.log",
                    f"nikto -ask=no -host http://{self.target}:{port} >{self.target}-Report/web/niktoscan-{self.target}-{port}.txt 2>&1 &",
                )
            self.processes = commands
            # print(self.processes)

    def CMS(self):
        np = nmapParser.NmapParserFunk(self.target)
        np.openPorts()
        http_ports = np.http_ports
        if len(http_ports) == 0:
            pass
        else:
            for http_port in http_ports:
                cwd = os.getcwd()
                reportPath = f"{cwd}/{self.target}-Report/*"
                whatweb_files = []
                cms_commands = []
                dir_list = [
                    d
                    for d in glob.iglob(f"{reportPath}", recursive=True)
                    if os.path.isdir(d)
                ]
                for d in dir_list:
                    reportFile_list = [
                        fname
                        for fname in glob.iglob(f"{d}/*", recursive=True)
                        if os.path.isfile(fname)
                    ]
                    for rf in reportFile_list:
                        if "nmap" not in rf:
                            if "whatweb" in rf:
                                if str(http_port) in rf:
                                    whatweb_files.append(rf)
                if len(whatweb_files) != 0:
                    for i in whatweb_files:
                        cms_strings = [
                            "WordPress",
                            "Magento",
                            "tomcat",
                            "WebDAV",
                            "Drupal",
                            "Joomla",
                        ]
                        with open(i, "r") as wwf:
                            for word in wwf:
                                fword = (
                                    word.replace("[", " ")
                                    .replace("]", " ")
                                    .replace(",", " ")
                                )
                                for cms in cms_strings:
                                    if cms in fword:
                                        if "WordPress" in cms:
                                            wpscan_cmd = f"wpscan --no-update --url http://{self.target}:{http_port}/ --wp-content-dir wp-content --enumerate vp,vt,cb,dbe,u,m --plugins-detection aggressive | tee wpscan-{self.target}-{http_port}.log"
                                            cms_commands.append(wpscan_cmd)
                                        if "Drupal" in cms:
                                            drupal_cmd = f"droopescan scan drupal -u http://{self.target}:{http_port}/ -t 32 | tee drupalscan-{self.target}-{http_port}.log"
                                            cms_commands.append(drupal_cmd)
                                        if "Joomla" in cms:
                                            joomla_cmd = f"joomscan --url http://{self.target}:{http_port}/ -ec | tee joomlascan-{self.target}-{http_port}.log"
                                            cms_commands.append(joomla_cmd)
                                        if "Magento" in cms:
                                            magento_cmd = f"cd /opt/magescan && bin/magescan scan:all http://{self.target}:{http_port}/ | tee magentoscan-{self.target}-{http_port}.log && cd - &>/dev/null"
                                            cms_commands.append(magento_cmd)
                                        if "WebDAV" in cms:
                                            webdav_cmd = f"davtest -move -sendbd auto -url http://{self.target}:{http_port}/ | tee davtestscan-{self.target}-{http_port}.log"
                                            webdav_cmd2 = f"nmap -Pn -v -sV -p {http_port} --script=http-iis-webdav-vuln.nse -oA {self.target}-Report/nmap/webdav {self.target}"
                                            cms_commands.append(webdav_cmd)
                                            cms_commands.append(webdav_cmd2)
                                        if "tomcat" in cms:
                                            tomcat_cmd = f"hydra -C /usr/share/seclists/Passwords/Default-Credentials/tomcat-betterdefaultpasslist.txt -s {http_port} {self.target} http-get /manager/html"

                sorted_commands = sorted(set(cms_commands))
                commands_to_run = []
                for i in sorted_commands:
                    commands_to_run.append(i)
                mpCmds = tuple(commands_to_run)
                self.cms_processes = mpCmds

    def proxyScan(self):
        npp = nmapParser.NmapParserFunk(self.target)
        npp.openProxyPorts()
        proxy_http_ports = npp.proxy_http_ports
        proxy_ports = npp.proxy_ports
        web_proxy_cmds = []
        cwd = os.getcwd()
        if len(proxy_http_ports) == 0:
            pass
        else:
            if not os.path.exists(f"{self.target}-Report/proxy"):
                os.makedirs(f"{self.target}-Report/proxy")
            if not os.path.exists(f"{self.target}-Report/proxy/web"):
                os.makedirs(f"{self.target}-Report/proxy/web")
            for proxy in proxy_ports:
                a = f"{fg.cyan} Enumerating HTTP Ports Through Port: {proxy}, Running the following commands: {fg.rs}"
                print(a)
                for proxy_http_port in proxy_http_ports:
                    proxy_http_string_ports = ",".join(map(str, proxy_http_ports))
                    proxy_whatwebCMD = f"whatweb -v -a 3 --proxy {self.target}:{proxy} http://127.0.0.1:{proxy_http_port} | tee {self.target}-Report/proxy/web/whatweb-proxy-{proxy_http_port}.txt"
                    web_proxy_cmds.append(proxy_whatwebCMD)
                    proxy_dirsearch_cmd = f"python3 /opt/dirsearch/dirsearch.py -e php,asp,aspx,txt,html -x 403,500 -t 50 -w wordlists/dicc.txt --proxy {self.target}:{proxy} -u http://127.0.0.1:{proxy_http_port} --plain-text-report {self.target}-Report/proxy/web/dirsearch-127.0.0.1-proxy-{proxy}-{proxy_http_port}.log"
                    web_proxy_cmds.append(proxy_dirsearch_cmd)
                    proxy_dirsearch_cmd2 = f"python3 /opt/dirsearch/dirsearch.py -u http://{self.target}:{proxy_http_port} -t 80 -e php,asp,aspx -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -x 403,500 --plain-text-report {self.target}-Report/proxy/web/dirsearch-dlistsmall-127.0.0.1-proxy-{proxy_http_port}.log"
                    web_proxy_cmds.append(proxy_dirsearch_cmd2)
                    proxy_nikto_cmd = f"nikto -ask=no -host http://127.0.0.1:{proxy_http_port}/ -useproxy http://{self.target}:{proxy}/ -output {self.target}-Report/nikto-port-{proxy_http_port}-proxy-scan.txt"
                    web_proxy_cmds.append(proxy_nikto_cmd)

                    sorted_commands = sorted(set(web_proxy_cmds), reverse=True)
                    commands_to_run = []
                    for i in sorted_commands:
                        commands_to_run.append(i)
                    wpCmds = tuple(commands_to_run)
                    self.proxy_processes = wpCmds
