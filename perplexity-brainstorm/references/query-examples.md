# Perplexity Query Examples

## Overview

This reference provides proven query patterns for effective Perplexity searches. Use these patterns to craft queries that yield comprehensive, actionable results.

## Query Patterns by Use Case

### Technology Evaluation

**Pattern:** `[technology A] vs [technology B] production experience [year] [specific criteria]`

**Examples:**
- "React vs Vue production experience 2026 performance scalability"
- "PostgreSQL vs MongoDB production use cases 2026 ACID transactions"
- "Kubernetes vs Docker Swarm production deployment 2026 small team"
- "Next.js vs Remix SSR framework 2026 developer experience"

**Why this works:**
- "production experience" filters out toy examples
- Year ensures current information
- Specific criteria focuses results

---

### Architecture Patterns

**Pattern:** `[system type] architecture patterns [scale] [year] best practices`

**Examples:**
- "real-time notification system architecture 10000 users 2026 best practices"
- "microservices API gateway patterns 2026 authentication authorization"
- "event-driven architecture patterns 2026 message queue reliability"
- "serverless architecture cold start optimization 2026"

**Why this works:**
- "architecture patterns" targets design discussions
- Scale helps filter relevant examples
- "best practices" surfaces vetted approaches

---

### Implementation Guides

**Pattern:** `[technology] [specific feature] implementation [year] production`

**Examples:**
- "Socket.io Redis adapter implementation 2026 production scaling"
- "Stripe webhooks implementation 2026 production idempotency"
- "OAuth2 PKCE flow implementation 2026 security best practices"
- "React Server Components implementation 2026 data fetching patterns"

**Why this works:**
- Specific feature narrows results
- "implementation" targets how-to content
- "production" filters enterprise-grade info

---

### Problem Solving

**Pattern:** `[problem statement] solutions [context] [year]`

**Examples:**
- "database connection pooling exhaustion solutions Node.js 2026"
- "Redis memory optimization solutions large datasets 2026"
- "WebSocket reconnection strategies mobile apps 2026"
- "rate limiting API gateway solutions high throughput 2026"

**Why this works:**
- Problem-first approach
- Context narrows to relevant solutions
- Assumes others have solved this before

---

### Current State / Trends

**Pattern:** `state of [domain] [year] trends adoption`

**Examples:**
- "state of JavaScript frameworks 2026 trends adoption"
- "state of AI code generation 2026 developer productivity"
- "state of headless CMS 2026 market leaders features"
- "state of web performance 2026 Core Web Vitals standards"

**Why this works:**
- "state of" surfaces overview content
- "trends adoption" focuses on what's actually used
- Great for landscape understanding

---

### Debugging / Troubleshooting

**Pattern:** `[error/symptom] causes [technology stack] [year]`

**Examples:**
- "memory leak causes Node.js event emitters 2026"
- "CORS errors causes Next.js API routes 2026"
- "slow query causes PostgreSQL JSON fields 2026"
- "WebSocket disconnections causes mobile networks 2026"

**Why this works:**
- Symptom-first matches how users search
- Technology stack filters relevant results
- "causes" surfaces root cause analysis

---

### Security / Compliance

**Pattern:** `[technology] security [specific concern] [year] best practices`

**Examples:**
- "JWT token security XSS CSRF 2026 best practices"
- "S3 bucket security public access prevention 2026"
- "API authentication security mobile apps 2026 token storage"
- "database security SQL injection prevention 2026 parameterized queries"

**Why this works:**
- Specific concern (XSS, CSRF, etc.) targets exact issue
- "best practices" surfaces vetted approaches
- Security context attracts detailed explanations

---

### Migration / Upgrade

**Pattern:** `migrate from [old] to [new] [year] production experience`

**Examples:**
- "migrate from REST to GraphQL 2026 production experience breaking changes"
- "migrate from JavaScript to TypeScript 2026 incremental adoption"
- "migrate from MongoDB to PostgreSQL 2026 data model translation"
- "upgrade Next.js 14 to 15 2026 breaking changes migration guide"

