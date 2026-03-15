---
name: skill-v2-upgrader
description: "Upgrade and improve existing skills by analyzing functionality, creating comprehensive evals, running benchmarks, and suggesting improvements. Use when: user wants to improve an existing skill, add evals to a skill, benchmark skill performance, modernize skill structure, or verify skill works correctly. Don't use when: creating a skill from scratch (use skill-creator instead), or general skill questions."
version: 1.0.0
author: Rocco
---

# Skill V2 Upgrader 🚀

Automatically upgrade existing skills by analyzing their functionality, creating evals, running benchmarks, and suggesting improvements.

## What This Skill Does

1. **Analyzes** an existing skill's SKILL.md and functionality
2. **Creates** comprehensive evals covering main use cases
3. **Runs** evals with and without the skill (baseline comparison)
4. **Benchmarks** performance (time, tokens, success rate)
5. **Suggests** improvements based on results
6. **Updates** the skill with improvements

## Quick Start

```bash
# Upgrade a skill
Analyze skill at ~/clawdbot-skills/skills/my-skill and create comprehensive evals

# Run the full upgrade pipeline
1. Read and analyze the existing skill
2. Identify core functionality to test
3. Create evals using temporary directories (mktemp -d)
4. Run evals with and without skill
5. Compare results and generate benchmark
6. Suggest improvements
7. Update SKILL.md
```

## Workflow

### Step 1: Analyze Skill

Read the target skill's SKILL.md and identify:
- Main commands/functionality
- Key use cases
- Input/output patterns
- Dependencies
- Common failure modes

### Step 2: Create Evals

Generate evals in `<skill-name>-evals-workspace/evals/evals.json`:

```json
{
  "skill_name": "target-skill",
  "evals": [
    {
      "id": 1,
      "name": " descriptive-test-name",
      "prompt": "Test prompt using temporary directory",
      "expected_output": "What should happen",
      "assertions": [
        {
          "name": "check_file_exists",
          "type": "file_exists",
          "path": "*/output.txt",
          "description": "Output file should exist"
        }
      ]
    }
  ]
}
```

**Important Rules for Evals:**
- ✅ Use `mktemp -d` for temporary directories
- ✅ Add `trap cleanup EXIT` for automatic cleanup
- ✅ Never use `~/` or fixed paths for test files
- ✅ Keep tests focused on one functionality each
- ✅ Include both positive and edge cases

### Step 3: Run Evals

For each eval, spawn two subagents:
- **With skill**: Has access to the target skill
- **Without skill**: Baseline (discovers commands naturally)

**Structure:**
```
<skill-name>-evals-workspace/
├── evals/
│   └── evals.json
└── iteration-1/
    ├── eval-1-<name>/
    │   ├── eval_metadata.json
    │   ├── with_skill/outputs/
    │   │   └── result.json
    │   └── without_skill/outputs/
    │       └── result.json
    └── benchmark.json
```

### Step 4: Benchmark Results

Compare metrics between with-skill and without-skill runs:
- Success rate (which assertions passed)
- Runtime (duration_ms)
- Token usage (total_tokens)
- Quality (did it use best practices?)

### Step 5: Suggest Improvements

Based on benchmark results, identify:
- **Missing guidance**: Did baseline struggle? Add clearer instructions
- **Redundancy**: Did skill add no value? Remove or improve
- **Best practices**: Did skill use patterns worth documenting?
- **Edge cases**: What failed that should be handled?

### Step 6: Update Skill

Apply improvements to SKILL.md:
- Clarify unclear instructions
- Add examples for common patterns
- Document edge cases
- Remove redundant sections
- Update description for better triggering

## Eval Best Practices

### Directory Structure

```bash
# GOOD: Temporary directory with cleanup
TEST_DIR=$(mktemp -d)
trap "rm -rf $TEST_DIR" EXIT

# Run tests in $TEST_DIR
# Files auto-cleaned on exit

# BAD: Fixed paths that persist
# mkdir ~/my-test-vault  # DON'T DO THIS
```

### Assertion Types

- `file_exists`: Check file was created
- `file_contains`: Check file has expected content
- `file_not_exists`: Ensure file wasn't created (negative tests)
- `output_contains`: Check command output
- `output_matches`: Regex match on output

### Test Coverage

Create evals for:
1. **Happy path**: Normal usage works
2. **Edge cases**: Empty inputs, invalid args
3. **Error handling**: Graceful failures
4. **Integration**: Multiple commands together
5. **Cleanup**: No leftover files

## Example Eval Set

For a skill like `clawvault`:

```json
{
  "skill_name": "clawvault",
  "evals": [
    {
      "id": 1,
      "name": "init-vault",
      "prompt": "Use mktemp -d, init clawvault, verify structure, cleanup",
      "assertions": [
        {"name": "vault_created", "type": "file_exists", "path": "*/.clawvault.json"}
      ]
    },
    {
      "id": 2,
      "name": "remember-entity",
      "prompt": "Create temp dir, init vault, remember decision, verify file, cleanup",
      "assertions": [
        {"name": "file_created", "type": "file_exists", "path": "*/decisions/*.md"},
        {"name": "has_frontmatter", "type": "file_contains", "path": "*/decisions/*.md", "content": "type: decision"}
      ]
    }
  ]
}
```

## Scripts

Use bundled scripts for automation:

```bash
# scripts/generate_evals.py - Generate evals from skill analysis
# scripts/run_comparison.py - Run with/without skill comparison
# scripts/analyze_results.py - Analyze benchmark and suggest improvements
```

## Success Criteria

An upgrade is successful when:
- ✅ All evals pass with skill
- ✅ Skill shows clear value over baseline (faster, better, or easier)
- ✅ No persistent test files left on system
- ✅ SKILL.md is clearer and more complete
- ✅ Description triggers appropriately

## Compatibility

- Requires: subagents for parallel execution
- Optional: skill-creator for description optimization
- Works with: Any skill that has verifiable outputs

## Tips

1. **Start small**: Create 3-5 evals first, expand based on results
2. **Focus on value**: If baseline works fine, skill may not be needed
3. **Document findings**: Note why changes were made
4. **Iterate**: Run evals, improve, repeat
5. **Clean up**: Always verify no test files persist

---

Remember: The goal is to make skills that provide clear value over baseline Claude capabilities.
