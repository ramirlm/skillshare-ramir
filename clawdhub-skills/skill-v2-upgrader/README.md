# Skill V2 Upgrader 🚀

Automatically upgrade existing skills by creating evals, running benchmarks, and suggesting improvements.

## Quick Start

```bash
# Place skill in the correct location
mkdir -p ~/clawdbot-skills/skills/skill-v2-upgrader
# Copy SKILL.md and scripts/ here

# Use the skill:
# "Upgrade the skill at ~/clawdbot-skills/skills/my-skill"
```

## What It Does

1. **Analyze** - Reads SKILL.md, identifies testable functionality
2. **Generate Evals** - Creates evals.json with comprehensive tests
3. **Run Comparison** - Tests with and without skill (baseline)
4. **Benchmark** - Compares time, tokens, success rate
5. **Suggest** - Identifies improvements based on results
6. **Update** - Applies improvements to SKILL.md

## Key Features

- ✅ Automatic eval generation from skill analysis
- ✅ Baseline comparison (with vs without skill)
- ✅ Temporary directory usage (no persistent test files)
- ✅ Automatic cleanup (mktemp + trap)
- ✅ Benchmark reporting
- ✅ Improvement suggestions

## Workflow

```
Skill Analysis → Generate Evals → Run Comparison → Benchmark → Improve → Update
```

## Example Usage

```
User: "Upgrade the clawvault skill"
→ Read ~/clawdbot-skills/skills/clawvault/SKILL.md
→ Identify commands: init, remember, search, task, etc.
→ Generate evals for each command
→ Run 10 evals × 2 configs (with/without skill)
→ Compare results
→ Suggest improvements
→ Update SKILL.md
```

## Scripts

| Script | Purpose |
|--------|---------|
| `generate_evals.py` | Analyze skill and create evals.json |
| `run_comparison.py` | Set up directory structure for runs |
| `analyze_results.py` | Analyze benchmark and suggest improvements |

## Output Structure

```
<skill-name>-evals-workspace/
├── evals/
│   └── evals.json          # Generated test cases
└── iteration-1/
    ├── eval-1-init/
    │   ├── eval_metadata.json
    │   ├── with_skill/outputs/result.json
    │   └── without_skill/outputs/result.json
    ├── eval-2-remember/
    │   └── ...
    ├── benchmark.json      # Aggregated metrics
    └── suggestions.json    # Improvement suggestions
```

## Rules Enforced

1. **Temporary directories only** - `mktemp -d`, never `~/`
2. **Automatic cleanup** - `trap cleanup EXIT`
3. **No persistent test files** - Everything in /tmp
4. **Focused tests** - One functionality per eval
5. **Baseline comparison** - Always test with and without skill

## Success Criteria

An upgrade is successful when:
- All evals pass with skill
- Skill shows clear value over baseline
- No test files left on system
- SKILL.md is clearer
- Description triggers appropriately

---

Created: 2026-03-07
Version: 1.0.0
