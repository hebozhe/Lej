# **Lej**: A Semantically Intuitionistic, Syntactically Intuitive Language

**Disclaimer:** This is a work in progress, not a usable release. What follows are implementation plans and syntactic coverage. Examples and parallel programs in Go will be added to the [Examples](https://github.com/hebozhe/Lej/tree/main/Examples) folder, and the language will be updated accordingly. The older Python interpreter for Lej has been scrapped, but will recommence once Codon or mypy are sufficiently rich to cover the needed types.

## **Overview**
---
Lej (pronounced as "ledge") is a statically typed programming language that aims to provide a simple and intuitive syntax while allowing access to both classical and intuitionistic worlds. It is being developed under these maxims, in loose order of priority:

- **Access both classical and intuitionistic worlds.** Brouwerian types work normally if you have only `T` (true) and `F` (false) values. `U` (unsure) values behave reliably intuitionistically for `and`, `or`, and `not` operations.
- **Simple and intuitive syntax.** The syntax is designed to be easy to read and write for beginners and seasoned developers alike. A single symbol does a single thing, for a single type. 
- **Key-value pairs for containers.** Key-value pairs constitute the entire container ontology, whether they are immutable or not. A `key` unlocks a `value`, regardless of the container type.
- **Avoid undefined or null types.** Lej does not have a type for `None`, `nil`, `null`, `nix`, `nada`. `undefined` is an error, not a type.
- **Precision guaranteed.** A `rat` is a `map` with "num" (numerator) and "den" (denominator) keys and `int` values. There is no `float` type in Lej.
- **Intuitive and efficient.** The language is meant to be easy to read and write, using a syntax similar to natural language. This enables speech-to-text software to encode natural verbal instructions into Lej with ease.
---

## **Documentation**
### Basic Syntax
[**Comments**](#comments)
1. **Primitive Symbols**
    - [**Whitespaces**](#whitespaces)
    - [**Arithmetic Operators**](#arithmetic-operators)


## **The Complete EBNF Grammar of Lej**
---
```

```
---


## **Comments**
---
There are only multiline comments in Lej. They are initialized and terminated with unescaped "`" characters. They can go anywhere, as they are skipped at lexing and parsing.

Example:
```
def nat zero as 0; `Assigns the natural number 0 to the name "zero".`
change zero `which was defined above
             and continues onto this line` to -1 + 1;
```
---

## **Whitespaces**
---
Spaces, tabs, and line breaks are all legitimate spacing options.
Spacing is only meaningful in the separation of lexemes in the language. They make no difference to the validity of the syntax.

Obviously, you should use your best judgment when it comes to formatting, but Lej does not impose such rules on it. Lej, therefore, can also be minified.

Example:
```
from showing use showing;


def brou               spacedOkay as               T;
if spacedOkay:  
def brou didPrintToTerminal
as what showing with "Conditional caught!" gives;
else:  def brou didPrintToTerminal as F; otherwise: def brou didPrintToTerminal as U;
```
---

## **Arithmetic Operators**
---
Arithmetic operators connnect numeric types to produce other numeric types:
- `+` for addition,
- `-` for subtraction,
- `*` for multiplication,
- `/` for division,
- `%` for modulo,
- `.` for decimalization.


Example:
```
def nat sumOfFirstTwoPrimes as 2 + 3;
```
---



---
These are the only semantic primitives of Lej:
- `nat` (***naturals***: optionally, `nat8`, `nat16`, `nat32`, `nat64`; `nat` assumes `nat64 `)
- `int` (***integers***: optionally, `int8`, `int16`, `int32`, `int64`; `int` assumes `int64`),
  - The key difference between `nat` and `int` types is the same as the difference between unsigned and signed integers in other languages.
- `chr` (UTF-8 ***characters***, which also work like Go's `rune` types), and
- `T`, `U`, and `F`  (Brouwerian ***truth-values***: the `int8` values 2, 1, and 0)
- `fun` (***functions***)
- `gen` (***generators***)

Every other type is a key-value pairing.

These key-value types are declared by their names, alone, because both the keys and values are predetermined:
- `brou` (***Brouwerians***: `int` keys and `T`, `U`, or `F` values),
- `rat` (***rationals***: `str` keys `'num'` and `'den'`, the numerators and denominators, respectively, and `int` values),
denominators of their respective exponents, and `int` values.
- `str` (***strings***: `int` keys and `chr` values),
- `text` (***texts***: `int` keys and `chr` values)

The remaining key-value pairings are underdetermined, and so space-separated types in adjoining brackets `[...]` are needed to specify the types of their values, or of their keys and values.

Some keys are *inferred*, meaning they are restricted to just one type. Thus, only the type(s) of their values need to be specified. For the rest, both must be.

Keys inferred:
  - `tup[<VAL-TYPE>]`  (`int` keys and values of any type)
  - `list[<VAL-TYPE>]`  (`int` keys and values of any type)
  - `block[<VAL-TYPE>, ...]`  (`str` keys and a comma-separated, ordered listing of the types for every block attribute)
  - `class[<VAL-TYPE>, ...]`  (`str` keys and a comma-separated, ordered listing of the types for every block attribute)

Keys not inferred:
  - `map[<KEY-TYPE> <VAL-TYPE>]`  (`int`, `chr`, `str`, `tup`, `block`, and ` keys, and keys can be of any legally defined type.)
  - `dict[<KEY-TYPE> <VAL-TYPE>]` (Keys can be of `str`, `int` or `brou` types, and keys can be of any legally defined type.)


All keys must be immutable, and the immutable (`IMM`) types are `int`, `chr`, `T`, `U`, `F`, `str`, `tup[<IMM-VAL-TYPE>]`, and `block[<IMM-VAL-TYPE>, ...]`.


## Lej Syntax




### Identifiers
All `<ID>` tokens must be in camelCase, as defined by the regular expression `[a-z][0-9a-zA-Z]*`.

### Variable Assignment and Reassignment
Every type declaration creates a `<TYPE>` node. Along with the `<ID>` node, via the following syntax:

`def <X-TYPE> <ID> as <X-EXPR>;`

Once assigned, variables can be reassigned with the following syntax:

`change <ID> to <X-EXPR>;`

Every variable must be assigned *exactly once* for the lifetime of its existence. Reassignent, however, is unlimited, so long as the type (here, `X`) continues to match.


### Brouwerian Expressions
Brouwerians under the hood are of the type `list[int8]` where the `int8` values 2, 1, and 0 correspond to `T`, `U`, and `F`. `T` and `F` values have only one item, called the head. `U` values consist of a head and a tail corresponding to a unique Boolean truth-table column, which is decided when the program is lexed.

The following expressions work for every `brou` type:
- Negation: `not <BROU-SUBEXPR|ID>`,
- Conjunction: `<BROU-SUBEXPR|ID> and <BROU-SUBEXPR|ID>`, and
- Disjunction: `<BROU-SUBEXPR|ID> or <BROU-SUBEXPR|ID>`.

These expressions can be nested to produce more complex expressions, though they must be enclosed in parentheses when binary operators are used. There is no left- or right-associativity in Lej's parsing procedure.

For instance, the following classical and intuitionistic theorems can be expressed, where `X` and `Y` refer to truth-values or Brouwerian variables, as follows:
- LNC: `not (<BROU-X> and not <BROU-X>)`,
- LEM: `<BROU-X> or not <BROU-X>`
- Double negation introduction: `not not not <BROU-X> or <BROU-X>`,
- Peirce's law: `not (not (not <BROU-X> or <BROU-Y>) or <BROU-X>) or <BROU-X>`.

Of these theorems, if `<BROU-X>` and `<BROU-Y>` both evaluate to `U`, only the LNC evaluates to `T` intuitionistically. The remainder evaluate to `U`, even though all of the tail's truth-values evaluate to `T`. A separate evaluation phase converts `U` Brouwerian heads to `F` and removes their tails.


### Numeracy and Arithmetic Expressions
> God made the integers, all else is the work of man.

While `int` primitives are simply a collection of digits, `rat` types are `map[str int]` types with only the keys `'num'` for their numerators and `'den'` for their denominators.

The following expressions work for both `int` and `rat` types and evaluate to `int` or `rat` types:
- Addition: `<INT|RAT-SUBEXPR> + <INT|RAT-SUBEXPR>`,
- Subtraction: `<INT|RAT-SUBEXPR> - <INT|RAT-SUBEXPR>`,
- Negatives: `-<INT|RAT-SUBEXPR>` (equivalent to subtraction from 0),
- Multiplication: `<INT|RAT-SUBEXPR> * <INT|RAT-SUBEXPR>`,
- Division: `<INT|RAT-SUBEXPR> / <INT|RAT-SUBEXPR>`,
- Modulus: `<INT|RAT-SUBEXPR> % <INT|RAT-SUBEXPR>`, and

`rat` types are not stores. Every `rat` value simplifies in its evaluation. For example, `(1 / 2) + (3 / 2)` evaluates to `2/1`, not `4/2`.

The following expressions work for both `int` and `rat` types and evaluate to `brou` types:
- Equality: `<INT|RAT-SUBEXPR> = <INT|RAT-SUBEXPR>`,
- Greater-Than: `<INT|RAT-SUBEXPR> > <INT|RAT-SUBEXPR>`, and
- Less-Than: `<INT|RAT-SUBEXPR> < <INT|RAT-SUBEXPR>`.


Note that the evaluations for `=`, `>`, and `<` only work with `int` and `rat` types. Lej provides other means for comparing other types.

The following expressions only work with `int` types:
- Decimalization: `<INT-SUBEXPR>.<INT-SUBEXPR>`.

For example, the expression `1.2 * 3.4` evaluates as follows:
- `1.2 * 3.4` to `(12/10) * (34/10)`, to `(6/5) * (17/5)`, to `102/25`.

There are no `float` types in Lej. `2/3` is not equal to `0.333333333333333`, and it never will be.

There is no order of operations nor left- or right-associativity in Lej. An expression like `1 + 2 * 3` is ill-formed in Lej. `(1 + 2) * 3` and `1 + (2 * 3)` are well-formed.

Finally, `int` and `rat` types to not implicitly convert, as shown in these examples.
- `def int divInt as 3/2;` throws an error.
- `def rat divRat as 2/2;` assigns `1/1` to `divRat`.
- `def int decInt as 1.2;` throws an error.

### Container Expressions
Key-value pairs explain the entire ontology of Lej containers. A key-value pair is a call to a unique, immutable value, called
the *key*, to fetch a stored *value*. The exact permissions for these key-value types are covered in this table:

| CONTAINER TYPE | MUTABLE? | ALLOWED KEYS   | ALLOWED VALUES | IMPLICIT KEYS | TYPE MIXING IN KEYS?   | TYPE MIXING IN VALUES? |
| -------------- | -------- | -------------- | -------------- | ------------- | ---------------------- | ---------------------- |
| `map`          | No       | All Immutables | All*           | No            | No                     | No                     |
| `dict`         | Yes      | All Immutables | All*           | No            | No                     | No                     |
| `tup`          | No       | `int`          | All*           | Yes           | No                     | No                     |
| `list`         | Yes      | `int`          | All*           | Yes           | No                     | No                     |
| `str`          | No       | `int`          | `chr`          | Yes           | No                     | No                     |
| `text`         | Yes      | `int`          | `chr`          | Yes           | No                     | No                     |
| `rec`        | No       | `str`          | All*           | Yes           | No                     | Yes, Each Declared     |
| `data`        | Yes      | `str`          | All*           | Yes           | No                     | Yes, Each Declared     |
\* Except for `fun` and `gen` types.

All containers' individual values are all fetched the same way:

- `<CONTAINER-ID>[<CONTAINER'S-KEY>]`

`tup`, `list`, `str`, and `text` types, because they are implicitly ordered, allow for slicing:

- `<(TUP|LIST|STR|TEXT)-ID>[int int]`

Mutable containers can:
- Add key-value pairs,
- Remove key-value pairs, and
- Change values from keys.

Immutable containers cannot.  "Immutable" therefore is closer to "frozen" in meaning.

The phrase "All Immutables" above refers to `int`, `str`, `tup`, and `block` types. `map` types, themselves, cannot be keys.

Container key types cannot ever be changed or mixed within a container. It is perfectly static.
