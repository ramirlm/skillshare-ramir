#!/usr/bin/env python3
"""
Run comparison between with-skill and without-skill for all evals.
"""

import json
import sys
from pathlib import Path

def create_subagent_task(eval_item: dict, skill_path: str = None) -> dict:
    """Create a subagent task for an eval."""
    
    skill_line = f"- Skill path: {skill_path}\n" if skill_path else ""
    
    task = f"""Execute this task{' (NO SKILL - baseline)' if not skill_path else ''}:
{skill_line}- Task: {eval_item['prompt']}
- Important: Use mktemp -d for temp dir and trap for cleanup
- Save outputs to: <eval-workspace>/iteration-1/eval-{eval_item['id']}-{'with_skill' if skill_path else 'baseline'}/outputs/
- Save summary to: result.json"""
    
    return {
        "runtime": "subagent",
        "mode": "run",
        "task": task,
        "label": f"{eval_item['name']}-{'with-skill' if skill_path else 'baseline'}"
    }

def main():
    if len(sys.argv) < 3:
        print("Usage: run_comparison.py <skill-path> <evals-workspace>")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    workspace = Path(sys.argv[2])
    
    evals_file = workspace / "evals" / "evals.json"
    if not evals_file.exists():
        print(f"Error: {evals_file} not found")
        sys.exit(1)
    
    with open(evals_file) as f:
        evals_data = json.load(f)
    
    print(f"Preparing to run {len(evals_data['evals'])} evals...")
    print(f"With skill: {skill_path}")
    print(f"Workspace: {workspace}")
    
    # Create directory structure
    iteration_dir = workspace / "iteration-1"
    iteration_dir.mkdir(exist_ok=True)
    
    for eval_item in evals_data['evals']:
        eval_dir = iteration_dir / f"eval-{eval_item['id']}-{eval_item['name']}"
        (eval_dir / "with_skill" / "outputs").mkdir(parents=True, exist_ok=True)
        (eval_dir / "without_skill" / "outputs").mkdir(parents=True, exist_ok=True)
        
        # Write metadata
        metadata = {
            "eval_id": eval_item['id'],
            "eval_name": eval_item['name'],
            "prompt": eval_item['prompt'],
            "assertions": eval_item.get('assertions', [])
        }
        with open(eval_dir / "eval_metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
    
    print(f"\nDirectory structure created in {iteration_dir}")
    print("\nReady to spawn subagents:")
    print(f"- {len(evals_data['evals'])} with skill")
    print(f"- {len(evals_data['evals'])} without skill (baseline)")

if __name__ == "__main__":
    main()
