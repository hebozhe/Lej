# Control Flow

Lej's control flow involves three three main components: functions, conditionals, and loops. These components allow you to define the logic of your program and control the flow of data.

## `this` Blocks

A `this` block is a special type of block that allows you to define a scope for a set of statements. It is used to group related statements together and control the flow of data within a program.

They are used in control flow to define functions and loops. A `this` block consists of `this: ... \`, where the colon `:` and `\` enclose the block.

```
fun sum is this:
    take itr[N] ns;
    want N;

    give (ns at 0) + (sum with (ns from 1) as ns);
\
```

## Conditionals

Unlike most programming languages, Lej has more than just `if` and `else` expressions. Because Lej's semantics involve three primitive values (`true`, `false`, and `unsure`), conditionals must account for `unsure` evaluations, as well.

`if` blocks in Lej are written as `if B: ... \`, where `B` is an expression that evaluates to a Brouwerian. The block is executed if `B` is `true`.

`else` blocks in Lej are written as `else: ... \`. The block is executed if the preceding `if` block evaluates to `false`.

`otherwise` blocks in Lej are written as `otherwise: ... \`. The block is executed if the preceding `if` block evaluates to `unsure` or when an `else` block is not present and the preceding `if` block evaluates to `false`.

```
fun isPositive is this:
    take N n;
    want brou;

    if 0 < n: give true; \
    otherwise: give false; \
\

fun doesLEMHold is this:
    take brou b;
    want brou;
    know brou lem;

    lem is b or (not b);

    if lem: give true; \
    else: give false; \
    otherwise: give unsure; \
\
```

## Functions

Functions are used to group related statements together and perform a specific task. Functions can take arguments, must return values, and can be called from other parts of the program.

### Function Definitions

A minimal function definition consists of a name and a `this` block with a `want` statement and `give` statements at all possible exit points.

Three other statements are used in function definitions: `take` statements, `want` statements, and `know` statements. Their functionality is as follows:

| Function Statement           | Functionality           | Optional? |
|------------------------------|-------------------------|-----------|
| `take <PTYPE> <PNAME>, ...;` | Define parameters.      | Yes       |
| `want <RTYPE>;`              | Define the return type. | No        |
| `know <PTYPE> <PNAME>, ...;` | Define local variables. | Yes       |
| `give <VALUE>;`              | Return a value.         | No        |

These function statements must appear in the order shown above. If a function does not take any arguments, the `take` statement is omitted. If a function does not require any local variables, the `know` statement is omitted.

Every `give` statement's value (a name or expression) must match the `want` statement's type. This is enforced by the compiler.

```
fun max is this:
    take itr[comp] cs;
    want comp;

    if (len of cs) = 0:
        die with 
            "max Error: The iterable is empty." as message, 1 as code;
    \

    if (len of cs) = 1: give (cs at 0); \

    if (cs at 0) < (cs at 1):
        give max with (cs from 1) as cs;
    \

    give max with ((cs to 1) & (cs from 2)) as cs;
\
```

`know` statements, if present, must contain all and only the local variables used in the function. This carries a few benefits:
- It makes the function more readable by declaring all local variables at the beginning.
- It helps coders know which variables are local to the function and which are not.
- It discourages local variable overloading, which indicates a refactoring need.
- It eliminates the need to reassert local variables' types elsewhere in a function.

Any variable that's not declared in a `take` or `know` statement is assumed to be a global variable.

```
~sort implements a quicksort algorithm.~
fun sort is this:
    take itr[comp] cs;
    want itr[comp];
    know itr[comp] left, itr[comp] right, comp pivot, nat64 i;

    if (len of cs) < 2: give cs; \

    if (len of cs) = 2:
        if (cs at 0) < (cs at 1): give cs; \
        else: give (cs to 1) & (cs from 0); \
    \

    pivot is (cs at 0);
    left is {};
    right is {};
    i is 0;

    for some time, do this:
        i is i + 1;
        
        if i = (len of cs): out! \
        
        if pivot < (cs at i): 
            right is right & {cs at i};
        \
        otherwise:
            left is left & {cs at i};
        \
    \

    give (sort with left as cs) & {pivot} & (sort with right as cs);
\
```

### Function Calls

Because all functions return values, they must be captured by something that can accept them. This is usually a variable assignment or a `give` statement.

Function calls are written as `<FNAME> with X as <PNAME>, ...;`, where `<FNAME>` is the name of the function, `X` is some value, expression, or name, and `<PNAME>` is the name of the `<FNAME>`'s parameters, if any.

Parameters are passed to functions by name, not by position. This allows for more flexibility in function calls and makes the code more readable.

### Meta-Functions `live` and `die`

Meta-functions are functions that are built into the language and manage control flow beyond the internal scope of a Lej program, itself. In Lej, there are only two such functions:

- `live` is the entry point of a program. It is the first function called when a program is executed. It always returns an `int8` value, which is the program's exit status code. By convention, a `live` function should give `0` if the program executed successfully and any other value if it did not.
    - `live` is particularly unique in that it takes no `take` statements, because it is the entry point of the program and does not take any arguments.
- `die` is used to exit a program with an error message and a status code. Because Lej is interested in program correctness, any error "handled" by `die` is considered fatal (hence the name), and the program will exit immediately.
    - The parameters of `die` are `str message, int8 code`. The `message` parameter is a string that describes the error, and the `code` parameter is the status code that the program will exit with.
    - `die` is particularly unique in that it does not permit an assignment, because `die` provably returns no value to the program (because calling `die` exits the program).

```
fun live is this:
    want int8;
    know int8 x, int8 y;

    x is 5;
    y is 10;

    if x < y:
        give 1;

    give 0;
\
```

## For-Some-Time Loops

Loops in Lej come in one and only one form: `for some time, do this: ... \`. It's equivalent to a `while true` loop in other languages. However, this is double-edged. It's easier to write, but it's also easier to write non-terminating loops.

The `out!` statement is used to break out of a loop. It's equivalent to a `break` statement in other languages.

The `back!` statement is used to continue to the top of a for-some-time loop. It's equivalent to a `continue` statement in other languages.

### The `out!` Rule

As a rule, every for-some-time loop must have at least one `out!` statement to help ensure termination.

Lej encourages recursion over loops, as for-some-time loops are mainly here to handle asynchronous operations.

```
from http:
    take fun httpGet, rec[nat8, str] noResponseYet;
\
from time:
    take fun sleep, nat64 timeSecond;
\

fun getUrlRec is this:
    take txt url, nat8 waitSecs;
    want rec[nat8, str];
    know rec[nat8, str] resp;

    resp is noResponseYet;
    resp is httpGet with "http://example.com" as url;

    for some time, do this:
        if waitSecs = 0: out! \

        if not (status of resp) = 0:
            out!
        \

        _ is sleep with (1 * timeSecond) as howLong;
        waitSecs is waitSecs - 1;
    \

    give resp;
\
```

---

#### [Back to the Table of Contents](README.md)