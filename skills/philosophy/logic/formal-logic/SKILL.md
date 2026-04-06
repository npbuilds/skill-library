---
name: formal-logic
description: >
  Propositional, predicate, and modal logic essentials for formalizing natural-language
  arguments. Reference when translating arguments into logical notation, checking validity
  via truth tables or derivation, understanding quantifiers and scope, or exploring
  possibility and necessity via modal operators.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Formal Logic — The Language of Reasoning

The symbolic machinery for making argument structure visible and validity mechanically checkable. Formal logic strips away content and reveals pure form — if the form is valid, any argument with that form is valid regardless of subject matter.

## Propositional Logic

The logic of sentences connected by truth-functional operators.

### Syntax

| Symbol | Name | Meaning | Truth Condition |
|--------|------|---------|----------------|
| ¬ | Negation | "not" | True when operand is false |
| ∧ | Conjunction | "and" | True when both operands are true |
| ∨ | Disjunction | "or" (inclusive) | True when at least one operand is true |
| → | Conditional | "if...then" | False only when antecedent is true and consequent is false |
| ↔ | Biconditional | "if and only if" | True when both operands have the same truth value |

### Key Valid Forms

| Form | Name | Pattern |
|------|------|---------|
| Modus ponens | Affirming the antecedent | P → Q, P ⊢ Q |
| Modus tollens | Denying the consequent | P → Q, ¬Q ⊢ ¬P |
| Hypothetical syllogism | Chain rule | P → Q, Q → R ⊢ P → R |
| Disjunctive syllogism | Elimination | P ∨ Q, ¬P ⊢ Q |
| Constructive dilemma | | (P → Q) ∧ (R → S), P ∨ R ⊢ Q ∨ S |
| Reductio ad absurdum | Proof by contradiction | Assume ¬P, derive contradiction ⊢ P |

### Key Invalid Forms (Common Fallacies)

| Form | Name | Pattern | Why Invalid |
|------|------|---------|-------------|
| Affirming the consequent | | P → Q, Q ⊢ P | Q could be true for other reasons |
| Denying the antecedent | | P → Q, ¬P ⊢ ¬Q | Q could be true independently of P |

### Validity Testing

**Truth table method**: Enumerate all possible truth values for atomic propositions. An argument is valid if there's no row where all premises are true and the conclusion is false.

**Short truth table method**: Try to construct a counterexample (premises true, conclusion false). If you can't, the argument is valid.

## Predicate Logic (First-Order)

Extends propositional logic with quantifiers, variables, and predicates — captures internal structure of propositions.

### Syntax

| Symbol | Name | Meaning | Example |
|--------|------|---------|---------|
| ∀x | Universal quantifier | "for all x" | ∀x(Human(x) → Mortal(x)) |
| ∃x | Existential quantifier | "there exists an x" | ∃x(Planet(x) ∧ Habitable(x)) |
| Predicate | Property or relation | F(x), R(x,y) | Tall(socrates), Loves(romeo, juliet) |

### Key Equivalences

- ¬∀xF(x) ≡ ∃x¬F(x) — "not all are F" = "some are not F"
- ¬∃xF(x) ≡ ∀x¬F(x) — "none are F" = "all are not F"
- ∀x(F(x) → G(x)) ≠ ∀x(F(x) ∧ G(x)) — "all F are G" ≠ "everything is both F and G"

### Common Formalization Errors

| Natural Language | Wrong Formalization | Right Formalization | Why |
|-----------------|--------------------|--------------------|-----|
| "All humans are mortal" | ∀x(Human(x) ∧ Mortal(x)) | ∀x(Human(x) → Mortal(x)) | Universal uses →, not ∧ |
| "Some students passed" | ∀x(Student(x) → Passed(x)) | ∃x(Student(x) ∧ Passed(x)) | Existential uses ∧, not → |
| "Only cats purr" | Cat(x) → Purrs(x) | Purrs(x) → Cat(x) | "Only A are B" = B → A |

## Modal Logic

Extends classical logic with operators for possibility and necessity.

### Operators

| Symbol | Name | Meaning |
|--------|------|---------|
| □ | Necessity | "necessarily" / "it must be the case that" |
| ◇ | Possibility | "possibly" / "it could be the case that" |

### Key Relations

- □P ≡ ¬◇¬P — "necessarily P" = "not possibly not-P"
- ◇P ≡ ¬□¬P — "possibly P" = "not necessarily not-P"
- □P → P — what's necessary is actual (in most systems)
- P → ◇P — what's actual is possible

### Applications

| Domain | □ means | ◇ means |
|--------|---------|---------|
| **Metaphysics** | True in all possible worlds | True in some possible world |
| **Epistemics** | Known to be true | Consistent with what's known |
| **Deontic** | Obligatory | Permissible |
| **Temporal** | Always true (in all future times) | Sometimes true (at some future time) |

Modal logic is particularly useful for counterfactual reasoning (connects to counterfactual-reasoner), thought experiments (connects to thought-experiment-lab), and analyzing necessity vs. contingency claims.

## Diagnostic Cues

**When to formalize**: Formalize when an argument's validity is in question and the natural-language structure is ambiguous. Formalization strips away rhetorical fog and reveals pure structure.

**When NOT to formalize**: Don't formalize when the argument's weakness is in its premises (bad evidence, false claims), not its structure. Formal logic checks validity, not soundness — a valid argument with false premises is formally fine but practically useless.

**Translation heuristic**: Map natural language to logical form by identifying:
1. The atomic propositions (what's being asserted)
2. The logical connectives (how assertions relate)
3. The quantifier scope (what "all" and "some" range over)

Apply these translation steps to convert natural-language arguments into symbolic form before evaluating validity.

## Common Mistakes

- Confusing validity (structure) with truth (content)
- Treating "if" in natural language as always mapping to material conditional (→)
- Quantifier scope errors ("Every student has a teacher" — one teacher for all, or each student has their own?)
- Treating "or" as always exclusive (logic's ∨ is inclusive by default)
- Assuming formal validity makes an argument good (a valid argument with false premises proves nothing)
