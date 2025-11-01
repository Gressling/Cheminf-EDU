"""
Fix broken function definitions from the previous fix
"""

import os
import re

def fix_broken_function_def(content):
    """Fix function definitions that were truncated"""
    
    # Pattern to find broken function definitions followed by docstring
    pattern = r'(def\s+\w+\([^)]*),\s*\n\s*"""([^"]+)"""\s*\n\s*return\s+\[\]\s*#\s*Placeholder return'
    
    def replace_func(match):
        func_start = match.group(1)
        docstring = match.group(2)
        # Add closing parenthesis and complete parameters
        return f'{func_start}, *args, **kwargs):\n    """{docstring}"""\n    return []  # Placeholder return'
    
    return re.sub(pattern, replace_func, content, flags=re.MULTILINE)

def main():
    """Fix broken function definitions"""
    
    files_to_fix = [
        "cheminf/reactions/ui_reactions.py",
        "cheminf/reactions/ui_reactionparticipants.py",
        "cheminf/reactions/ui_overview.py",
        "cheminf/reactions/rest_api.py",
        "cheminf/lims_experiments/ui_experiments.py",
        "cheminf/lims_experiments/ui_samples.py", 
        "cheminf/lims_experiments/ui_measurements.py",
        "cheminf/lims_experiments/rest_api.py",
    ]
    
    for filepath in files_to_fix:
        if os.path.exists(filepath):
            print(f"Checking {filepath}...")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for syntax errors by trying to compile
            try:
                compile(content, filepath, 'exec')
                print(f"  ✓ {filepath} is syntactically correct")
            except SyntaxError as e:
                print(f"  ! Syntax error in {filepath}: {e}")
                
                # Try to fix common issues
                fixed_content = fix_broken_function_def(content)
                
                # If that didn't work, try a more aggressive fix
                if fixed_content == content:
                    lines = content.split('\n')
                    fixed_lines = []
                    
                    for i, line in enumerate(lines):
                        # Look for incomplete function definitions
                        if line.strip().startswith('def ') and line.strip().endswith(','):
                            # Find the next line that isn't indented (start of function body)
                            j = i + 1
                            while j < len(lines) and (lines[j].strip() == '' or lines[j].startswith('    ')):
                                if '"""' in lines[j] and 'migration' in lines[j]:
                                    # This is our placeholder function
                                    # Fix the function definition
                                    line = line.rstrip(',') + ', *args, **kwargs):'
                                    break
                                j += 1
                        fixed_lines.append(line)
                    
                    fixed_content = '\n'.join(fixed_lines)
                
                # Write the fixed content
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                # Verify the fix
                try:
                    compile(fixed_content, filepath, 'exec')
                    print(f"  ✓ Fixed {filepath}")
                except SyntaxError as e2:
                    print(f"  ! Still has syntax errors: {e2}")

if __name__ == "__main__":
    main()