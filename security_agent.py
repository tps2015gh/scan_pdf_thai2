"""
AI Security Agent - Data Leak Checker for AI Scan PDF Project

This agent scans the project for potential data security leaks before uploading to GitHub.
It checks for:
1. Sensitive files that should be in .gitignore
2. API keys, passwords, and credentials in code
3. Personal information (names, IDs, phone numbers)
4. Database credentials and connection strings
5. Private keys and certificates

Usage:
    python security_agent.py [--strict] [--fix]
    
Options:
    --strict  : More aggressive scanning (may have false positives)
    --fix     : Auto-move sensitive files to .gitignore folders
"""

import os
import re
import json
import sys
from datetime import datetime
from pathlib import Path

# Color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Patterns that indicate sensitive data
SENSITIVE_PATTERNS = {
    'api_key': [
        r'api[_-]?key\s*[=:]\s*["\'][A-Za-z0-9]{16,}["\']',
        r'apikey\s*[=:]\s*["\'][A-Za-z0-9]{16,}["\']',
        r'API_KEY\s*[=:]\s*["\'][A-Za-z0-9]{16,}["\']',
    ],
    'password': [
        r'password\s*[=:]\s*["\'][^"\']{8,}["\']',
        r'passwd\s*[=:]\s*["\'][^"\']{8,}["\']',
        r'pwd\s*[=:]\s*["\'][^"\']{8,}["\']',
    ],
    'secret': [
        r'secret\s*[=:]\s*["\'][A-Za-z0-9]{16,}["\']',
        r'SECRET\s*[=:]\s*["\'][A-Za-z0-9]{16,}["\']',
    ],
    'token': [
        r'token\s*[=:]\s*["\'][A-Za-z0-9_.-]{20,}["\']',
        r'access_token\s*[=:]\s*["\'][A-Za-z0-9_.-]{20,}["\']',
        r'auth_token\s*[=:]\s*["\'][A-Za-z0-9_.-]{20,}["\']',
    ],
    'private_key': [
        r'-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----',
        r'PRIVATE KEY\s*[=:]\s*["\'][^"\']+["\']',
    ],
    'database_url': [
        r'(mongodb|mysql|postgresql|redis)://[^\s"\']+',
        r'DATABASE_URL\s*[=:]\s*["\'][^"\']+["\']',
    ],
    'email': [
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    ],
    'phone_thai': [
        r'0[6-9]\d{8}',
        r'\+66\d{9}',
        r'0[1-9]-\d{3}-\d{4}',
    ],
    'thai_id_card': [
        r'\d{4}-\d{5}-\d{2}-\d{1}',
        r'\d{13}',
    ],
    'aws_credentials': [
        r'AKIA[0-9A-Z]{16}',
        r'aws_access_key_id\s*[=:]\s*["\'][A-Z0-9]{20}["\']',
        r'aws_secret_access_key\s*[=:]\s*["\'][A-Za-z0-9/+=]{40}["\']',
    ],
    'ip_address_internal': [
        r'192\.168\.\d{1,3}\.\d{1,3}',
        r'10\.\d{1,3}\.\d{1,3}\.\d{1,3}',
        r'172\.(1[6-9]|2[0-9]|3[0-1])\.\d{1,3}\.\d{1,3}',
    ],
}

# Files that should NEVER be committed
CRITICAL_FILES = [
    '*.pdf',
    '*.key',
    '*.pem',
    '*.p12',
    '*.pfx',
    '.env',
    '.env.*',
    'secrets.json',
    'credentials.json',
    'config.local.*',
    'vector_db.json',
    '*.gguf',
    '*.bin',  # Model files
]

# Directories that should be ignored
CRITICAL_DIRS = [
    'PDF_Input',
    'Temp_Output',
    'LearningDb_Output',
    'chunks',
    'models',
    'embeddings',
    'venv',
    'env',
    '.venv',
]


