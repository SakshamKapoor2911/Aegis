#!/usr/bin/env python3

def fix_scanner_ports():
    """Fix the port numbers in scanner.py"""
    
    # Read the current scanner.py file
    with open('backend/scanner.py', 'r') as f:
        content = f.read()
    
    # Fix the port numbers
    content = content.replace('"port": 5050,', '"port": 5050,')
    content = content.replace('"port": 8080,', '"port": 5000,')
    
    # Write the fixed content back
    with open('backend/scanner.py', 'w') as f:
        f.write(content)
    
    print("Fixed scanner port numbers")

if __name__ == "__main__":
    fix_scanner_ports()
