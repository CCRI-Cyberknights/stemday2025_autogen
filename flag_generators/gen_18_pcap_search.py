#!/usr/bin/env python3
try:
    from scapy.all import *
except ImportError:
    print("❌ Scapy is not installed. Run: pip install scapy")
    exit(1)

import random
import os
from pathlib import Path
from flag_generators.flag_helpers import generate_real_flag, generate_fake_flag  # ✅ fixed import


def http_packet(src, dst, sport, dport, payload):
    """
    Craft a TCP packet with HTTP payload.
    """
    ip = IP(src=src, dst=dst)
    tcp = TCP(sport=sport, dport=dport, flags="PA", seq=random.randint(1000, 5000))
    raw = Raw(load=payload)
    return ip / tcp / raw


def http_conversation(src, dst, flag=None, noise=False, real_flag=False):
    """
    Build a realistic HTTP conversation.
    """
    sport = random.randint(1024, 65535)
    dport = 80
    packets = []

    # Client sends HTTP GET
    packets.append(http_packet(
        src, dst, sport, dport,
        f"GET / HTTP/1.1\r\nHost: {dst}\r\nUser-Agent: Mozilla/5.0\r\nAccept: */*\r\n\r\n".encode()
    ))

    # Server responds
    server_headers = (
        "HTTP/1.1 200 OK\r\n"
        "Server: nginx/1.18.0\r\n"
        "Content-Type: text/html\r\n"
        "Set-Cookie: sessionid=" +
        ''.join(random.choices('abcdef1234567890', k=10)) + "; HttpOnly\r\n"
    )

    # Embed flag in header if real
    if real_flag:
        server_headers += f"X-Flag: {flag}\r\n"

    # Body content
    if noise:
        body = "<html><body><p>Welcome to our web server.</p></body></html>"
    elif flag and not real_flag:
        # Fake flags as distractions in HTML comments
        body = f"<html><body><!-- DEBUG: Found flag {flag} --></body></html>"
    else:
        body = "<html><body><p>Hello, authorized user.</p></body></html>"

    response = f"{server_headers}\r\n{body}".encode()
    packets.append(http_packet(dst, src, dport, sport, response))
    return packets


def generate_flag(challenge_folder: Path) -> str:
    """
    Generate traffic.pcap in the challenge folder with
    1 real flag and 4 fake flags. Return the real flag.
    """
    try:
        # === Generate flags ===
        real_flag = generate_real_flag()
        fake_flags = set()
        while len(fake_flags) < 4:
            fake = generate_fake_flag()
            if fake != real_flag:
                fake_flags.add(fake)
        fake_flags = list(fake_flags)

        # === Generate traffic ===
        packets = []

        # Random noise traffic (~150 conversations)
        for _ in range(150):
            src = f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
            dst = f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
            packets.extend(http_conversation(src, dst, noise=True))

        # Embed fake flags
        for fake in fake_flags:
            src = f"172.16.{random.randint(0,255)}.{random.randint(1,254)}"
            dst = f"172.16.{random.randint(0,255)}.{random.randint(1,254)}"
            packets.extend(http_conversation(src, dst, flag=fake))

        # Embed the real flag (header only, no hint in body)
        src = "192.168.50.10"
        dst = "192.168.50.20"
        packets.extend(http_conversation(src, dst, flag=real_flag, real_flag=True))

        # Shuffle packets for realism
        random.shuffle(packets)

        # === Write PCAP ===
        output_file = challenge_folder / "traffic.pcap"
        if output_file.exists():
            backup_file = output_file.with_suffix(".pcap.bak")
            output_file.rename(backup_file)
            print(f"📂 Existing traffic.pcap backed up as {backup_file}")

        wrpcap(str(output_file), packets)

        print(f"✅ traffic.pcap generated in {challenge_folder}")
        print(f"   🏁 Real flag: {real_flag}")
        print(f"   🎭 Fake flags: {', '.join(fake_flags)}")
        print(f"📦 Total packets: {len(packets)}")

        return real_flag  # ✅ Needed for challenges.json update

    except Exception as e:
        print(f"❌ ERROR generating traffic.pcap: {e}")
        raise
