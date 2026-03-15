#!/usr/bin/env python3
"""
Analyze benchmark results and suggest skill improvements.
"""

import json
import sys
from pathlib import Path

def load_results(workspace: Path):
    """Load all result.json files from workspace."""
    results = []
    
    iteration_dir = workspace / "iteration-1"
    if not iteration_dir.exists():
        return results
    
    for eval_dir in iteration_dir.iterdir():
        if not eval_dir.is_dir() or not eval_dir.name.startswith("eval-"):
            continue
        
        for config in ["with_skill", "without_skill"]:
            result_file = eval_dir / config / "outputs" / "result.json"
            if result_file.exists():
                with open(result_file) as f:
                    data = json.load(f)
                    data["_eval"] = eval_dir.name
                    data["_config"] = config
                    results.append(data)
    
    return results

def analyze(results: list):
    """Analyze results and generate suggestions."""
    
    # Group by eval
    by_eval = {}
    for r in results:
        eval_name = r['_eval']
        if eval_name not in by_eval:
            by_eval[eval_name] = {}
        by_eval[eval_name][r['_config']] = r
    
    suggestions = []
    
    for eval_name, configs in by_eval.items():
        with_skill = configs.get('with_skill', {})
        baseline = configs.get('without_skill', {})
        
        # Compare success
        with_success = with_skill.get('status') == 'completed'
        base_success = baseline.get('status') == 'completed'
        
        if with_success and not base_success:
            suggestions.append({
                "eval": eval_name,
                "type": "value_add",
                "message": "Skill provides clear value - baseline failed but skill succeeded"
            })
        elif not with_success and base_success:
            suggestions.append({
                "eval": eval_name,
                "type": "needs_fix",
                "message": "Skill may be broken - baseline succeeded but skill failed"
            })
        elif with_success and base_success:
            # Compare tokens if available
            with_tokens = with_skill.get('stats', {}).get('total_tokens', 0)
            base_tokens = baseline.get('stats', {}).get('total_tokens', 0)
            
            if with_tokens > base_tokens * 1.5:
                suggestions.append({
                    "eval": eval_name,
                    "type": "optimization",
                    "message": f"Skill uses {with_tokens} vs baseline {base_tokens} tokens - consider simplifying"
                })
    
    return suggestions

def main():
    if len(sys.argv) < 2:
        print("Usage: analyze_results.py <evals-workspace>")
        sys.exit(1)
    
    workspace = Path(sys.argv[1])
    
    print(f"Analyzing results in {workspace}")
    results = load_results(workspace)
    
    if not results:
        print("No results found")
        sys.exit(1)
    
    print(f"Loaded {len(results)} result files")
    
    suggestions = analyze(results)
    
    print("\n" + "="*60)
    print("ANALYSIS RESULTS")
    print("="*60)
    
    for s in suggestions:
        print(f"\n[{s['type'].upper()}] {s['eval']}")
        print(f"  → {s['message']}")
    
    # Save suggestions
    suggestions_file = workspace / "iteration-1" / "suggestions.json"
    with open(suggestions_file, 'w') as f:
        json.dump(suggestions, f, indent=2)
    
    print(f"\nSuggestions saved to: {suggestions_file}")

if __name__ == "__main__":
    main()
