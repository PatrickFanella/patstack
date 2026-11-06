---
name: digest-distiller
description: "Summaries: TL;DR, executive summary, abstract or condensed version of a document, thread or transcript, matched to audience and purpose. Not for checking claims; use claim-verifier."
license: MIT
metadata:
  blacktower-pack: creative
  blacktower-kind: workflow
  blacktower-tier: standard
  blacktower-capabilities: writing-craft,summarization
  author: jwynia
  version: "1.0"
  type: utility
  mode: generative
  domain: writing
---

# digest-distiller

## Purpose

Create effective summaries by matching summarization type to purpose, audience, and context. "Summarize" can mean many different things—this skill helps identify and execute the right approach.

## Core Principle

**Summarization is translation, not just reduction.** Different purposes require different summary types. Match the type to the need before condensing.

---

## Defaults

Summarize without asking first. Infer purpose, audience and length from the request and the source. When they are unstated, write a brief summary (a paragraph or a few bullets) that leads with the main point, for a reader who has not seen the source, and say in one line what you assumed.

Ask before summarizing only when the target audience or length is genuinely ambiguous and the choice changes the result, such as an executive summary versus an academic abstract of the same paper. Then use [the question groups](references/clarifying-questions.md) and ask about the dimension that matters.

---

## Summary Type Taxonomy

### Information Reduction Approaches

| Type | What It Is | When to Use |
|------|-----------|-------------|
| **Key Point Extraction** | Isolating the most important claims | Original has discrete important points |
| **Abstraction** | Higher-level statements covering multiple details | Patterns matter more than specifics |
| **Gisting** | Capturing essential meaning, discarding details | Only core message matters |
| **Compression** | Shortening while preserving information | Comprehensive coverage needed in less space |

### Structural Approaches

| Type | What It Is | When to Use |
|------|-----------|-------------|
| **Executive Summary** | Business-focused: decisions, recommendations, outcomes | Documents requiring action |
| **Abstract/Précis** | Academic: methodology and findings | Research papers, technical documents |
| **TLDR** | Ultra-brief main takeaway | Casual communication, extreme brevity |
| **Outline** | Hierarchical structure of main/supporting points | Logical structure matters |

### Purpose-Oriented Approaches

| Type | What It Is | When to Use |
|------|-----------|-------------|
| **Synthesis** | Combining multiple sources coherently | Summarizing across documents |
| **Critical Summary** | Evaluating claims while condensing | Assessment of quality needed |
| **Contextual Summary** | Framing within broader knowledge | Understanding bigger picture matters |
| **Actionable Summary** | Focusing on implications and next steps | Summary will drive action |

---

## Execution by Type

### Key Point Extraction
1. Scan for topic sentences and conclusions
2. Identify explicitly stated main ideas
3. List each distinct point
4. Preserve original phrasing where powerful

**Example:** "The author makes three main arguments: (1)..., (2)..., (3)..."

### Abstraction
1. Group related details
2. Find common themes or patterns
3. Create higher-level statements
4. Reduce specifics to principles

**Example:** "Multiple studies consistently show..." instead of listing 12 studies

### Gisting
1. Ask: "What is the one thing to remember?"
2. Distill to core insight
3. Remove all supporting detail
4. Verify essence is preserved

**Example:** "Remote work increases productivity for most knowledge workers."

### Executive Summary
1. State the problem/opportunity
2. Present the solution/recommendation
3. Highlight key benefits
4. Note costs/risks
5. Specify required actions

### Synthesis
1. Read all sources
2. Identify common themes
3. Note contradictions
4. Find complementary information
5. Create unified narrative

**Example:** "Across the five reports, three key trends emerge..."

### Critical Summary
1. Summarize the claims
2. Evaluate the evidence
3. Assess methodology
4. Note limitations
5. Conclude with assessment

**Example:** "While the author claims X, the evidence is limited by..."

---

## Format Variations

### Quotation-Based
- Use key phrases verbatim
- When precise wording is important
- Select and organize most important quotes

### Bullet Points
- Break continuous text into discrete units
- When quick scanning is valued
- Make each point standalone

### Progressive Summary
- Start ultra-brief
- Add layers of detail
- Let reader choose depth

### Comparative Summary
- Side-by-side analysis
- Highlight similarities and differences
- When contrasting sources

---

## Quality Checklist

- [ ] Purpose is clear
- [ ] Audience is considered
- [ ] Scope is appropriate
- [ ] Emphasis matches needs
- [ ] Format serves purpose
- [ ] Core message is preserved
- [ ] Reduction is proportional
- [ ] No invented information
- [ ] Attribution where needed

---

## Anti-Patterns

### The Information Dump
**Problem:** Reduces length but not complexity
**Fix:** Focus on what matters, not just what's short

### The Distortion
**Problem:** Changes meaning through compression
**Fix:** Verify summary against original claims

### The One-Size-Fits-All
**Problem:** Same approach for all requests
**Fix:** Match type to purpose and audience

### The Over-Abstraction
**Problem:** Loses all useful specifics
**Fix:** Preserve concrete details that support understanding

---

## Integration Points

**Inbound:**
- When asked to summarize any content
- When processing long documents
- When creating documentation

**Outbound:**
- To decision-making processes
- To knowledge management systems
- To communication outputs

**Complementary:**
- `speech-shaper`: For spoken summaries
- `voice-fingerprint`: For maintaining voice in summaries
