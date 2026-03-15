---
name: perplexity-brainstorm
description: "Deep research + structured brainstorming workflow. Use when user wants to explore a topic deeply before ideating solutions. Combines Perplexity (deep research), brainstorming (structured ideation), and iterative search (web_search/perplexity) as needed. Triggers: 'research and brainstorm X', 'deep dive into Y', 'explore Z comprehensively', or any request combining research + ideation."
---

# Perplexity Brainstorm

## Overview

This skill combines deep research capabilities with structured brainstorming to help explore topics comprehensively before implementation. It uses a three-phase approach:

1. **Deep Research** - Perplexity search for comprehensive initial understanding
2. **Structured Ideation** - obra/superpowers@brainstorming for collaborative refinement
3. **Iterative Exploration** - Additional searches (web_search or perplexity) as needed

## Prerequisites

**IMPORTANT:** Before using this skill, verify these dependencies are installed:

### 1. Perplexity Skill
```bash
# Check if installed
ls ~/.openclaw/skills/perplexity/SKILL.md

# If missing, install
npx skills add softaworks/agent-toolkit@perplexity -g -y
ln -sf ~/.agents/skills/perplexity ~/.openclaw/skills/perplexity
```

### 2. Brainstorming Skill
```bash
# Check if installed
ls ~/.agents/skills/brainstorming/SKILL.md

# If missing, install
npx skills add obra/superpowers@brainstorming -g -y
```

### 3. Perplexity MCP Server (Optional but Recommended)

The perplexity skill uses MCP (Model Context Protocol). If using MCP:
- Ensure `mcp-servers.json` has perplexity configured
- Perplexity API key set in environment

**Fallback:** If Perplexity/MCP unavailable, the skill automatically falls back to **xAI deep search** (X.AI) for research phase.

## When to Use

Use this skill when the user wants to:
- Research a topic deeply before making decisions
- Explore solutions comprehensively before implementation
- Combine external knowledge with structured thinking
- Validate assumptions with current information before brainstorming

**Example triggers:**
- "Research and brainstorm solutions for X"
- "Deep dive into Y and help me design Z"
- "Explore A comprehensively before building B"
- "What's the current state of X? Let's brainstorm from there"

## The Workflow

### Phase 1: Deep Research (Perplexity)

Start with Perplexity search to gather comprehensive, current information about the topic.

**Perplexity skill location:** `~/.openclaw/skills/perplexity/SKILL.md`

**Steps:**
1. Read the perplexity skill if not already in context
2. Formulate focused search query based on user's topic
3. Execute perplexity search (uses Perplexity API)
4. Summarize key findings for the user (bullet points, 200-300 words)

**Example:**
```
Topic: "Build a notification system for our app"
Perplexity query: "modern notification system architecture best practices 2026 real-time push"
```

**Search tips:**
- Include year/timeframe for current information
- Add technical keywords for deeper results
- Focus on implementation patterns, not just concepts

### Phase 2: Structured Brainstorming

After gathering research, trigger the brainstorming skill to explore design options.

**Brainstorming skill location:** `~/.agents/skills/brainstorming/SKILL.md`

**Steps:**
1. Read the brainstorming skill
2. Present research findings to user
3. Follow brainstorming process:
   - Understand project context (check files, docs, commits)
   - Ask questions one at a time to refine the idea
   - Propose 2-3 approaches with trade-offs
   - Present design in sections (200-300 words each)
   - Validate each section before continuing

**Key principle from brainstorming:**
- One question at a time
- Multiple choice questions preferred
- YAGNI ruthlessly (remove unnecessary features)
- Incremental validation

### Phase 3: Iterative Exploration

During brainstorming, additional research may be needed. Choose the appropriate tool:

**Use web_search (native tool) when:**
- Quick fact-checking needed
- Specific library/API documentation lookup
- Recent news or updates check
- Simple queries with clear answers

**Use Perplexity again when:**
- Deep analysis of a sub-topic needed
- Comparing multiple approaches comprehensively
- Understanding complex technical patterns
- Validating architectural decisions

**Decision flow:**
```
Need more info?
├─ Simple/quick answer → web_search
└─ Deep/comprehensive → perplexity (read skill again)
```

## Integration Points

### With Project Context

Before starting brainstorming phase, always check:
- Current project files and structure
- Existing documentation in `docs/`
- Recent git commits
- Related PRDs in `state/prd-jobs.json` (if applicable)