**Why this works:**
- "production experience" surfaces real-world challenges
- "breaking changes" anticipates pain points
- Attracts case studies and war stories

---

### Performance Optimization

**Pattern:** `[technology] performance optimization [specific metric] [year]`

**Examples:**
- "React performance optimization bundle size 2026 code splitting"
- "PostgreSQL query performance optimization large tables 2026 indexing"
- "Redis performance optimization memory usage 2026 eviction policies"
- "Next.js performance optimization LCP FCP 2026 Core Web Vitals"

**Why this works:**
- Specific metric (bundle size, LCP, etc.) focuses results
- "optimization" targets actionable advice
- Technique hints (code splitting, indexing) guide search

---

### Scaling Strategies

**Pattern:** `scale [system] from [current] to [target] [year] strategies`

**Examples:**
- "scale WebSocket server from 1000 to 100000 connections 2026 strategies"
- "scale PostgreSQL from 1TB to 10TB 2026 partitioning sharding"
- "scale API from 100 to 10000 RPS 2026 caching load balancing"
- "scale team from 5 to 50 developers 2026 monorepo strategies"

**Why this works:**
- Concrete numbers make results actionable
- "strategies" surfaces architectural approaches
- Technique hints guide toward solutions

---

## Anti-Patterns (Avoid These)

### Too Vague

❌ "notifications"
✅ "real-time notification system architecture WebSockets 2026"

**Problem:** Vague queries return generic, surface-level content

---

### Too Narrow

❌ "Socket.io version 4.5.2 Redis adapter configuration parameter timeout value"
✅ "Socket.io Redis adapter configuration 2026 production settings"

**Problem:** Over-specification might miss relevant content with slightly different versions/terminology

---

### Missing Context

❌ "best framework 2026"
✅ "best SSR framework React ecosystem 2026 production performance"

**Problem:** "Best" is subjective; add context for meaningful comparisons

---

### No Time Filter

❌ "React performance optimization"
✅ "React performance optimization 2026 React 19"

**Problem:** Old content may be outdated or irrelevant

---

### Jargon Overload

❌ "isomorphic universal SSR CSR hydration reconciliation optimization"
✅ "server-side rendering optimization 2026 React Next.js"

**Problem:** Too much jargon may miss well-explained content using simpler terms

---

## Query Refinement Workflow

When initial query doesn't yield good results:

1. **Start broad:** "notification system architecture"
2. **Add specificity:** "real-time notification system WebSockets"
3. **Add scale/context:** "real-time notification system WebSockets 10000 users"
4. **Add year/tech:** "real-time notification system WebSockets 10000 users 2026 Node.js"
5. **Add desired outcome:** "real-time notification system WebSockets 10000 users 2026 Node.js production reliability"

Stop when results become relevant and actionable.

---

## Domain-Specific Tips

### Frontend Development
- Include framework name (React, Vue, Svelte)
- Mention performance metrics (LCP, FCP, bundle size)
- Add deployment target (Vercel, Netlify, static)

### Backend Development
- Include language/runtime (Node.js, Python, Go)
- Mention scale (requests/sec, concurrent connections)
- Add infrastructure (AWS, GCP, Kubernetes)

### DevOps / Infrastructure
- Include cloud provider (AWS, GCP, Azure)
- Mention scale (servers, regions, traffic)
- Add specific services (ECS, Lambda, RDS)

### Data / Database
- Include DB type (PostgreSQL, MongoDB, Redis)
- Mention data size (rows, GB, TB)
- Add query patterns (read-heavy, write-heavy, analytical)

---

## Combining with Brainstorming

**Research phase queries** should be broad and exploratory:
- "state of real-time web technologies 2026"
- "notification system architecture patterns 2026"

**Brainstorming phase queries** should be specific and actionable:
- "Socket.io Redis adapter horizontal scaling 2026"
- "Browser Push API implementation 2026 service workers"

**Principle:** Start wide (research), then narrow (brainstorm), then deep dive (implementation).
