---
id: 001
title: Initial Constitution Ratification
stage: constitution
date: 2025-12-24
surface: agent
model: claude-sonnet-4-5
feature: none
branch: master
user: Mohsin Raza
command: /sp.constitution
labels: ["constitution", "governance", "phase-1", "hackathon"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (governance document)
---

## Prompt

# 📜 Project Constitution
## Todo App — Phase 1 (Hackathon II)

This Constitution defines the **non-negotiable laws**, **constraints**, and **quality standards** governing the development of the Todo App (Phase 1).
All agents, sub-agents, skills, specifications, and implementations **MUST comply** with this Constitution.

---

## 1. 🎯 Project Purpose

The goal of Phase 1 is to build a **robust, production-grade CLI Todo Application** using **AI-Driven Development** principles, demonstrating:

- Agent orchestration
- Reusable intelligence (skills)
- Spec-driven development
- Automated QA enforcement
- Clear separation of concerns

This phase is intentionally minimal in scope but **maximal in quality**.

---

## 2. 🧠 Development Philosophy (Foundational Laws)

1. **Specification is the Source of Truth**
   - No code may exist without an approved specification.
   - Specs override assumptions, preferences, and shortcuts.

2. **Agents, Not Prompts**
   - All meaningful work must be executed by agents or sub-agents.
   - Skills are reusable intelligence units, not one-off instructions.

3. **Quality Gates Over Speed**
   - Failing QA is a hard stop.
   - Partial correctness is considered failure.

4. **Deterministic Behavior**
   - Same input → same output.
   - No randomness, no hidden state.

---

## 3. 🧩 Phase 1 Scope (Hard Boundaries)

### ✅ Allowed
- CLI-based interaction only
- In-memory data storage
- Python standard library
- CRUD operations for todos
- Clear error handling
- Structured command syntax
- Automated tests

### ❌ Prohibited
- ❌ Databases (SQL / NoSQL)
- ❌ File persistence (JSON, CSV, TXT, etc.)
- ❌ Web frameworks (FastAPI, Flask, Django)
- ❌ UI / Frontend
- ❌ External APIs
- ❌ Background services
- ❌ Network calls
- ❌ Global mutable state without control

Violation of any ❌ rule = **automatic failure**.

---

## 4. 🤖 Agent Architecture Rules

### 4.1 Main Agent
- Orchestrates workflow
- Delegates work to sub-agents
- Never implements logic directly

### 4.2 Sub-Agents
Each sub-agent must have:
- A **single clear responsibility**
- One or more **reusable skills**
- Explicit ownership of outcomes

### 4.3 Skills (Reusable Intelligence)
- Stored in `.claude/skills/`
- Markdown format
- Must be:
  - Deterministic
  - Reusable
  - Agent-owned
- Skills must never contain project-specific hardcoding unless explicitly scoped to Phase 1.

---

## 5. 🧪 Quality Assurance (Mandatory)

### QA is NOT optional.

The QA Agent must enforce:

- Test execution and coverage validation
- Requirement-to-implementation traceability
- Code quality audits
- Phase-1 constraint compliance

### Quality Gates
- ❌ Any FAIL = stop execution
- ⚠️ CONDITIONAL = must be resolved
- ✅ PASS = proceed

---

## 6. 📐 Specification Rules

- All features must have:
  - Description
  - Acceptance criteria
  - Edge cases
  - Error conditions
- CLI commands must be:
  - Explicit
  - Predictable
  - Documented
- Specs must be human-readable and machine-enforceable

---

## 7. 🔁 Execution Lifecycle (Enforced Order)

1. Constitution
2. Specification
3. Planning
4. Execution
5. QA Validation
6. Checklist Verification

Skipping steps is **strictly forbidden**.

---

## 8. 🧯 Error Handling Principles

- Errors must be:
  - Clear
  - Actionable
  - User-friendly
- Silent failures are forbidden.
- Stack traces must not be exposed to end users.

---

## 9. 📊 Evaluation Criteria (Judge-Aligned)

This project will be evaluated on:

- Agent design clarity
- Skill reusability
- Spec completeness
- QA rigor
- Constraint discipline
- Architectural cleanliness
- Professional documentation

---

## 10. 🏁 Final Law

> **If it is not specified, it does not exist.**
> **If it is not tested, it is broken.**
> **If it violates Phase-1 constraints, it is rejected.**

---

## ✅ Constitution Acceptance

By proceeding with `/sp.specify`, all agents acknowledge and accept this Constitution in full.

## Response snapshot

Constitution successfully created and ratified as **Version 1.0.0**.

**Created File:** `.specify/memory/constitution.md`

**Constitution Structure:**
- **7 Core Principles** defined with rules and rationale
- **Phase 1 Technical Constraints** documented (Python 3.11+, CLI, in-memory)
- **Quality Assurance Rules** established (3 QA skills, quality gates)
- **Development Workflow** enforced (Constitution → Spec → Plan → Tasks → Implement → QA)
- **Governance** rules for amendments and compliance

**Key Principles:**
1. **Specification is the Source of Truth** - No code without approved spec
2. **Agents, Not Prompts** - Skills are reusable intelligence units
3. **Quality Gates Over Speed** - QA failures block progress
4. **Deterministic Behavior** - Same input = same output
5. **Phase 1 Scope Boundaries** - CLI + in-memory only (strict)
6. **Agent Architecture** - Single responsibility, clear delegation
7. **Test-First Development** - TDD mandatory (Red-Green-Refactor)

**Quality Gates Defined:**
- ✅ PASS: 100% tests pass, ≥80% coverage, Phase 1 compliant
- ⚠️ CONDITIONAL: 75-79% coverage with plan
- ❌ FAIL: Test failures, Phase 1 violations, <75% coverage

**Phase 1 Constraints Enforced:**
- ✅ Allowed: CLI, in-memory, Python, CRUD, tests
- ❌ Prohibited: Databases, file I/O, web frameworks, GUI, APIs

**Sync Impact:**
- ✅ plan-template.md - Constitution Check aligns
- ✅ spec-template.md - User scenarios align with determinism
- ✅ tasks-template.md - Test-first approach aligns with TDD

**Next Steps:**
Ready to proceed with `/sp.specify` to create feature specifications.

## Outcome

- ✅ Impact: Constitution ratified, governance framework established for Todo App Phase 1
- 🧪 Tests: N/A (governance document, not implementation)
- 📁 Files: Created .specify/memory/constitution.md (440 lines, Version 1.0.0)
- 🔁 Next prompts: /sp.specify [feature-name] to create first feature specification
- 🧠 Reflection: Constitution successfully establishes non-negotiable laws for Phase 1. All 7 principles are clear, measurable, and enforceable. Phase 1 constraints (CLI + in-memory) are explicit and strict. QA skills (test-execution, requirement-verification, quality-audit) are referenced. Ready for specification-driven development.

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution template successfully filled with user-provided comprehensive governance rules
- Graders run and results (PASS/FAIL): PASS - All placeholders replaced, no TODOs, version 1.0.0 ratified, sync impact documented
- Prompt variant (if applicable): Full constitution provided by user, comprehensive governance model
- Next experiment (smallest change to try): Test constitution enforcement by running /sp.specify and verifying Phase 1 constraints are checked
