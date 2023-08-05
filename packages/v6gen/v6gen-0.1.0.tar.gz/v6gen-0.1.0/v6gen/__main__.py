import argparse
import re

from ipaddress import IPv6Network


def generate_ip(net, net_max, host):
    host = int(host.encode("utf-8").hex(), 16)

    return IPv6Network(net + host) if host < net_max else None


def generate_ip_wo_vowels(net, net_max, host):
    hostname = ""

    for i in host.lower():
        if i not in ("a", "i", "u", "e", "o"):
            hostname += i

    return hostname, generate_ip(net, net_max, hostname)


def print_result(ip):
    print(ip.compressed)
    exit(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("range", help="IPv6 network range", type=str)

    type_parser = parser.add_mutually_exclusive_group(required=True)
    type_parser.add_argument(
        "-r",
        "--random",
        help="Generate random machine ipv6",
        action="store_true",
    )
    type_parser.add_argument(
        "-n",
        "--name",
        help="Generate IPv6 based on the machine name",
        type=str,
    )

    parser.add_argument(
        "-R",
        "--reverse",
        help="Get reverse IP for ARPA zone",
        action="store_true",
    )

    args = parser.parse_args()
    network = IPv6Network(args.range)
    host_exploded = str(network.exploded).split("/")[0]
    net_host_bytes = int(host_exploded.replace(":", ""), 16)
    max_host_bytes = int(str(network.hostmask).replace(":", ""), 16)

    if network.prefixlen > 126:
        print(
            "Woaw! This subnet is too small for me! I can't do anything "
            "for you!"
        )
        exit(1)

    if args.name:
        hostname = args.name.split(".")[0]
        hostname = re.sub(r"[^A-Za-z0-9]+", "", hostname)

        # Test with the complete hostname
        ip = generate_ip(net_host_bytes, max_host_bytes, hostname)
        if ip:
            print_result(ip)

        # Test by removing vowels
        host, ip = generate_ip_wo_vowels(
            net_host_bytes, max_host_bytes, hostname
        )
        if ip:
            print_result(ip)

        while len(host) != 0:
            host = host[:-1]
            ip = generate_ip(net_host_bytes, max_host_bytes, host)

            if ip:
                print_result(ip)

        print("Meh ¯\_(ツ)_/¯")
    else:
        print("Still not implemented  ¯\_(ツ)_/¯")


if __name__ == "__main__":
    main()
