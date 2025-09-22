#!/usr/bin/env python3

import re

def fix_scanner_typos():
    """Fix typos in the scanner.py file"""
    
    # Read the current scanner.py file
    with open('backend/scanner.py', 'r') as f:
        content = f.read()
    
    # Fix the typos
    content = content.replace('self.findings.append', 'self.findings.append')
    content = content.replace('self.findings.append', 'self.findings.append')
    
    # Write the fixed content back
    with open('backend/scanner.py', 'w') as f:
        f.write(content)
    
    print("Fixed typos in scanner.py")

if __name__ == "__main__":
    fix_scanner_typos()
