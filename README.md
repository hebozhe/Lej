# Lej
## A Semantically Intuitionistic, Syntactically Intuitive Language

**Disclaimer:** This is a work in progress, not a usable release. What follows are implementation plans and syntactic coverage. Examples and parallel programs in Go and Python will be added to the [Examples](https://github.com/hebozhe/Lej/tree/main/Examples) folder, and the language will be updated accordingly.


## Synopsis
Lej (pronounced as "ledge") is a statically typed programming language being developed under these maxims, in loose order of priority:
- **Access both classical and intuitionistic worlds.** `brou` (Brouwerian) types work totally normally if you have only `T` (true) and `F` (false) values. `U` (unsure) values behave reliably intuitionistically for `and`, `or`, and `not` operations.
- **The syntax of the green layman, not the seasoned coder, prevails.**  There is no wonky operator `>=` or `!=`, nor is there a `*` that does five different things. A single symbol does a single thing, for a single type. A sixth-grader should be able to follow the arithmetic.
- **Key-value pairs constitute the entire container ontology.**  Immutable or not, a `key` unlocks a `value`, regardless of the container type.
- **If something can't be constructed, it shan't be named.**  No `None`, `nil`, `null`, `nix`, `nada`. `undefined` is an error, not a type.
- **Guarantee precision.** A `rat` is a `map` with "num" (numerator) and "den" (denominator) keys and `int` values. No `float` type.
- **Get it done with two fingers or fewer.** The language is meant to read much like natural language to keep it intuitive and to enable speech-to-text software to encode natural verbal instructions into Lej.


## Lej Semantics and Type Declaration
Lej is meant to read very closely to natural language, but not so much that it's inaccessible to coders. I have so far reached this balancing act:


### The Type System and Type Declaration
As can be inferred from the maxims above, every type that's not primitive is a key-value container.

These are the only semantic primitives of Lej:
- `int` (***integers***: optionally, `int8`, `int16`, `int32`, `int64`; `int` assumes `int64`),
- `chr` (UTF-8 ***characters***), and
- `T`, `U`, and `F`  (Brouwerian ***truth-values***: the `int8` values 2, 1, and 0)
- `fun` (***functions***)
- `gen` (***generators***)

`int`, `fun`, and `gen` can be declared. Brouwerian truth-values and `chr` cannot.

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


### Comments
Comments are enclosed in backticks `` ` ``. They have no effect on the program, itself, and they can be placed anywhere, so long as their deletion at runtime preserves the syntactic legality of the Lej program.


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
- Less-Than: `<INT|RAT-SUBEXPR> > <INT|RAT-SUBEXPR>`.


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
| `block`        | No       | `str`          | All*           | Yes           | No                     | Yes, Each Declared     |
| `class`        | Yes      | `str`          | All*           | Yes           | No                     | Yes, Each Declared     |
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
