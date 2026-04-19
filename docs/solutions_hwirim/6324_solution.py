import sys
import re

def solve():
    n_str = sys.stdin.readline().strip()
    if not n_str:
        return
    n = int(n_str)
    
    for i in range(1, n + 1):
        url = sys.stdin.readline().strip()
        
        # Protocol is always before "://"
        protocol, rest = url.split("://", 1)
        
        # Path starts after the first "/" in the rest
        if "/" in rest:
            host_port, path = rest.split("/", 1)
        else:
            host_port, path = rest, "<default>"
            
        # Port is after ":" in host_port
        if ":" in host_port:
            host, port = host_port.split(":", 1)
        else:
            host, port = host_port, "<default>"
            
        print(f"URL #{i}")
        print(f"Protocol = {protocol}")
        print(f"Host     = {host}")
        print(f"Port     = {port}")
        print(f"Path     = {path}")
        print()

if __name__ == "__main__":
    solve()
