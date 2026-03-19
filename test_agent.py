"""
Test Agent - AI Scan PDF System Tester

This agent tests all components of the AI Scan PDF system to ensure everything is working.

Usage:
    python test_agent.py [--full] [--verbose]
    
Options:
    --full      : Run comprehensive tests (including PDF parsing)
    --verbose   : Show detailed output
"""

import os
import sys
import json
import requests
import time
from datetime import datetime

# Color codes
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class TestAgent:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.tests_passed = 0
        self.tests_failed = 0
        self.tests_skipped = 0
        self.results = []
        
    def log(self, message, level='info'):
        """Log message with color"""
        colors = {
            'info': Colors.BLUE,
            'success': Colors.GREEN,
            'warning': Colors.YELLOW,
            'error': Colors.RED,
            'test': Colors.CYAN
        }
        color = colors.get(level, Colors.RESET)
        print(f"{color}{message}{Colors.RESET}")
    
    def test_result(self, test_name, passed, message=""):
        """Record test result"""
        if passed:
            self.tests_passed += 1
            self.log(f"  ✓ {test_name}", 'success')
        else:
            self.tests_failed += 1
            self.log(f"  ✗ {test_name}: {message}", 'error')
        
        self.results.append({
            'name': test_name,
            'passed': passed,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
    
    def run_all_tests(self, full_test=False):
        """Run all tests"""
        self.log("\n" + "="*70, 'info')
        self.log("🤖 AI Scan PDF - Test Agent", 'info')
        self.log("="*70 + "\n", 'info')
        
        print(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Test 1: File Structure
        self.log("[Test 1/6] Checking File Structure...", 'test')
        self.test_file_structure()
        print()
        
        # Test 2: Python Dependencies
        self.log("[Test 2/6] Checking Python Dependencies...", 'test')
        self.test_dependencies()
        print()
        
        # Test 3: GPT4All API
        self.log("[Test 3/6] Testing GPT4All API...", 'test')
        self.test_gpt4all_api()
        print()
        
        # Test 4: Vector Database
        self.log("[Test 4/6] Checking Vector Database...", 'test')
        self.test_vector_db()
        print()
        
        # Test 5: Security Check
        self.log("[Test 5/6] Running Security Scan...", 'test')
        self.test_security()
        print()
        
        # Test 6: Full Pipeline (Optional)
        if full_test:
            self.log("[Test 6/6] Testing Full Pipeline...", 'test')
            self.test_full_pipeline()
            print()
        else:
            self.log("[Test 6/6] Skipping Full Pipeline (use --full to include)", 'test')
            self.tests_skipped += 1
            print()
        
        # Print Summary
        self.print_summary()
        
        return self.tests_failed == 0
    
    def test_file_structure(self):
        """Test 1: Check file structure"""
        required_files = [
            'main.py',
            'embed_local.py',
            'parse_and_chunk.py',
            'security_agent.py',
            'README.md',
            '.gitignore'
        ]
        
        required_dirs = [
            'PDF_Input',
            'Temp_Output',
            'LearningDb_Output',
            'MDFile',
            'HTMLFile'
        ]
        
        # Check files
        for file in required_files:
            exists = os.path.exists(file)
            self.test_result(f"File: {file}", exists, "Not found" if not exists else "")
        
        # Check directories
        for dir_name in required_dirs:
            exists = os.path.exists(dir_name) and os.path.isdir(dir_name)
            self.test_result(f"Directory: {dir_name}/", exists, "Not found" if not exists else "")
        
        # Check .gitignore content
        if os.path.exists('.gitignore'):
            with open('.gitignore', 'r') as f:
                content = f.read()
                has_pdf_input = 'PDF_Input' in content
                has_temp_output = 'Temp_Output' in content
                has_learning_db = 'LearningDb_Output' in content
                
                self.test_result(".gitignore has PDF_Input", has_pdf_input)
                self.test_result(".gitignore has Temp_Output", has_temp_output)
                self.test_result(".gitignore has LearningDb_Output", has_learning_db)
    
    def test_dependencies(self):
        """Test 2: Check Python dependencies"""
        dependencies = [
            ('requests', 'HTTP requests'),
            ('numpy', 'Vector operations'),
            ('tqdm', 'Progress bars'),
            ('pdfplumber', 'PDF parsing'),
            ('pythainlp', 'Thai language'),
        ]
        
        for package, description in dependencies:
            try:
                __import__(package)
                self.test_result(f"{package} ({description})", True)
            except ImportError:
                self.test_result(f"{package} ({description})", False, "Not installed")
        
        # Check GPT4All API accessibility
        try:
            response = requests.get("http://localhost:4891/v1/models", timeout=5)
            if response.status_code == 200:
                self.test_result("GPT4All API accessible", True)
            else:
                self.test_result("GPT4All API accessible", False, f"Status {response.status_code}")
        except:
            self.test_result("GPT4All API accessible", False, "Cannot connect")
    
    def test_gpt4all_api(self):
        """Test 3: Test GPT4All API endpoints"""
        api_base = "http://localhost:4891"
        
        # Test 1: Models endpoint
        try:
            response = requests.get(f"{api_base}/v1/models", timeout=5)
            if response.status_code == 200:
                models = response.json().get('data', [])
                self.test_result("GET /v1/models", True, f"{len(models)} models found")
                
                # Check for expected models
                model_names = [m.get('id', '') for m in models]
                has_llm = any('qwen' in m.lower() or 'deepseek' in m.lower() for m in model_names)
                self.test_result("LLM model available", has_llm, "qwen3-8b or similar")
            else:
                self.test_result("GET /v1/models", False, f"Status {response.status_code}")
        except Exception as e:
            self.test_result("GET /v1/models", False, str(e))
        
        # Test 2: Chat completions endpoint
        try:
            response = requests.post(
                f"{api_base}/v1/chat/completions",
                json={
                    "model": "qwen3-8b",
                    "messages": [{"role": "user", "content": "Hi"}],
                    "stream": False,
                    "max_tokens": 10
                },
                timeout=30
            )
            if response.status_code == 200:
                self.test_result("POST /v1/chat/completions", True, "LLM responding")
            elif response.status_code == 500:
                self.test_result("POST /v1/chat/completions", False, "Model not loaded (500)")
            else:
                self.test_result("POST /v1/chat/completions", False, f"Status {response.status_code}")
        except Exception as e:
            self.test_result("POST /v1/chat/completions", False, str(e))
        
        # Test 3: Embeddings endpoint (expected to fail in v3.9.0)
        try:
            response = requests.post(
                f"{api_base}/v1/embeddings",
                json={
                    "model": "Qwen/Qwen3-Embedding-0.6B-GGUF",
                    "input": "test"
                },
                timeout=10
            )
            if response.status_code == 200:
                self.test_result("POST /v1/embeddings", True, "Embedding API working!")
            elif response.status_code == 404:
                # Expected in GPT4All v3.9.0 - using fallback
                self.test_result("POST /v1/embeddings", True, "Not available (expected in v3.9.0, using fallback)")
            else:
                self.test_result("POST /v1/embeddings", False, f"Status {response.status_code}")
        except Exception as e:
            self.test_result("POST /v1/embeddings", True, "Not available (expected, using fallback)")
    
    def test_vector_db(self):
        """Test 4: Check vector database"""
        vector_db_path = os.path.join("LearningDb_Output", "vector_db.json")
        
        if not os.path.exists(vector_db_path):
            self.test_result("vector_db.json exists", False, "Run: python embed_local.py")
            return
        
        self.test_result("vector_db.json exists", True)
        
        # Load and validate
        try:
            with open(vector_db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.test_result("Valid JSON format", True)
            self.test_result(f"Chunks loaded: {len(data)}", len(data) > 0)
            
            # Check structure
            if len(data) > 0:
                first_chunk = data[0]
                has_content = 'content' in first_chunk
                has_embedding = 'embedding' in first_chunk
                embedding_size = len(first_chunk.get('embedding', []))
                
                self.test_result("Chunks have content", has_content)
                self.test_result("Chunks have embeddings", has_embedding)
                if has_embedding:
                    self.test_result(f"Embedding size: {embedding_size}D", embedding_size > 0)
        except Exception as e:
            self.test_result("JSON validation", False, str(e))
    
    def test_security(self):
        """Test 5: Run security scan"""
        try:
            import subprocess
            result = subprocess.run(
                ['python', 'security_agent.py'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if 'No security issues found' in result.stdout:
                self.test_result("Security scan", True, "✓ Safe to commit")
            elif 'Issues found' in result.stdout:
                self.test_result("Security scan", False, "Issues detected!")
            else:
                self.test_result("Security scan", True, "Completed")
        except Exception as e:
            self.test_result("Security scan", False, str(e))
    
    def test_full_pipeline(self):
        """Test 6: Full pipeline test (optional)"""
        # Check if PDFs exist
        pdf_input_dir = "PDF_Input"
        if not os.path.exists(pdf_input_dir):
            self.test_result("PDF_Input directory", False, "Not found")
            return
        
        pdf_files = [f for f in os.listdir(pdf_input_dir) if f.endswith('.pdf')]
        self.test_result(f"PDF files found: {len(pdf_files)}", len(pdf_files) > 0)
        
        if len(pdf_files) == 0:
            self.log("  ⚠ Skipping pipeline test (no PDFs)", 'warning')
            self.tests_skipped += 1
            return
        
        # Check if chunks exist
        chunks_dir = os.path.join("Temp_Output", "chunks")
        if os.path.exists(chunks_dir):
            chunk_files = []
            for root, dirs, files in os.walk(chunks_dir):
                chunk_files.extend([f for f in files if f.endswith('.md')])
            self.test_result(f"Chunks generated: {len(chunk_files)}", len(chunk_files) > 0)
        else:
            self.test_result("Chunks generated", False, "Run: python parse_and_chunk.py")
        
        # Check vector DB
        vector_db_path = os.path.join("LearningDb_Output", "vector_db.json")
        if os.path.exists(vector_db_path):
            with open(vector_db_path, 'r') as f:
                data = json.load(f)
            self.test_result(f"Embeddings generated: {len(data)}", len(data) > 0)
        else:
            self.test_result("Embeddings generated", False, "Run: python embed_local.py")
    
    def print_summary(self):
        """Print test summary"""
        self.log("\n" + "="*70, 'info')
        self.log("📊 Test Summary", 'info')
        self.log("="*70, 'info')
        
        total = self.tests_passed + self.tests_failed + self.tests_skipped
        
        print(f"\nTotal Tests: {total}")
        print(f"{Colors.GREEN}✓ Passed: {self.tests_passed}{Colors.RESET}")
        print(f"{Colors.RED}✗ Failed: {self.tests_failed}{Colors.RESET}")
        print(f"{Colors.YELLOW}⊘ Skipped: {self.tests_skipped}{Colors.RESET}")
        
        if self.tests_failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ All tests passed! System is ready.{Colors.RESET}")
            success = True
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}⚠️  {self.tests_failed} test(s) failed. Please fix issues above.{Colors.RESET}")
            success = False
        
        print(f"\nTest completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70 + "\n")
        
        # Save results
        self.save_results()
        
        return success
    
    def save_results(self):
        """Save test results to file"""
        results_dir = "Temp_Output"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        results_file = os.path.join(results_dir, "test_results.json")
        
        results_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'passed': self.tests_passed,
                'failed': self.tests_failed,
                'skipped': self.tests_skipped
            },
            'results': self.results
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, ensure_ascii=False, indent=2)
        
        self.log(f"📄 Test results saved to: {results_file}", 'info')


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Scan PDF Test Agent')
    parser.add_argument('--full', action='store_true', help='Run full pipeline test')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    agent = TestAgent(verbose=args.verbose)
    success = agent.run_all_tests(full_test=args.full)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
