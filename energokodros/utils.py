from typing import Iterable


def append_http_and_https_for_hosts(hosts: Iterable[str]) -> Iterable[str]:
    hosts_with_http_and_https = []
    hosts_with_http_and_https.extend([host + 'http://' for host in hosts])
    hosts_with_http_and_https.extend([host + 'https://' for host in hosts])
    return hosts_with_http_and_https
