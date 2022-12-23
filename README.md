# Lej
## A Semantically Intuitionistic, Syntactically Intuitive Language
**Disclaimer:** This is a work in progress, not a usable release. What follows are implementation plans and syntactic coverage. Examples and parallel programs in Go and Python will be added to the [Examples](https://github.com/hebozhe/Lej/tree/main/Examples) folder, and the language will be updated accordingly.

## Synopsis

Lej (pronounced as "ledge") is a statically typed programming language being developed under these maxims, in loose order of priority:
- **A programmer gets the best of both classical and intuitionistic worlds.** `val` types work totally normally if you have only `T` and `F` values. `U` (unsure) values behave reliably intuitionistically for `and`, `or`, and `not` operations. 
- **A sixth-grader should be able to understand the notation.**  That means no more wonky operator combinations like `>=` or `!=`, nor a `*` that does five different things. A single symbol does a single thing; or, at worst case, for a single type. Assignments and reassignments read more like natural-language sentences. Dealing with integer arithmetic? `=` means "equals", `^` means "to the power of".
- **The map is the King of the Containers.** Anything that's not a primitive is a map of something. A `dict` is a mutable `map`. A `list` is a `dict` with integer keys and renumbering in the background.
    - **Caveat: No floats.** A `rat` is a `map` with "n" (numerator) and "d" (denominator) keys and `int` values. Precision is guaranteed under division. No `float` type.
    - **Caveat: No `None`, `nil`, `null`, `nix`, `nada`.**
- **The type scheme is absolute.** Every type is constructed from base types.
- **A person with two fingers should be able to code in it.** Decent text-to-speech software should output a sentence that a decent encoder can render into Lej syntax.

## Lej Syntax
Lej is meant to read very closely to natural language, but not so much that it's inaccessible to coders. I have so far reached this balancing act.
### Comments
Comments are enclosed in backticks `` ` ``. They can go anywhere. Backticks are meaningless elsewhere in the language.
### Type Declaration
These types are declared by their names, alone: `val` (value, as in "truth-value") and `int` (integer), `rat` (rational number), `str` (string) and `text` (text).

Composite types are declared by their names, and space-separated types indicating the pairs (or singles, if only one key type is permitted). This is much how type hinting works in Python.
They are all as follows:
- Keys not inferred:
    - `map[<KEY-TYPE> <VALUE-TYPE>]`
    - `dict[<KEY-TYPE> <VALUE-TYPE>]`
- Keys inferred:
    - `tup[<VALUE-TYPE>]`
    - `list[<VALUE-TYPE>]`

### Variable Assignment
All variable assignments follow the following format:
`def <TYPE> <ID> as <TYPE-EXPR>;`
Once assigned, it cannot be reassigned via this syntax.
`_` is being reserved for operator consideration. For the time being, onlyStrictCamelCasingWithNumbers is a legal for `<ID>` strings.
### Variable Reassignment
`change <TYPE-ID> to <TYPE-EXPR>;`
Type information is bound to `<ID>` and `<TYPE-EXPR>` nodes at parse time, rather than verified at runtime. Any other behavior is to be considered a bug and should be listed as an Issue.
### Order-of-Operation-Scoped Expressions
Parentheses `(` and `)` denote the order of operations and ***must be present*** for all binary sub-expressions. Unary operators (e.g., `not`, `-`) assume the subexpression immediately after it. The outermost parentheses of an expression may be omitted.
#### Value Expressions
- Primitive values `T` for true, `F` for false, and `U` for unsure. For more on how intuitionistic validity is captured via a mere ternary Kleene logic for the operators available to this language, feel free to read [my article](https://medium.com/@hebozhe/hacking-truth-tables-for-an-intuitionistic-semantics-on-programming-languages-logical-operators-dbbc46e313b4) outlining it.
- Logical negation via `not <VAL-SUBEXPR>`,
- Logical disjunction via `<VAL-SUBEXPR> or <VAL-SUBEXPR>`,
- Logical conjunction via `<VAL-SUBEXPR> and <VAL-SUBEXPR>`.

#### Arithmetic Expressions (WIP)
- Decimal notation via `<INT-SUBEXPR>.<INT-SUBEXPR>`,
    - These always create a `rat` type. There are no floats in Lej.
- Addition via `<(INT|RAT)-SUBEXPR> + <(INT|RAT)-SUBEXPR>`,
- Subtraction via `<(INT|RAT)-SUBEXPR> - <(INT|RAT)-SUBEXPR>`,
- Multiplication via `<(INT|RAT)-SUBEXPR> * <(INT|RAT)-SUBEXPR>`,
- Division via `<(INT|RAT)-SUBEXPR> / <(INT|RAT)-SUBEXPR>`,
    - If the type declaration is `int`, it will evaluate to an `int` (strict division).
    - If the type declaration is `rat`, it will evaluate to a `rat`, even if the denominator is 1.
- Exponentiation `<(INT|RAT)-SUBEXPR> ^ <(INT|RAT)-SUBEXPR>`,

Note: If these arithmetic symbols are ever used for other types, their behavior will be unambiguous.

#### Relational-Logical Expressions (WIP)
Where `X` and `Y` refer to the type of the expressions...
- Identity via `<X-SUBEXPR> = <X-SUBEXPR>`,
- Comparatives via `<X-SUBEXPR> > <X-SUBEXPR>` and `<X-SUBEXPR> < <X-SUBEXPR>`,
    - Negated comparisons normally done via `<X-SUBEXPR> != <X-SUBEXPR>` in other languages are instead accomplished with `not <VAL-SUPEXPR>`, since all comparisons in this categeory output value subexpressions.
    - The same applies to `<=`, `>=`, `!=`, etc. For example, `<X-SUBEXPR> <= <X-SUBEXPR>` in other languages can instead be rendered `not (<X-SUBEXPR> > <X-SUBEXPR>)` or `(<X-SUBEXPR> < <X-SUBEXPR>) or (<Y-SUBEXPR> = <Y-SUBEXPR>)`.

Note: If these relational symbols are ever used for other types, their behavior will be unambiguous.

### Containers
#### Explicit Key-Value Containers
Containers where keys must be explicit include `map`, and `dict`. Square brackets `[` and `]` denote their scopes. The comma `,` separates items in a given container. If the items of a container are a key-value pair, they are space-separated. The keys of these containers must be immutable

Here are some example map assignments:
`def map[str int] alphaOrder as ['A' 1, 'B' 2, 'C' 3];`
`def map[str dict[int str]] alphaOrderLower as ['A' [1 'a'], 'B' [2 'b'], 'C' [3 'c']];`

#### Implicit Key-Value Containers
Containers where keys should not be declared include `tup` and `list`. Following the examples above should clarify the differences in the rules:
`def tup[str] alphaTuple as ['A', 'B', 'C'];`
`def list[int] orderList as [1, 2, 3];`

#### Strings and Text
Strings and text, according to Lej semantics, are tuples and lists of character primitives, respectively.
Only single quotes denote them. The single-quote character "'" is offset with a backslash `\`.

So, these examples follow from the above ones:
`def str alphaString as 'ABC';`
`def text alphaText as 'ABC';`

### Functions (WIP)
#### Creating Functions
The syntactic shell of every new function is:
```
def <ID> as follows:
  take <TYPE> <ID>, <TYPE> <ID>;
  expect <X>;
  ...
  give <X-(EXPR|ID)>;
```
The indentation is optional. Only a single space is required to separate blocks and "lines" of code. Lej can be minified.
- A `take` statement is optional. You place your parameters here.
- An `expect` statement is required. It declares the expected return type of the function.
- A `give` statement is required.
- The `expect` and `give` types (marked `X` above) must match.

#### Calling Functions
Function calls work by replacing the expression to be resolved in an assignment or reassignment statement as follows:
`def <TYPE> <ID> as what <FUNC-ID> with <TYPE-(EXPR|ID)>, <TYPE-(EXPR|ID)>, ... gives;`
- A `with <TYPE-(EXPR|ID)>, ...` corresponds to what the function `take` wants as parameters. It can be omitted if there is no `take` statement in the called function.

### Control Flow (WIP)
#### Conditionals
Because the semantics of Lej are intuitionistic instead of classical/Boolean, a simple `if-else` dynamic will be inadequate for it. Instead, Lej follows a pattern of `if-else-otherwise` model. This is its syntactic shell:

```
if <VAL-EXPR>:
  ...
else:
  ...
otherwise:
  ...
```
The `if` is entered when the `<VAL-EXPR>` evaluates to `T`; the `else` block is entered when it evaluates to `F`; and finally the `otherwise` block is entered when it evaluates to `U`. `else` and `otherwise` blocks are optional. However, if the `else` portion is omitted, then `otherwise` is entered upong either `F` or `U` evaluations of the `<VAL-EXPR>`.

#### Loops
For-loops and while-loops can be merged, so all three schemes are valid:
```
do what follows <INT-(ID|EXPR)> times:
  ...
  again!
```
```
do what follows until <VAL-(EXPR|ID)>:
  ...
  again!
```
```
do what follows <INT-(ID|EXPR)> times or until <VAL-(EXPR|ID)>:
  ...
  again!
```
`again!` commands are required enclose loops. Additionally, the `back!` command corresponds to the `continue` keyword in most programming languages, and the `out!` command corresponds to the `break` statement in most programming languages.

## Lej Semantics
### Primitives
- The truth-value primitives `T`, `U`, and `F` in the Go interpreter are signed 8-bit integers from 0 to 2.
- All integer (`int`-type) literals in the Go interpreter are signed 64-bit integers.
- There are character primitives for `str` and `text`.

### Composites
Here, I'm using "mutable" to mean "not frozen". "Immutable" types are frozen. They can only be reassigned with entire expressions, but their internal values cannot be.
The following composite type hierarchy holds:
- (1) A `map` is an immutable base container type with key-value pairs.
    - (1.1) A `tup` (tuple) is a `map` with ordered `int` keys.
        - (1.1.1) A `str` (string) is a `tup` with character values.
    - (1.2) A `rat` (rational number) is a `map` with two character keys -- "n" and "d" -- and `int` values for both. "n" represents the numerator, and "d" represents the denominator.
    - (1.3). A `dict` (dictionary) is a mutable `map`.
        - (1.3.1) A `list` is a `dict` with ordered `int` keys.
            - (1.3.1.1) A `text` (text) is a `list` with character values.

## Production Schedule
My current production schedule involves integrating all of the core syntax and semantics.

If you'd like to see what's in the pipeline for implementation, feel free to visit the Examples folder and see analogous Python and Go programs to the Lej ones. They're currently being used so that my coding assistant (ChatGPT) will have specific examples to guide its recommendations and code generation.
