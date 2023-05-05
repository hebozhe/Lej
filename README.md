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
    - [**Primitive Values**](#primitive-values) (`T`, `U`, and `F`)
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

## **Punctuations**
---
Because Lej can be minified, punctuation plays a major role in organizing sections of the language.

---

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
    \
```
---

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

### **Primitive Values**
---
The primitive Brouwerians `T` and `F` work exactly as their Boolean counterparts. They evaluate to all of the classical (Boolean) evaluations when used on their own. However, every literal `U` ("unknown") in a program refers to a unique valuation.

Example:
```
def brou thisUnsure as U;
def brou lncWithOneUnsure as not [thisUnsure and not thisUnsure]; `← Evaluates to T, since thisUnsure refers to a single unsure value.`
def brou lncWithTwoUnsures as not [U and not U]; `← Evaluates to U, since both U variables occupy different possible truth-values.`
```
---

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

