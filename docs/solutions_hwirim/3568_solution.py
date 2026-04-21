import sys

def solve():
    line = sys.stdin.readline().strip()
    if not line:
        return
    
    # Remove final semicolon and split by space or comma
    # Format: BaseType Var1, Var2, ...;
    parts = line[:-1].replace(',', '').split()
    base_type = parts[0]
    variables = parts[1:]
    
    for var in variables:
        # Separate var name and additional types
        name = ""
        extras = ""
        for char in var:
            if char.isalpha():
                name += char
            else:
                extras += char
        
        # Reverse the extras logic
        # Note: [] is treated as a single unit but reversed it becomes ][
        # Wait, C++ logic: int* a[] -> int[]* a
        # Reversing: [] -> [] (stays the same unit), * -> *, & -> &
        reversed_extras = ""
        i = len(extras) - 1
        while i >= 0:
            if extras[i] == ']':
                reversed_extras += '[]'
                i -= 2
            else:
                reversed_extras += extras[i]
                i -= 1
        
        print(f"{base_type}{reversed_extras} {name};")

if __name__ == "__main__":
    solve()
