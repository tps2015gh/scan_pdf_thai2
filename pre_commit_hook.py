"""
Pre-commit Security Check Hook

Run this before every git commit to ensure no sensitive data is leaked.

Usage:
    python pre_commit_hook.py
    
Or add to .git/hooks/pre-commit:
    #!/bin/bash
    python pre_commit_hook.py
"""

import subprocess
import sys
from security_agent import SecurityAgent

def main():
    print("\n" + "="*60)
    print("🔒 Pre-commit Security Check")
    print("="*60 + "\n")
    
    # Run security scan
    agent = SecurityAgent(root_path='.', strict_mode=True)
    is_clean = agent.scan()
    
    if not is_clean:
        print("\n❌ SECURITY CHECK FAILED")
        print("Please fix the issues above before committing.\n")
        print("To bypass this check (NOT RECOMMENDED), use:")
        print("  git commit --no-verify\n")
        sys.exit(1)
    
    print("\n✅ SECURITY CHECK PASSED")
    print("Safe to commit!\n")
    sys.exit(0)

if __name__ == '__main__':
    main()