### Output Documentation

After completing the brainstorming phase:

1. **Design document** - Written to `docs/plans/YYYY-MM-DD-<topic>-design.md`
2. **Research summary** - Include perplexity findings at the top
3. **References** - Link to searched resources when available
4. **Git commit** - Commit the design document

**Example document structure:**
```markdown
# [Topic] Design - YYYY-MM-DD

## Research Summary
[Perplexity findings - key insights, trends, best practices]

## Design Options
[2-3 approaches explored during brainstorming]

## Recommended Approach
[Validated design with architecture, components, data flow]

## References
- Perplexity search: [query used]
- Additional searches: [web_search queries if any]
```

## Best Practices

### Research Quality

- **Be specific** - "notification system push architecture patterns" > "notifications"
- **Include timeframe** - Add "2026" or "latest" for current information
- **Technical depth** - Include framework/language names when relevant
- **Avoid jargon overload** - Balance specificity with clarity

### Brainstorming Quality

- **Context-aware** - Reference research findings during questioning
- **Practical** - Focus on implementable solutions, not theory
- **Incremental** - Don't dump entire design at once
- **Flexible** - Be ready to research more if gaps appear

### Iteration Strategy

Don't over-research:
1. Start with one perplexity search
2. Move to brainstorming quickly
3. Only search again when specific gaps appear
4. Prefer focused follow-up searches over broad ones

## Example Session

**User:** "Research and brainstorm a real-time notification system for our web app"

**Phase 1 (Research):**
```
[Read perplexity skill]
Searching Perplexity for: "real-time notification system architecture websockets 2026 best practices"

Key findings:
- WebSockets vs Server-Sent Events trade-offs
- Popular libraries: Socket.io, Pusher, Ably
- Scaling considerations for 10k+ concurrent connections
- Browser notification API integration patterns
```

**Phase 2 (Brainstorm):**
```
[Read brainstorming skill]

Based on research, I see 3 main approaches:

1. **WebSocket-based (Socket.io)** - Full duplex, complex scaling
2. **SSE + polling fallback** - Simpler, unidirectional
3. **Third-party (Pusher/Ably)** - Fastest setup, ongoing cost

Let me understand your constraints better:
What's your expected concurrent user count? 
A) < 1,000
B) 1,000 - 10,000  
C) > 10,000
```

**Phase 3 (Iterate if needed):**
```
[User chooses option B, asks about Socket.io scaling]

Let me research Socket.io scaling patterns specifically...

[web_search: "socket.io scaling 10000 concurrent connections redis"]

Found: Redis adapter pattern for horizontal scaling...
```

## Troubleshooting

**Perplexity search fails:**
- Check API key in `~/.openclaw/skills/perplexity/`
- Perplexity skill automatically falls back to xAI deep search
- Note limitation in findings summary if using fallback

**Brainstorming skill not found:**
- Verify installation: `ls ~/.agents/skills/brainstorming/`
- Install if missing: `npx skills add obra/superpowers@brainstorming -g -y`
- Fall back to manual structured questioning

**Research → Brainstorm disconnect:**
- Always summarize research before starting questions
- Reference specific findings during brainstorming
- Save research summary to paste if needed

## Advanced Patterns

### Multi-Domain Research

For complex topics spanning multiple domains:

```
1. Perplexity search: "domain A + domain B integration patterns"
2. Brainstorm: Focus on integration layer
3. Perplexity search: "domain A specific implementation"
4. Perplexity search: "domain B specific implementation"  
5. Brainstorm: Refine complete design
```

### Competitive Analysis

When researching existing solutions:

```
1. Perplexity: "product X vs Y vs Z comparison 2026"
2. Brainstorm: Discuss findings, identify gaps
3. Perplexity or web_search: Check specific features/pricing if needed
4. Brainstorm: Design differentiated approach
```

### Technology Evaluation

When choosing between technologies:

```
1. Perplexity: "technology A vs B production experience 2026"
2. Brainstorm: Present trade-offs, ask about constraints
3. Perplexity: "technology [chosen] implementation patterns"
4. Brainstorm: Design concrete implementation
```

## Notes

- Perplexity skill uses MCP or falls back to xAI deep search automatically
- For simple/quick queries, web_search tool can be used directly to save tokens
- Brainstorming skill writes to `docs/plans/` automatically
- Research quality improves with specific, focused queries
- Don't research forever - move to brainstorming after initial findings
