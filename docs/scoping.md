# Scoping

Lej restricts most, and ideally all, syntactic ambiguity. The tradeoff for this clarity is that parentheses are more common in Lej than in other languages.

No operator precedence exists in Lej, either. This means that all complex expressions must be explicitly scoped with parentheses for the parser to permit them.

## Parenthetical Scope

Parentheses `(...)` are used to group expressions in Lej. This is the only way to group expressions, and it is required for all complex expressions.

```
fun foo is this:
    know nat64 n;

    n is (1 + 2) * 3; ~n is 9.~
    n is 1 + (2 * 3); ~n is 7.~
    n is 1 + 2 * 3; ~This throws an error.~

    give n;
\
```