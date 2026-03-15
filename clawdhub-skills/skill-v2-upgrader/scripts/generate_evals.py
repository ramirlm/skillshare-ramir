#!/usr/bin/env python3
"""
Generate evals for a skill based on its SKILL.md analysis.
"""

import json
import sys
import re
from pathlib import Path

def analyze_skill(skill_path: str):
    """Analyze SKILL.md and extract testable functionality."""
    skill_file = Path(skill_path) / "SKILL.md"
    
    if not skill_file.exists():
        print(f"Error: {skill_file} not found")
        sys.exit(1)
    
    content = skill_file.read_text()
    
    # Extract code blocks (examples)
    code_blocks = re.findall(r'```(?:\w+)?\n(.*?)```', content, re.DOTALL)
    
    # Extract commands (lines starting with command names)
    commands = []
    for block in code_blocks:
        lines = block.strip().split('\n')
        for line in lines:
            # Look for command patterns
            if line.startswith('clawvault') or line.startswith('openclaw'):
                commands.append(line.strip())
    
    # Extract sections
    sections = re.findall(r'##+\s+(.+)', content)
    
    return {
        "commands": list(set(commands)),
        "sections": sections,
        "content": content
    }

def generate_evals(skill_name: str, analysis: dict):
    """Generate evals based on analysis."""
    evals = []
    
    # Basic init eval
    evals.append({
        "id": 1,
        "name": "basic-init",
        "prompt": f"Use mktemp -d to create temp dir. Initialize the tool, verify it works, cleanup with trap.",
        "expected_output": "Tool initializes correctly in temporary directory",
        "assertions": [
            {"name": "command_succeeds", "type": "output_contains", "content": "success"}
        ]
    })
    
    # Generate evals for each unique command pattern
    for i, cmd in enumerate(analysis["commands"][:5], start=2):  # Limit to 5
        cmd_name = cmd.split()[0] if cmd.split() else "command"
        evals.append({
            "id": i,
            "name": f"{cmd_name}-usage",
            "prompt": f"Use mktemp -d. Execute: {cmd}. Verify output. Cleanup.",
            "expected_output": f"Command executes successfully",
            "assertions": [
                {"name": "no_errors", "type": "output_not_contains", "content": "error"}
            ]
        })
    
    return {
        "skill_name": skill_name,
        "evals": evals
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: generate_evals.py <skill-path>")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    skill_name = Path(skill_path).name
    
    print(f"Analyzing skill: {skill_name}")
    analysis = analyze_skill(skill_path)
    
    print(f"Found {len(analysis['commands'])} unique commands")
    print(f"Found {len(analysis['sections'])} sections")
    
    evals = generate_evals(skill_name, analysis)
    
    # Write evals.json
    workspace = Path(f"{skill_name}-evals-workspace")
    workspace.mkdir(exist_ok=True)
    (workspace / "evals").mkdir(exist_ok=True)
    
    evals_file = workspace / "evals" / "evals.json"
    with open(evals_file, 'w') as f:
        json.dump(evals, f, indent=2)
    
    print(f"Generated {len(evals['evals'])} evals")
    print(f"Saved to: {evals_file}")

if __name__ == "__main__":
    main()
