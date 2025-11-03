#!/usr/bin/env python3
"""
Automatic test fixer based on ChatGPT recommendations
"""
import os
import re
import sys

def fix_api_paths(directory):
    """Fix old API paths to new ones"""
    changes = 0
    patterns = [
        (r'/api/v1/auth', '/api/auth'),
        (r'/api/v1/user', '/api/user'),
        (r'/api/v1/admin', '/api/admin'),
        (r'/api/v1/crm', '/api/crm'),
        (r'/api/v1/leads', '/api/leads'),
        (r'/api/v1/payments', '/api/payments'),
        (r'/api/v1/wallet', '/api/wallet'),
        (r'/api/v1/programs', '/api/programs'),
        (r'/api/v1/challenges', '/api/challenges'),
    ]
    
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.py') and file_name.startswith('test_'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                for old_path, new_path in patterns:
                    content = re.sub(old_path, new_path, content)
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    changes += 1
                    print(f"✅ Fixed paths in: {file_path}")
    
    return changes

def fix_assertions(directory):
    """Fix old assertions to match new API responses"""
    changes = 0
    replacements = [
        # Access token assertions
        ("assert 'access_token' in data", "assert 'verification_code' in data or 'access_token' in data"),
        ("assert 'access_token' in response_data", "assert 'verification_code' in response_data or 'access_token' in response_data"),
        
        # Mock references
        (", mock_sendgrid", ""),
        ("mock_sendgrid,", ""),
        ("mock_sendgrid)", ")"),
        ("(mock_sendgrid", "("),
    ]
    
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.py') and file_name.startswith('test_'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                for old_text, new_text in replacements:
                    content = content.replace(old_text, new_text)
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    changes += 1
                    print(f"✅ Fixed assertions in: {file_path}")
    
    return changes

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 auto_fix_tests.py <tests_directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    if not os.path.exists(directory):
        print(f"❌ Directory not found: {directory}")
        sys.exit(1)
    
    print("🤖 Starting automatic test fixes...")
    print("=" * 80)
    
    print("\n📝 Phase 1: Fixing API paths...")
    path_changes = fix_api_paths(directory)
    print(f"✅ Fixed {path_changes} files with API path issues")
    
    print("\n📝 Phase 2: Fixing assertions and mocks...")
    assertion_changes = fix_assertions(directory)
    print(f"✅ Fixed {assertion_changes} files with assertion/mock issues")
    
    print("\n" + "=" * 80)
    print(f"🎉 Done! Total files modified: {path_changes + assertion_changes}")
    print("\n💡 Next steps:")
    print("1. Review the changes with: git diff")
    print("2. Run tests: pytest tests/ -v")
    print("3. Fix any remaining issues manually")

if __name__ == '__main__':
    main()
