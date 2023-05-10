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
---
### The Syntax and Semantic Features of Each Type
1. [**Comments**](#comments)
2. [**Whitespaces**](#whitespaces)
3. [**Punctuations**](#punctuations)
    - [**Ending Lines**](#ending-lines)
    - [**Setting Scopes**](#setting-scopes)
    - [**Closing Blocks**](#closing-blocks)
    - [**Checking Legality**](#checking-legality)
4. [**Brouwerians**](#brouwerians)
    - [**Brouwerian Primitives**](#brouwerian-primitives) (`T`, `U`, and `F`)
    - [**Brouwerian Operations**](#brouwerian-operations) (`and`, `or`, and `not`)
5. [**Numerics and Arithmetic**](#numerics-and-arithmetic)
    - [**Numeric Types**](#numeric-types) (`nat`, `int`, and `rat`)
    - [**Arithmetic Operations**](#arithmetic-operations) (`+`, `-`, `*`, and `/`)
    - [**Arithmetic Evaluations**](#arithmetic-evaluations) (`=`, `>`, and `<`)
6. [**Characters**](#characters) (`chr`)
7. [**Data Types**](#data-types)
    - [**Tuples and Lists**](#tuples-and-lists) (`tup` and `list`)
    - [**Strings and Text**](#strings-and-text) (`str` and `text`)
    - [**Maps and Dictionaries**](#maps-and-dictionaries) (`map` and `dict`)
    - [**Records and Data**](#records-and-data) (`rec` and `data`)
### Basic Control Flow
8. [**Assignment and Reassignment**](#assignment-and-reassignment) (`def` and `as`)
    - [**Variable Name Rules**](#variable-name-rules)
9. [**Function Assignments**](#function-assignments)
    - [**Defining Functions**](#defining-functions) (`def fun ID as:`)
    - [**Defining Parameters**](#defining-parameters) (`take`)
    - [**Defining Expected Returns**](#defining-expected-returns) (`expect`)
    - [**Returning Values**](#returning-values) (`give`)
    - [**Calling Functions**](#calling-functions)
10. [**Type Casting**](#type-casting) (`as`)
### Choice Control Flow
11. [**Conditional Statements**](#conditional-statements)
    - [**The Conditional Triad**](#the-conditional-triad) (`if`, `else`, and `otherwise`)
    - [**Conditional Scopes**](#conditional-scopes) (`:` and `\`)
12. [**Loops**](#loops)
    - [**Do-This Loops**](#do-this-loops)
    - [**Do-Until Loops**](#do-until-loops)
    - [**Loop Scopes**](#loop-scopes) (`:` and `\`)
    - [**Breaking**](#breaking) (`out!`)
    - [**Continuing**](#continuing) (`back!`)
13. [**Lookup Checking**](#lookup-checking) (`?`)


## **Comments**
---
There are only multiline comments in Lej. They are initialized and terminated with unescaped "`" characters. They can go anywhere, as they are skipped at lexing and parsing.

Example:
```
def nat zero as 0; `Assigns the natural number 0 to the name "zero".`
re zero `which was defined above
             and continues onto this line` as -1 + 1;
```
---
[Back to Table of Contents](#documentation)


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
def brou didShowOnTerminal
as showing["Conditional caught!"]; \
else:  def brou didShowOnTerminal as F; \ otherwise: def brou didShowOnTerminal as U; \
```
---
[Back to Table of Contents](#documentation)


## **Punctuations**
---
Because Lej can be minified, punctuation plays a major role in organizing sections of the language.

---
[Back to Table of Contents](#documentation)


### **Ending Lines**
---
Two punctuations end lines and have different functions:

- `;` ends a declarative statement, usually an assignment or reassignment.
- `:` opens a block for control flow. It's complementary closing operator is `\`.

Example:
```
def fun reverseStr as this:
    take str s;
    expect str;
    def str reversed as "";
    def nat sLen as len[s];
    def chr c as '';
    def nat i as sLen - 1;
    do this sLen times: `← Open a do-times-block.`
        c as s[i];
        reversed = reversed + c;
        i as i - 1;
        \
    give reversed;
    \
```
---
[Back to Table of Contents](#documentation)


### **Setting Scopes**
---

Scopes for operations, data type definitions, and hard-coded data-type expressions, are enclosed in square brackets `[` and `]`.

Scopes are paramount in Lej, particularly with expressions. It is always syntactically illegal in Lej to leave ambiguous subexpressions. For instance, `3 + 2 / 1` throws an error. The programmer must clarify it as `[3 + 2] / 1` or `3 + [2 / 1]`.

Example:
```
def fun fib as this:
    take nat n;
    expect nat;
    if n < 2:
        give n;
        \
    give [what fib with [n - 2] gives] + [what fib with [n - 1] gives]; `← The function calls are evaluated before the addition.`
    \
```
---
[Back to Table of Contents](#documentation)


### **Closing Blocks**
---

Blocks close with the `\` character after being opened with the `:` character.

Example:
```
def fun multiplyTups as this:
    take tup[int] tupA, tup[int] tupB;
    expect tup[int];
    def nat lenA as len[tupA];
    def nat lenB as len[tupB];
    if not [lenA = lenB]:
        give [];
        \ `← Exit the if-block.`
    def tup[int] result as [];
    def nat i as 0;
    def nat j as 0;
    do this lenA times:
        result as result + [tupA[i] * tupB[j]];
        \ `← Exit the do-times-block.`
    give result;
    \ `← Exit the function.`
```
---
[Back to Table of Contents](#documentation)


### **Checking Legality**
---

The `?` character runs a check on a single statement, outputting the Brouwerians `T`, `U`, or `F`.

Example:
```
def fun countCharFreq as this:
    take str s;
    expect dict[chr nat];
    def dict[chr nat] frequencies as [];
    def nat sLen as len[s];
    def nat i as 0;
    def chr c as '';
    def brou alreadyPresent as U;
    do this sLen times:
        c as s[i];
        alreadyPresent as frequencies[c]?; `← Evaluates to T or F for lookups.`
        if alreadyPresent:
            frequencies[c] as frequencies[c] + 1;
            \
        else:
            def nat frequencies[c] as 1;
            \
        i as i + 1;
        \
    give frequencies;
    \
```
---
[Back to Table of Contents](#documentation)


## **Brouwerians**
---
Brouwerians supplant Booleans as the default truth-value representation, by means of a trivalent system. This is accomplished by use of a Kleene logic and an application of a corollary of Gilvenko's theorem under the hood to correctly capture intuitionistic evaluations under the hood.

Example:
```
def brou thisUnsure as U;
def brou lemWithUnsure as thisUnsure or not thisUnsure; `← Evaluates to U.`
def brou lncWithUnsure as not [thisUnsure and not thisUnsure]; `← Evaluates to T.`
```
---
[Back to Table of Contents](#documentation)


### **Brouwerian Primitives**
---
The primitive Brouwerians `T` and `F` work exactly as their Boolean counterparts. They evaluate to all of the classical (Boolean) evaluations when used on their own. However, every literal `U` ("unknown") in a program refers to a unique valuation.

Example:
```
def brou thisUnsure as U;
def brou lncWithOneUnsure as not [thisUnsure and not thisUnsure]; `← Evaluates to T, since thisUnsure refers to a single unsure value.`
def brou lncWithTwoUnsures as not [U and not U]; `← Evaluates to U, since both U variables occupy different possible truth-values.`
```
---
[Back to Table of Contents](#documentation)


### **Brouwerian Operations**
---
There are four operations that work on Brouwerians:
- `and` for conjunction,
- `or` for disjunction, and
- `not` for negation.

The only peculiarity in Lej is that `not` operating on any unsure value `U` likewise evaluates to a `U` value. This is in line with the Kleene-logic evaluation of an "unsure" evaluation.

Example:
```
def brou valA as U;
def brou negValA as not valA; `← Evaluates to U, but inverts the unique tail under the hood.`
def brou contradiction as valA and negValA; `← Evaluates to F, using a lemma for Gilvenko's theorem under the hood.`

`
To illustrate:
valA and not valA
[1, 0, 2] and not [1, 0, 2]
[1, 0, 2] and [1, 2, 0]
[1, 0, 0]
[0] (The prior evaluation's tail was all-false, indicating a classical contradiction. All classical contradictions are intuitionistic contradictions.)
`
```
---
[Back to Table of Contents](#documentation)


## **Numerics and Arithmetic**
---
Lej seeks to preserve exact calculations at every step of a program. Thus, there is no `float` type employed anywhere in Lej, and that, along with the Brouwerians, probably sets Lej most apart from other programming languages.

---
[Back to Table of Contents](#documentation)


### **Numeric Types**
---
There are three numeric types with allowed subtypes for bit sizes.
- `nat` for all natural numbers (along with 0), including `nat8`, `nat16`, `nat32`, and `nat64` (mirroring `nat`);
- `int` for all integers, including `int8`, `int16`, `int32`, and `int64` (mirroring `int`); and
- `rat` for all rational numbers, including `rat8`, `rat16`, `rat32`, and `rat64` (mirroring `rat`).

While `nat` and `int` types correspond to the unsigned and signed integers of other languages more directly, and thus are primitive, the `rat` type is a `map[str int]` with the string `"num"` (representing the numerator) and `"den"` (the denominator).

However, the `rat` type is not merely a storage of divisions that do not resolve to `nat` or `int` types. `rat` types are also automatically simplified during evaluation.

Example:
```
def rat threeFourths as 24 / 32; `← Evaluates to 3 / 4, since 8 is the GCD of 24 and 32.`
def rat eightFifths as 1.6;  `← Evaluates to 8 / 5, since 1.6 = (16 / 10) = (8 / 5).`
```
---
[Back to Table of Contents](#documentation)


### **Arithmetic Operations**
---
Arithmetic operations evaluate pairs ofn umbers to other numeric types.

Only these five arithmetic operations exist:
- `+` for addition,
- `-` for subtraction,
- `*` for multiplication,
- `/` for division, and
- `.` for decimalization.

Here, `/` and `.` are the only risky operation to deal with in working with arithmetic, since divisions that do not simplify to `int` or `nat` types, but are meant to be assigned to `int` or `nat` variables, will throw errors.

Example:
```
def nat threeLongForm as (24 / 32) * (40 / 10); `← Evaluates to 3, since (3 / 4) * (4 / 1) = (12 / 4) = (3 / 1) = 3.`
def int halfOfThree as threeLongForm / -2;  `← ERROR! Since (3 / -2) only simplifies to (-3 / 2), it cannot be an integer.`
```

Further, be wary of decimalization places, since Lej _will_ count every place to the bitter end and find the GCD for that value, all of which take more time than would otherwise be required without it.

Example:
```
def nat threeLongForm as 3.00000; `← Evaluates to 3, since 3.00000 = (300000 / 100000) = (3 / 1) = 3.`
def nat threeShortForm as 3; `← Evaluates to 3, performing no operations.`
```
---
[Back to Table of Contents](#documentation)


### **Arithmetic Evaluations**
---
Arithmetic evaluations evaluate pairs of numbers to Brouwerians (though only `T` or `F`).

Only these three arithmetic evaluations exist:
- `<` for less-than comparison,
- `>` for greater-than comparison, and
- `=` for equality comparison.

Unlike most other programming languages, operator combinations like `<=` and `!=` are not meaningful in Lej. This will extend the size of one's code; but, it reveals how many evaluations are actually occurring in a piece of code.

Example:
```
def int a as -42;
def int b as 99 / 11;
def brou bNotLessThana as not [b < a]; `← Evaluates to T.`
def brou aAndbGreaterThanOrEqualTo0 as [[a > 0] or [a = 0]] and [[b > 0] or [b = 0]]; `← Evaluates to F.`
aAndbGreaterThanOrEqualTo50 as [a > -1] and [b > -1] `← Evaluates to F, also, since it's equivalent to the expression above.`
```
---
[Back to Table of Contents](#documentation)


## **Characters**
---
Characters are individual UTF-8 encodings that are mutually comparable. They're also the basic building blocks of `str` and `text` types.

`chr` values are comparable via the arithmetic evaluation symbols.

Example:
```
def chr enA as 'A';
def chr zhDe as '的';
def brou aLessThanDe as enA < zhDe; `← Evaluates to T.`
def chr lastTwoEnglishLetters as 'YZ'; `← ERROR! Too many characters for a single character type.`
```
---
[Back to Table of Contents](#documentation)


## **Data Types**
---
The data type ontology of Lej neatly divides into two classifications: read-only data types and read-writable data types. Given these constraints, the read-only data types, themselves, only accept other read-only data types or immutable types. Read-writable data types are more open. The main restriction to a read-only data type is that elements cannot be reassigned, added, or deleted once it is defined.

This table adequately breaks down the entire type system of Lej:

|    Name    | Signature |        Composition       | Mutable? |    Key Types   |   Value Types  |
|:----------:|:---------:|:------------------------:|:--------:|:--------------:|:--------------:|
|   Natural  |   `nat`   |         Primitive        |     F    |                |                |
|   Integer  |   `int`   |         Primitive        |     F    |                |                |
|  Character |   `chr`   |         Primitive        |     F    |                |                |
|    Tuple   |   `tup`   |        First-Class       |     F    |      `int`     | All Immutables |
|    List    |   `list`  |        First-Class       |     T    |      `int`     |       All      |
|   String   |   `str`   |        `tup[chr]`        |     F    |      `int`     |      `chr`     |
|    Text    |   `text`  |        `list[chr]`       |     T    |      `int`     |      `chr`     |
|   Record   |   `rec`   |        First-Class       |     F    |      `str`     | All Immutables |
|    Data    |   `data`  |        First-Class       |     T    |      `str`     |       All      |
|     Map    |   `map`   |   `rec[tup[X], tup[Y]]`  |     F    | All Immutables | All Immutables |
| Dictionary |   `dict`  | `data[list[X], list[Y]]` |     T    | All Immutables |       All      |
| Brouwerian |   `brou`  |   `rec[nat, tup[nat]]`   |     F    |                |                |
|  Rational  |   `rat`   |      `rec[int, int]`     |     F    |                |                |


For those already familiar with other languages, this table describes the inspirations and analogous types in Lej:

|    Name    |                                                                Closest Analog Goals                                                                |
|:----------:|:--------------------------------------------------------------------------------------------------------------------------------------------------:|
|   Natural  | [Rust's `u8` to `u64` Types](https://doc.rust-lang.org/book/ch03-02-data-types.html#integer-types)                                                 |
|   Integer  | [Rust's `18` to `164` Types](https://doc.rust-lang.org/book/ch03-02-data-types.html#integer-types)                                                 |
|  Character | [Go's `rune` Type](https://go.dev/ref/spec#Rune_literals)                                                                                          |
|    Tuple   | [TypeScript's `ReadOnlyArray` Type](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-4.html#a-new-syntax-for-readonlyarray) |
|    List    | [Go's Array and Slice Types](https://go.dev/ref/spec#Array_types)                                                                                  |
|   String   | [Go's `string` Type](https://go.dev/ref/spec#String_types)                                                                                         |
|    Text    | [Ruby's `String` Type](https://ruby-doc.org/3.2.2/String.html)                                                                                     |
|   Record   | [Dart (3.0)'s `record` Type](https://github.com/dart-lang/language/blob/main/accepted/future-releases/records/records-feature-specification.md)    |
|    Data    | [Go's `struct` Type](https://go.dev/ref/spec#Struct_types)                                                                                         |
|     Map    | A Unique, Key-Sorted Analog to [Python's (Rejected) `frozendict` Type](https://peps.python.org/pep-0416/)                                          |
| Dictionary | A Unique, Key-Sorted Analog to [Go's `map` Type](https://go.dev/ref/spec#Map_types)                                                                |
| Brouwerian | Unique                                                                                                                                             |
|  Rational  | [Julia's Rational Number Type](https://docs.julialang.org/en/v1/manual/complex-and-rational-numbers/#Rational-Numbers)                             |

---
[Back to Table of Contents](#documentation)


