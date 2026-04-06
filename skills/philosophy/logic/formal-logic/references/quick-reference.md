# Formal Logic — Quick Reference


## Syntax

| Symbol | Name | Meaning | Truth Condition |
|--------|------|---------|----------------|
| ¬ | Negation | "not" | True when operand is false |
| ∧ | Conjunction | "and" | True when both operands are true |
| ∨ | Disjunction | "or" (inclusive) | True when at least one operand is true |
| → | Conditional | "if...then" | False only when antecedent is true and consequent is false |
| ↔ | Biconditional | "if and only if" | True when both operands have the same truth value |

## Key Valid Forms

| Form | Name | Pattern |
|------|------|---------|
| Modus ponens | Affirming the antecedent | P → Q, P ⊢ Q |
| Modus tollens | Denying the consequent | P → Q, ¬Q ⊢ ¬P |
| Hypothetical syllogism | Chain rule | P → Q, Q → R ⊢ P → R |
| Disjunctive syllogism | Elimination | P ∨ Q, ¬P ⊢ Q |
| Constructive dilemma | | (P → Q) ∧ (R → S), P ∨ R ⊢ Q ∨ S |
| Reductio ad absurdum | Proof by contradiction | Assume ¬P, derive contradiction ⊢ P |

## Key Invalid Forms (Common Fallacies)

| Form | Name | Pattern | Why Invalid |
|------|------|---------|-------------|
| Affirming the consequent | | P → Q, Q ⊢ P | Q could be true for other reasons |
| Denying the antecedent | | P → Q, ¬P ⊢ ¬Q | Q could be true independently of P |

## Syntax

| Symbol | Name | Meaning | Example |
|--------|------|---------|---------|
| ∀x | Universal quantifier | "for all x" | ∀x(Human(x) → Mortal(x)) |
| ∃x | Existential quantifier | "there exists an x" | ∃x(Planet(x) ∧ Habitable(x)) |
| Predicate | Property or relation | F(x), R(x,y) | Tall(socrates), Loves(romeo, juliet) |

## Common Formalization Errors

| Natural Language | Wrong Formalization | Right Formalization | Why |
|-----------------|--------------------|--------------------|-----|
| "All humans are mortal" | ∀x(Human(x) ∧ Mortal(x)) | ∀x(Human(x) → Mortal(x)) | Universal uses →, not ∧ |
| "Some students passed" | ∀x(Student(x) → Passed(x)) | ∃x(Student(x) ∧ Passed(x)) | Existential uses ∧, not → |
| "Only cats purr" | Cat(x) → Purrs(x) | Purrs(x) → Cat(x) | "Only A are B" = B → A |

## Operators

| Symbol | Name | Meaning |
|--------|------|---------|
| □ | Necessity | "necessarily" / "it must be the case that" |
| ◇ | Possibility | "possibly" / "it could be the case that" |

## Applications

| Domain | □ means | ◇ means |
|--------|---------|---------|
| **Metaphysics** | True in all possible worlds | True in some possible world |
| **Epistemics** | Known to be true | Consistent with what's known |
| **Deontic** | Obligatory | Permissible |
| **Temporal** | Always true (in all future times) | Sometimes true (at some future time) |
