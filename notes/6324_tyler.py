import sys

input = sys.stdin.readline

n = int(input())
out = []

for i in range(1, n + 1):
    u = input().strip()

    protocol, rest = u.split("://", 1)

    if "/" in rest:
        host_port, path = rest.split("/", 1)
    else:
        host_port, path = rest, "<default>"

    if ":" in host_port:
        host, port = host_port.split(":", 1)
    else:
        host, port = host_port, "<default>"

    out.append(f"URL #{i}")
    out.append(f"Protocol = {protocol}")
    out.append(f"Host     = {host}")
    out.append(f"Port     = {port}")
    out.append(f"Path     = {path}")
    out.append("")

sys.stdout.write("\n".join(out))