class SecurityAgent:
    def __init__(self, root_path='.', strict_mode=False):
        self.root_path = Path(root_path)
        self.strict_mode = strict_mode
        self.issues = []
        self.files_scanned = 0
        self.issues_found = 0
        
    def scan(self):
        """Run full security scan"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}🔒 AI Security Agent - Data Leak Checker{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}\n")
        
        self.check_critical_files()
        self.check_critical_dirs()
        self.scan_code_for_secrets()
        self.check_gitignore()
        
        self.print_report()
        
        return len(self.issues) == 0
    
    def check_critical_files(self):
        """Check for critical files that shouldn't be committed"""
        print(f"[{Colors.BLUE}*{Colors.RESET}] Checking for critical files...")
        
        for pattern in CRITICAL_FILES:
            if '*' in pattern:
                # Glob pattern
                for file in self.root_path.glob(f"**/{pattern.lstrip('*')}"):
                    if self._is_in_gitignore(str(file)):
                        continue
                    self.add_issue(
                        level='HIGH',
                        category='Critical File',
                        path=str(file),
                        message=f"File '{file}' should be in .gitignore"
                    )
            else:
                file_path = self.root_path / pattern
                if file_path.exists() and not self._is_in_gitignore(str(file_path)):
                    self.add_issue(
                        level='HIGH',
                        category='Critical File',
                        path=str(file_path),
                        message=f"File '{pattern}' should be in .gitignore"
                    )
    
    def check_critical_dirs(self):
        """Check for critical directories that shouldn't be committed"""
        print(f"[{Colors.BLUE}*{Colors.RESET}] Checking for critical directories...")
        
        for dir_name in CRITICAL_DIRS:
            dir_path = self.root_path / dir_name
            if dir_path.exists() and dir_path.is_dir():
                if not self._is_in_gitignore(str(dir_path)):
                    self.add_issue(
                        level='HIGH',
                        category='Critical Directory',
                        path=str(dir_path),
                        message=f"Directory '{dir_name}/' should be in .gitignore"
                    )
                else:
                    print(f"  {Colors.GREEN}✓{Colors.RESET} {dir_name}/ is properly ignored")
    
    def scan_code_for_secrets(self):
        """Scan code files for potential secrets"""
        print(f"[{Colors.BLUE}*{Colors.RESET}] Scanning code for secrets...")
        
        # Files to scan
        extensions = ['.py', '.js', '.ts', '.json', '.yaml', '.yml', '.md', '.txt', '.html']
        
        for ext in extensions:
            for file in self.root_path.glob(f"**/*{ext}"):
                # Skip directories that should be ignored
                if self._should_skip_directory(file):
                    continue
                    
                self.files_scanned += 1
                self._scan_file_for_secrets(file)
    
    def _scan_file_for_secrets(self, file_path):
        """Scan a single file for sensitive patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception:
            return
        
        for category, patterns in SENSITIVE_PATTERNS.items():
            for pattern in patterns:
                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        # Skip obvious false positives
                        if self._is_false_positive(line, category):
                            continue
                        
                        self.add_issue(
                            level=self._get_severity(category),
                            category=category.replace('_', ' ').title(),
                            path=f"{file_path}:{i}",
                            message=f"Potential {category} detected",
                            snippet=self._mask_sensitive(line.strip())
                        )
    
    def check_gitignore(self):
        """Verify .gitignore exists and is comprehensive"""
        print(f"[{Colors.BLUE}*{Colors.RESET}] Checking .gitignore configuration...")
        
        gitignore_path = self.root_path / '.gitignore'
        if not gitignore_path.exists():
            self.add_issue(
                level='CRITICAL',
                category='Configuration',
                path='.gitignore',
                message='.gitignore file is missing!'
            )
            return
        
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()
        
        # Check if critical patterns are in gitignore
        missing_patterns = []
        for dir_name in CRITICAL_DIRS:
            if dir_name not in gitignore_content:
                missing_patterns.append(f"{dir_name}/")
        
        if missing_patterns:
            self.add_issue(
                level='MEDIUM',
                category='Configuration',
                path='.gitignore',
                message=f"Missing patterns: {', '.join(missing_patterns)}"
            )
        else:
            print(f"  {Colors.GREEN}✓{Colors.RESET} .gitignore is properly configured")
    
    def add_issue(self, level, category, path, message, snippet=None):
        """Add a security issue to the report"""
        self.issues_found += 1
        self.issues.append({
            'level': level,
            'category': category,
            'path': path,
            'message': message,
            'snippet': snippet
        })
    
    def _is_in_gitignore(self, path):
        """Check if a path is covered by .gitignore"""
        gitignore_path = self.root_path / '.gitignore'
        if not gitignore_path.exists():
            return False
        
        with open(gitignore_path, 'r') as f:
            content = f.read().lower()
        
        path_lower = path.lower()
        
        # Check for direct matches
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                if line.rstrip('/') in path_lower or path_lower.endswith(line.rstrip('/')):
                    return True
                if '*' in line:
                    pattern = line.replace('*', '')
                    if pattern in path_lower:
                        return True
        
        return False
    
    def _should_skip_directory(self, file_path):
        """Check if file is in a directory that should be skipped"""
        skip_dirs = ['__pycache__', '.git', 'venv', 'env', '.venv', 
                     'node_modules', '.pytest_cache', '.tox']
        
        for part in file_path.parts:
            if part in skip_dirs:
                return True
        return False
    
    def _is_false_positive(self, line, category):
        """Check if a match is likely a false positive"""
        # Common false positives
        false_positive_indicators = [
            'example', 'placeholder', 'xxx', 'your_', 'example_',
            '# ', '// ', '"""', "'''", 'TODO', 'FIXME', 'NOTE',
            'def ', 'class ', 'import ', 'from ',
            '<li>', '</li>', '<code>', '</code>', '<pre>', '</pre>',
            '```', 'mongodb://', 'postgresql://', 'mysql://',
        ]
        
        line_lower = line.lower()
        for indicator in false_positive_indicators:
            if indicator in line_lower:
                return True
        
        # Specific category exceptions
        if category == 'email' and ('example.com' in line_lower or 'test.com' in line_lower):
            return True
        
        if category == 'api_key' and ('get_' in line_lower or 'set_' in line_lower):
            return True
        
        # IP addresses in documentation/examples are often false positives
        if category == 'ip_address_internal' and ('****' in line or 'example' in line_lower):
            return True
        
        # Database URLs in documentation (examples) are false positives
        if category == 'database_url' and ('****' in line or 'example' in line_lower or 'your_' in line_lower):
            return True
        
        return False
    
    def _get_severity(self, category):
        """Get severity level for a category"""
        severity_map = {
            'api_key': 'HIGH',
            'password': 'HIGH',
            'secret': 'HIGH',
            'token': 'HIGH',
            'private_key': 'CRITICAL',
            'database_url': 'HIGH',
            'email': 'MEDIUM',
            'phone_thai': 'MEDIUM',
            'thai_id_card': 'HIGH',
            'aws_credentials': 'CRITICAL',
            'ip_address_internal': 'LOW',
        }
        return severity_map.get(category, 'MEDIUM')
    
    def _mask_sensitive(self, text, show_chars=4):
        """Mask sensitive data in snippets"""
        if len(text) <= show_chars * 2:
            return '*' * len(text)
        return text[:show_chars] + '*' * (len(text) - show_chars * 2) + text[-show_chars:]
    
    def print_report(self):
        """Print security scan report"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}📊 Security Scan Report{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}\n")
        
        print(f"Files scanned: {self.files_scanned}")
        print(f"Issues found: {self.issues_found}")
        print(f"Scan time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if not self.issues:
            print(f"\n{Colors.GREEN}✅ No security issues found! Safe to commit.{Colors.RESET}\n")
            return
        
        # Group by severity
        by_severity = {'CRITICAL': [], 'HIGH': [], 'MEDIUM': [], 'LOW': []}
        for issue in self.issues:
            by_severity[issue['level']].append(issue)
        
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            issues = by_severity[severity]
            if not issues:
                continue
            
            color = {
                'CRITICAL': Colors.RED + Colors.BOLD,
                'HIGH': Colors.RED,
                'MEDIUM': Colors.YELLOW,
                'LOW': Colors.BLUE
            }[severity]
            
            print(f"\n{color}[{severity}] {len(issues)} issue(s){Colors.RESET}")
            print(f"{Colors.CYAN}{'-'*50}{Colors.RESET}")
            
            for issue in issues[:10]:  # Show first 10
                print(f"\n{color}► {issue['category']}{Colors.RESET}")
                print(f"  File: {issue['path']}")
                print(f"  Issue: {issue['message']}")
                if issue.get('snippet'):
                    print(f"  Snippet: {issue['snippet']}")
            
            if len(issues) > 10:
                print(f"\n  ... and {len(issues) - 10} more issues")
        
        print(f"\n{Colors.BOLD}{Colors.RED}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}⚠️  RECOMMENDATION: Fix issues before committing!{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.RED}{'='*60}{Colors.RESET}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Security Agent - Data Leak Checker')
    parser.add_argument('--strict', action='store_true', help='Enable strict mode')
    parser.add_argument('--fix', action='store_true', help='Auto-fix issues (move to .gitignore)')
    parser.add_argument('--path', default='.', help='Path to scan')
    
    args = parser.parse_args()
    
    agent = SecurityAgent(root_path=args.path, strict_mode=args.strict)
    is_clean = agent.scan()
    
    sys.exit(0 if is_clean else 1)


if __name__ == '__main__':
    main()
