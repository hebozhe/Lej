# Lej:<br>Semantically Intuitionistic,<br>Syntactically Intuitive

Lej is a statically typed, compiled programming language. It's designed to work as a general-purpose language, since it focuses on features that make it approachable for beginners, though it also strives to be powerful enough for complex projects.

### The key features that set Lej apart from other languages are:

## Classical and Intuitionistic Access

Lej uses the triadic `true`-`unsure`-`false` values of [Kleene logic](https://en.wikipedia.org/wiki/Three-valued_logic#Kleene_and_Priest_logics) and a decision procedure for the logical operators `and`, `or`, and `not` that yield only intuitionistic tautologies. These values are called "Brouwerians" (`brou`).

## A Simple, Intuitive Syntax

Lej's syntax is primarily inspired by [Natural Semantic Metalanguage](https://intranet.secure.griffith.edu.au/schools-departments/natural-semantic-metalanguage/what-is-nsm/semantic-primes), and then by [Gricean-cooperative](https://en.wikipedia.org/wiki/Cooperative_principle) programming languages. 
    
- **Symbolic minimalism.** Lej rejects all "ASCII-art" operators like `<=`, `:=`, `++`, `+=`, etc. The symbolic operators that do exist are all single characters, and even those are limited if they're redundant (e.g., `<` is in Lej, but `>` is not).

- **Only one way to do things.** Lej tries to present a coder with only one obvious way to do things. The only loop in Lej is analogous to the unconditioned while-loop, and it's only there for asynchronous programming convenience (as Lej pushes recursion for iteration).

- **Unambiguity.** Lej is designed to be unambiguous in its syntax, and this is particularly true of scoping. The syntax not left-associative, is not right-associative, and has no operator precedence.

```
~A simple Lej program that prints "Hello, world!"~
a is (3 * 2) + 1; ~a is 7.~
b is 3 * (2 + 1); ~b is 9.~
c is 5 * 3 + 2; ~This throws and error.~
```

## Correct Code, No Exceptions

Since intuitionism requires that all proofs be constructive, Lej is designed to be a language where all code is correct by construction. This comes with a trade-off in terms of fault tolerance, but it also means that Lej is a language that can be reasoned about more easily.

- **Absolute functional purity.** Except for the `die` meta-function that kills program execution, all functions in Lej are pure. This means that they don't have side effects, and their return value is solely determined by their input values.

- **No null or undefined values.** Nothing resembling `null` or `undefined` is present in Lej. Undefined behavior throws an error.

- **No error handling.** Lej doesn't have exceptions or error handling. Programs in Lej are expected to be correct, and if they're not, the program will crash.

## A Thorough Type System

Lej employs a structural type theory with a focus on operators. This helps establish a direct correspondence between what syntactic choices are available to manipulate values of certain types.

- **A type system based on operators.** Built-in types in Lej are defined by what operators are permitted. Subtypes correspond to operational supersets. Here's an example hierarchy for some generic types:

| Generic | Operator Set                |
|---------|-----------------------------|
| `eval`  | `{=}`                       |
| `comp`  | `{=, <}`                    |
| `N`     | `{=, <, +, *, %}`           |
| `Z`     | `{=, <, +, *, %, -}`        |
| `Q`     | `{=, <, +, *, %, -, /, of}` |

- **Generic, immutable, and mutable subtyping.** Every generic in Lej has at most one immutable and one mutable subtype which actually allow for variable assignment. For example, the generic `N` has immutable subtypes `nat8`, `nat16`, `nat32`, and `nat64`, but no mutable subtypes. Structure types `sct`, however, have both the immutable record type `rec` and the mutable data type `data`.

- **Immutable _means_ immutable.** Immutable types in Lej are truly immutable. Once a value is assigned to a variable of an immutable type, its contents can't be changed, only overwritten. This has the effect of "freezing" all immutable container types in Lej.

- **Guaranteed precision.** Lej doesn't have floating-point arithmetic or the ability to leave values undefined. Instead, it has a generic `Q` (rational) type that guarantees precision by having `num` (numerator) and `den` (denominator) fields.

## Different Concurrent Programming

Thanks to Lej's `unsure` Brouwerian, it's easier to write concurrent logic that doesn't rely on locks or other synchronization primitives. This is because `unsure` values can be used to represent an indeterminate state of success in the execution of a concurrent operation.

```
~An asynchronous Lej program that runs one function concurrently with another.~
from madeUpModule:
    take fun asyncFun;
\
from time:
    take fun sleep, nat64 timeSecond;
\

fun twoAtOnce is this:
    take nat64 as retries;
    want brou;
    know brou success;

    success is unsure;

    ~Begin the asynchronous function.~
    success is asyncFun with "foo" as arg, "bar" as otherArg;

    ~Wait for the asynchronous function to finish.~
    for now, do this:
        
        if success or (not success): out! \
        
        _ is sleep with (1 * timeSecond) as howLong;
        retries is retries - 1;
        
        if retries = 0: give false; \
    \
    
    give success;
\

fun live is this:
    want int8;
    know brou success;

    success is twoAtOnce with 5 as retries;

    if success: give 0; \
    
    give 1;
\
```

---

#### [Back to the Table of Contents](README.md)