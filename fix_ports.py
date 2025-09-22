#!/usr/bin/env python3

def fix_scanner_ports():
    """Fix the port numbers in scanner.py"""
    
    # Read the current scanner.py file
    with open('backend/scanner.py', 'r') as f:
        content = f.read()
    
    # Fix the port numbers
    content = content.replace('"port": 3550,', '"port": 3550,')
    content = content.replace('"port": 7000,', '"port": 7000,')
    content = content.replace('"port": 50051,', '"port": 50051,')
    content = content.replace('"port": 8080,', '"port": 8080,')
    content = content.replace('"port": 5050,', '"port": 5050,')
    content = content.replace('"port": 9555,', '"port": 9555,')
    content = content.replace('"port": 8089,', '"port": 8089,')
    
    # Write the fixed content back
    with open('backend/scanner.py', 'w') as f:
        f.write(content)
    
    print("Fixed port numbers in scanner.py")

if __name__ == "__main__":
    fix_scanner_ports()
