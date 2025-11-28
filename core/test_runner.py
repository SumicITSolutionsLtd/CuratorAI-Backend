"""
Test runner utility for running and reporting test results.
"""
import subprocess
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional


class TestRunner:
    """Utility class to run tests and collect results."""
    
    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path(__file__).parent.parent
        self.results = {}
        self.pytest_cmd = self._find_pytest()
    
    def _find_pytest(self) -> List[str]:
        """Find pytest executable - try python -m pytest first, then direct pytest."""
        # Try python -m pytest first (most reliable)
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pytest', '--version'],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return [sys.executable, '-m', 'pytest']
        except:
            pass
        
        # Try direct pytest
        try:
            result = subprocess.run(
                ['pytest', '--version'],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return ['pytest']
        except:
            pass
        
        # Fallback: try common venv paths
        venv_paths = [
            self.base_dir / 'venv' / 'Scripts' / 'pytest.exe',
            self.base_dir / 'venv' / 'bin' / 'pytest',
            self.base_dir / '.venv' / 'Scripts' / 'pytest.exe',
            self.base_dir / '.venv' / 'bin' / 'pytest',
        ]
        
        for pytest_path in venv_paths:
            if pytest_path.exists():
                return [str(pytest_path)]
        
        # Last resort: use python -m pytest anyway
        return [sys.executable, '-m', 'pytest']
    
    def run_all_tests(self) -> Dict:
        """Run all tests and return results."""
        try:
            cmd = self.pytest_cmd + ['apps/', '-v', '--tb=short']
            result = subprocess.run(
                cmd,
                cwd=str(self.base_dir),
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                env=os.environ.copy()
            )
            
            # Parse summary from stdout
            summary = self._parse_summary(result.stdout)
            
            return {
                'success': result.returncode == 0,
                'exit_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'summary': summary
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Test execution timed out after 5 minutes'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def run_test_module(self, module: str) -> Dict:
        """Run tests for a specific module."""
        try:
            cmd = self.pytest_cmd + [f'apps/{module}/tests/', '-v', '--tb=short']
            result = subprocess.run(
                cmd,
                cwd=str(self.base_dir),
                capture_output=True,
                text=True,
                timeout=120,
                env=os.environ.copy()
            )
            
            return {
                'success': result.returncode == 0,
                'exit_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'summary': self._parse_summary(result.stdout)
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Test execution timed out'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def run_single_test(self, test_path: str) -> Dict:
        """Run a single test."""
        try:
            cmd = self.pytest_cmd + [test_path, '-v', '--tb=short']
            result = subprocess.run(
                cmd,
                cwd=str(self.base_dir),
                capture_output=True,
                text=True,
                timeout=60,
                env=os.environ.copy()
            )
            
            return {
                'success': result.returncode == 0,
                'exit_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'summary': self._parse_summary(result.stdout)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _parse_summary(self, stdout: str) -> Dict:
        """Parse pytest summary from stdout."""
        summary = {
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'errors': 0,
            'total': 0
        }
        
        import re
        lines = stdout.split('\n')
        
        # Look for the final summary line like "41 passed, 1 skipped, 12 warnings"
        for line in lines:
            line_lower = line.lower()
            # Match patterns like "X passed, Y failed, Z skipped"
            if 'passed' in line_lower or 'failed' in line_lower or 'skipped' in line_lower:
                # Extract numbers with their labels
                passed_match = re.search(r'(\d+)\s+passed', line_lower)
                failed_match = re.search(r'(\d+)\s+failed', line_lower)
                skipped_match = re.search(r'(\d+)\s+skipped', line_lower)
                error_match = re.search(r'(\d+)\s+error', line_lower)
                
                if passed_match:
                    summary['passed'] = int(passed_match.group(1))
                if failed_match:
                    summary['failed'] = int(failed_match.group(1))
                if skipped_match:
                    summary['skipped'] = int(skipped_match.group(1))
                if error_match:
                    summary['errors'] = int(error_match.group(1))
                
                summary['total'] = summary['passed'] + summary['failed'] + summary['skipped'] + summary['errors']
                
                # If we found a summary line, break (most accurate)
                if passed_match or failed_match:
                    break
        
        return summary
    
    def get_test_list(self) -> List[Dict]:
        """Get list of all available tests."""
        tests = []
        test_dirs = [
            'apps/accounts/tests',
            'apps/social/tests',
            'apps/lookbooks/tests',
            'apps/wardrobe/tests',
            'apps/outfits/tests',
            'apps/cart/tests',
            'apps/notifications/tests',
        ]
        
        for test_dir in test_dirs:
            test_path = self.base_dir / test_dir
            if test_path.exists():
                for test_file in test_path.glob('test_*.py'):
                    tests.append({
                        'module': test_dir.split('/')[1],
                        'file': test_file.name,
                        'path': str(test_file.relative_to(self.base_dir))
                    })
        
        return tests

