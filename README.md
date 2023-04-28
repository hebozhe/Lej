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
