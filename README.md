# Lej
## A Semantically Intuitionistic, Syntactically Intuitive Language
**Disclaimer:** This is a work in progress, not a usable release. What follows are implementation plans and syntactic coverage. Examples and parallel programs in Go and Python will be added to the [Examples](https://github.com/hebozhe/Lej/tree/main/Examples) folder, and the language will be updated accordingly.

## Synopsis

Lej (pronounced as "ledge") is a statically typed programming language being developed under these maxims, in loose order of priority:
- **A programmer gets the best of both classical and intuitionistic worlds.** `val` types work totally normally if you have only `T` and `F` values. `U` (unsure) values behave reliably intuitionistically for `and`, `or`, and `not` operations. 
- **A sixth-grader should be able to understand the notation.**  That means no more wonky operator combinations like `>=` or `!=`, nor a `*` that does five different things. A single symbol does a single thing; or, at worst case, for a single type. Assignments and reassignments read more like natural-language sentences. Dealing with integer arithmetic? `=` means "equals", `^` means "to the power of".
- **The map is the King of the Containers.** Anything that's not a primitive is a map of something. A `dict` is a mutable `map`. A `list` is a `dict` with integer keys and renumbering in the background.
    - **Caveat: No floats.** A `frac` is a `dict` with `numer` (numerator) and `denom` (denominator) keys and `int` values. Precision is guaranteed under division. No `float` type.
    - **Caveat: No `None`, `nil`, `null`, `nix`, `nada`.**
- **The type scheme is absolute.** Every type is constructed from base types.
- **A person with two fingers should be able to code in it.** Decent text-to-speech software should output a sentence that a decent encoder can render into Lej syntax.

## Lej Syntax
### Variable Assignment
All variable assignments follow the following format:
`def <TYPE> <ID> as <TYPE-EXPR>;`
Once assigned, it cannot be reassigned via this syntax.
`_` is being reserved for operator consideration. For the time being, onlyStrictCamelCasingWithNumbers is a legal for `<ID>` strings.
### Variable Reassignment
`change <TYPE-ID> to <TYPE-EXPR>;`
Type information is bound to `<ID>` and `<EXPR>` nodes at parse time, rather than verified at compile time. Any other behavior is to be considered a bug and should be listed as an Issue.
### Order-of-Operation Scoped Expressions
Parentheses `(` and `)` denote the order of operations and ***must be present*** for all binary sub-expressions. Unary operators (e.g., `not`, `-`) assume the subexpression immediately after it. The outermost parentheses of an expression may be omitted.
#### Value Expressions
- Primitive values `T` for true, `F` for false, and `U` for unsure. For more on how intuitionistic validity is captured via a mere ternary Kleene logic for the operators available to this language, feel free to read [my article](https://medium.com/@hebozhe/hacking-truth-tables-for-an-intuitionistic-semantics-on-programming-languages-logical-operators-dbbc46e313b4) outlining it.
- Logical negation via `not <VAL-SUBEXPR>`,
- Logical disjunction via `<VAL-SUBEXPR> or <VAL-SUBEXPR>`,
- Logical conjunction via `<VAL-SUBEXPR> and <VAL-SUBEXPR>`.

#### Arithmetic Expressions (WIP)
- Addition via `<(INT|FRAC)-SUBEXPR> + <(INT|FRAC)-SUBEXPR>`,
- Subtraction via `<(INT|FRAC)-SUBEXPR> - <(INT|FRAC)-SUBEXPR>`,
- Multiplication via `<(INT|FRAC)-SUBEXPR> * <(INT|FRAC)-SUBEXPR>`,
- Division via `<(INT|FRAC)-SUBEXPR> / <(INT|FRAC)-SUBEXPR>`,
- Exponentiation `<(INT|FRAC)-SUBEXPR> ^ <(INT|FRAC)-SUBEXPR>`,

#### Relational-Logical Expressions (WIP)
Where `X` and `Y` refer to the types of the expressions...
- Identity via `<X-SUBEXPR> = <X-SUBEXPR>`,
- Comparatives via `<X-SUBEXPR> > <X-SUBEXPR>` and `<X-SUBEXPR> < <X-SUBEXPR>`,
    - Negated comparisons normally done via `<X-SUBEXPR> != <X-SUBEXPR>` in other languages are instead accomplished with `not <VAL-SUPEXPR>`, since all comparisons in this categeory output value subexpressions.
    - The same applies to `<=`, `>=`, `!=`, etc. For example, `<X-SUBEXPR> <= <X-SUBEXPR>` in other languages can instead be rendered `not (<X-SUBEXPR> > <X-SUBEXPR>)` or `(<X-SUBEXPR> < <X-SUBEXPR>) or (<Y-SUBEXPR> = <Y-SUBEXPR>)`.

### Functions (WIP)
The syntactic shell of every function is:
```
def <ID> as follows:
  take <TYPE> <ID>, <TYPE> <ID>;
  ...
  give <TYPE-EXPR>|<TYPE-ID>;
```
The indentation is optional. Only a single space is required to set off individual segments of code.
A `give` statement is required, even if one would normally not return anything. When in doubt, give `T` to indicate successful completion of the function. A `take` statement is optional.
