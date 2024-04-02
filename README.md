# **Lej**: A Semantically Intuitionistic, Syntactically Intuitive Language

# **Overview**
Lej (pronounced as "ledge") is a statically typed, compiled programming language that aims to provide a simple and intuitive syntax while allowing access to both classical and intuitionistic semantics. It is being developed under these maxims, in loose order of priority:

- **Access to both classical and intuitionistic worlds.** Brouwerian types work normally if you have only `true` and `false` values. `unsure` values behave reliably intuitionistically for the available logical operators.
- **Simple and intuitive syntax.** The syntax is designed to be easy to read and write for beginners and seasoned programmers alike. A single symbol does a single thing, for a single type.
- **Mandated functional purity.** Every function **_must_** return a value, no exceptions.
- **No undefined or null types.** Lej does not have a type for `None`, `nil`, `null`, `nix`, or any other empty value. `undefined` is an error, not a type.
- **Guaranteed precision.** There is no `float` type in Lej. Types are closed under their permitted operations, so there is no loss of precision in arithmetic operations.

# **Syntax**
The syntax of Lej is designed to be simple and intuitive. It is inspired by [the semantic primes of Natural Semantic Metalanguage](https://intranet.secure.griffith.edu.au/schools-departments/natural-semantic-metalanguage/what-is-nsm/semantic-primes), as well as the programming languages Ada, Dart, Delphi (Object Pascal), Go, Haskell, and Swift.

## **Comments**
All comments are multiline, and are enclosed by tildes `~`. Comments are not nestable.

```
~This is a comment.~

~This is
a multiline comment.~
```

## **Whitespaces and Newlines**
Whitespaces and newlines can separate tokens and statements.
Newlines to separate expressions or statements are not required, but can help make code more readable. Lej can be completely minified.

## **Statements**
Statements end with a semicolon `;`. In specific circumstances, some end with an exclamation mark `!`.

## **Parentheses**
Parentheses `()` are only used to disambiguate scope. All syntactic ambiguity must be resolved with parentheses.

```
int a is 5 * (3 + 2); ~a is 25.~
int b is (5 * 3) + 2; ~b is 17.~
int c is 5 * 3 + 2; ~Error: c is ambiguous.~
```

## **Code Blocks**
Code blocks are opened with a colon `:` and closed with a backslash `\`. They are used to group statements together under a control flow (function definitions, conditionals, and do-times loops).

## **Names**
Names refer to variables, functions, and types. They must be formatted as alphanumeric, camelCase strings that start with a lowercase letter (e.g., `myVariable`, `myFunction`, `myType`).
The only special name is `_`, which is used to assign a variable that is never referred to elsewhere.

## **Variables**
Lej assigns variables via the statement format `<TYPE> <NAME> is <VALUE>;`
The variable type must be declared the first time it is used and it must never be declared again. (e.g., `int16 a is 5; a is a + 1;`)

## **Control Structures**
There are three control structures in Lej: conditionals, functions, and do-times loops.

## **Functions**
Functions are defined via the format `fun <NAME> is this: ... \`.

### **Function Keywords**
There are four reserved keywords for functions: `take`, `want`, `know`, and `give`. The following table describes their usage:

| Keyword | Format                                    | Usage                | Required |
|---------|-------------------------------------------|----------------------|----------|
| `take`  | `take <TYPE> <NAME>, <TYPE> <NAME>, ...;` | Function arguments   | No       |
| `want`  | `want <TYPE>;`                            | Expected return type | Yes      |
| `know`  | `know <TYPE> <NAME>;`                     | Local variables      | No       |
| `give`  | `give <VALUE>;`                           | Return value         | Yes      |

The order in which `take`, `want`, and `know` are provided in a function definition is strict.

`know` statements must contain every distinct local variable used in a function. Lej assumes that any variable not declared in a `know` statement is a modular or global variable, even if its type is declared in an assignment statement. The only exception to this is a variable with the `_` name, as it will not be used in the function.

### **Function Calls**
Function calls are made via the format `<FUNCTION-NAME> with <VAR-NAME|VALUE> as <PARAM-NAME>, <VAR-NAME|VALUE> as <PARAM-NAME>, ...;`.
The `with` expression is required to pass parameters to a function.
Each `as` expression designates the corresponding parameter names in a function's definition. Thus, the parameter input order does not matter.


### **Example Functions**
```
fun factorial is this:
    take Z n;
    want Z;

    if n = 0: give 1; \

    give n * (factorial with n - 1 as n);
\

fun trim is this:
    take str s;
    want str;
    know tup[chr] whitespaces;

    if s = "": give s; \

    whitespaces is (' ', '\t', '\n', '\r');

    if (s from 0 to 1) in whitespaces:
        give trim with (s from 1 to (len of s)) as s; 
    \
    if (s from (len of s) - 1 to (len of s)) in whitespaces:
        give trim with (s from 0 to (len of s) - 1) as s;
    \

    give s;
\
```

## **Conditionals**
Conditionals are defined via the format `if <BROU>: ... \ (else: ... \) (otherwise: ... \)`. The `else` and `otherwise` blocks are optional.
Due to Lej's intuitionistic semantics, the behavior of the control flow is different from that of Boolean semantics:
- The `if` block is entered if the resulting `brou` evaluates to `true`.
- The `else` block is entered if the `if` block evaluates to `false`.
- The `otherwise` block is entered when:
    - The `if` block evaluates to `unsure`, or
    - The `if` block evaluates to `false` and the `else` block is absent.

```
fun isPalindrome is this:
    take str s;
    want brou;

    if (len of s) < 2: give true; \

    if (s at 0) = (s at ((len of s) - 1)):
        give isPalindrome with (s from 1 to ((len of s) - 1)) as s; 
    \

    give false;
\
```

# **Semantics**
The semantics of Lej is a primitives-to-composites type system, with types defined as the set of built-in operations that can be performed on them.

While all primitive types are immutable, composite types are named separately according to their mutability.
All immutable composite types are also frozen, meaning that they cannot be modified after they are created.

## **Primitive Types**
| Operator Set                  | Primitive (Generic) Type | Subtypes               | Primitive Values            |
|-------------------------------|--------------------------|------------------------|-----------------------------|
| {}                            | Functions (`fun`)        |                        |                             |
| `fun`                         |                          | Functions (`fun`)      |                             |
| {`=`}                         | Evaluables (`eval`)      |                        |                             |
| `eval` ∪ {`and`, `or`, `not`} | Brouwerians (`brou`)     |                        |                             |
| `brou`                        |                          | (`brou`)               | {`true`, `false`, `unsure`} |
| {`=`, `<`}                    | Comparables (`comp`)     |                        | {`many`}                    |
| `comp` ∪ {`+`, `*`, `%`}      | Naturals (`N`)           |                        |                             |
| `N`                           |                          | (`nat8`, ..., `nat64`) | {0. 1, 2, 3, 4, ...}        |
| `N`                           |                          | Bytes (`byte`)         |                             |
| `N` ∪ {`-`}                   | Integers (`Z`)           |                        |                             |
| `Z`                           |                          | (`int8`, ..., `int64`) | {..., -2, -1, 0, 1, 2, ...} |

## **Composite Types**
| Operator Set                                   | Generic Type       | Immutable (and Frozen) Subtype | Mutable Subtype          |
|------------------------------------------------|--------------------|--------------------------------|--------------------------|
| `eval` ∪ {`of`}                                | Structures (`sct`) |                                |                          |
| `sct`                                          |                    | Records (`rec`)                | Data (`data`)            |
| `sct` ∪ `Z` ∪ {`/`, `.`}                       | Rationals (`Q`)    |                                |                          |
| `Q`                                            |                    | (`rat8`, ..., `rat64`)         |                          |
| `rec` ∪ {`at`, `from`, `to`, `&`}              | Iterables (`itr`)  |                                |                          |
| `itr`∪ {`{...}`}                               |                    | Tuples (`tup`)                 | Lists (`list`)           |
| `itr` ∪ `comp` ∪ {``` `...` ```}               | Glyphs (`gly`)     |                                |                          |
| `gly`                                          |                    | Marks (`mrk`)                  | Runes (`rune`)           |
| `itr` ∪ `comp` ∪ {`'...'`}                     | Graphemes (`gph`)  |                                |                          |
| `gph`                                          |                    | Characters (`chr`)             | Phemes (`pheme`)         |
| `itr` ∪ `comp` ∪ {`"..."`}                     | Textuals (`txt`)   |                                |                          |
| `txt`                                          |                    | Strings (`str`)                | Character Texts (`ctxt`) |
| `txt`                                          |                    |                                | Pheme Texts (`ptxt`)     |
| `itr` ∪ {`{<KEY> <VALUE>, ...}`, `where`, `K`} | Lookups (`lkp`)    |                                |                          |
| `lkp`                                          |                    | Maps (`map`)                   | Dictionaries (`dict`)    |

## **Evaluables**
Because the `=` operator checks for deep value equality, every type in Lej is an evaluable.
The rules governing the behavior of the `=` operator vary slightly by type, but it performs a deep value comparison for all types.

The level of evaluation will is the lowest common supertype of the two compared types. For example, comparing `N` and `Z` values will result in a `N`-type comparison. If the lowest common supertype is `eval`, the evaluation is always `false`.

This obeys the [bundle theory of identity](https://en.wikipedia.org/wiki/Bundle_theory).

## **Brouwerians**
Brouwerians replace Booleans as the primary logical value type in Lej. Their semantics follows Kleene logic, a three-valued logic that includes a third value, `unsure`, to represent the uncertainty of a statement's truth value. To make it intuitionistic, Brouwerian evaluations also check whether a Boolean contradiction results at any point in the evaluation.

### **Brouwerian Operator Behavior**
Where `a`, and `b` are among the primitives {`true`, `false`, `unsure`}, the following rules apply:
- `a = b`:
    - If `a` and `b` are both either `true` or `false`, the result is the same as in Boolean algebra.
    - If either `a` or `b` is `unsure`, the result is `unsure`.
- `a and b`:
    - If `a` is `true`, the result is `b`.
    - If `a` is `unsure`, the result is `unsure` if `b` is `true` or `unsure`, and `false` if `b` is `false`.
    - If `a` is `false`, the result is `false`.
- `a or b`:
    - If `a` is `true`, the result is `true`.
    - If `a` is `unsure`, the result is `true` if `b` is `true`, and `unsure` if `b` is `unsure` or `false`.
    - If `a` is `false`, the result is `b`.
- `not a`:
    - If `a` is `true`, the result is `false`,
    - If `a` is `unsure`, the result is `unsure` if it's not also a classical contradiction, and `false` if it is.
        - [Lej uses a lemma of Gilvenko's theorem and some elaborations on Kleene algebra as its decision procedure.](https://math.stackexchange.com/questions/4847894/can-this-classical-kleene-combination-for-intuitionistic-fragment-neg-vee).
    - If `a` is `false`, the result is `true`.

## **Comparables**
Comparables are evaluables that can also be compared with the `<` operator. Naturals, integers, rationals, bytes, glyphs, graphemes, and textuals are comparables.

## **Naturals and Integers**
Naturals and integers are comparables that can also be added, subtracted, multiplied, and moduloed. They are also the only types that can be infinite.
The difference between integers and naturals is that integers can be negative, while naturals cannot.

Their operator behaviors for naturals and integers are widely known, so they will not be listed here.

However, there is _no overflow or underflow_ in Lej. If a natural or integer exceeds its maximum value or goes below its minimum value, it throws an error.

## **Bytes**
Bytes are an alias of `nat8`, though their primary purpose in Lej's ontology is to construct glyphs.
Lej enforces this naming convention to separate arithmetic operations on `nat8` from the construction of glyphs.

## **Structures**
Structures are evaluables that can also be accessed by their fields.

### **Structure Syntax**
Structures are defined via the format `(rec|data) <NAME> is this: <FIELD-NAME> <TYPE>; ... \`.

```
data person is this:
    name str;
    age nat;
    isMarried brou;
```

Structures are are initialized via the format `<NAME-OF-SCT> with <VALUE> as <FIELD-NAME>, <VALUE> as <FIELD-NAME>, ...;`.

```
person p is person with "John Doe" as name, 30 as age, false as isMarried;
```

### **Structure Operator Behavior**
Where `a` and `b` are both structures, the following rules apply:
- `a = b`:
    - If `a` and `b` have the same fields and the values of those fields are equal, the result is `true`.
    - Otherwise, it's false.
- `<NAME> of a`:
    - The result is the value of the field `<NAME>` in `a`.

## **Records and Data**
Records and data are structures with their mutability defined. Records are immutable and frozen, while data is mutable.

## **Rationals**
Rationals are comparables that can also be divided and allow for decimal notation.

Decomposed, rationals are specialized `rec[int8, NX, NX]`, where `X` is the numeral in `ratX`, where the `X` is one of the available bit-widths for rationals.

### **Rational Fields***
- `pos` is a `int8` representing the sign. It houses one of only three values: `1` for positive, `0` for zero, and `-1` for negative.
- `num` is an `natX` representing the numerator.
- `den` is an `natX` representing the denominator.

All rationals auto-simplify. Ergo `rat a is 50/100;` is equivalent to `rat a is 1/2;`.

### **Rational Operator Behavior**
Where `a` and `b` are both both comparables, the following rules apply:

- All of the rules of naturals apply to rationals.
- `a = b`:
    - If the `pos`, `num`, and `den` fields of `a` and `b` are all equal, the result is `true`.
    - Otherwise, it's false.
- `a / b`:
    - The result is a simplified `ratN`.
        - `pos` holds its positive, negative, or zero value;
        - `num` holds the simplified numerator of `a` divided by `b`;    
        - `den` holds the simplified denominator of `a` divided by `b`.

Where `a` and `b` are both numeric literals:

- `a.b`:
    - Where the numeral `b` is of length `n`, the result is equivalent to `ratN` build by the formula "((a^n) + b) / (10^n)".
        - For example, `3.14` is equivalent to `314/100`, is equivalent to `157/50`, the final input.

## **Iterables**
Iterables are numerically indexable, sliceable, and concatenatable collections of elements. They are the only types that can be iterated over in Lej.

Decomposed, iterables are specialized `rec[nat, arr[T]]`, where `T` is the type of the elements in the iterable, which is defined by its type signature `iter[T]`.

### **Iterable Fields**
- `len` is an `nat64` representing the length of the iterable.
- `arr` is an array of type `T` representing the elements of the iterable.
    - Arrays cannot be directly called or modified. They can only be accessed via their legal operators.

### **Iterable Operator Behavior**
Where `a` and `b` are both iterables, the following rules apply:

- All of the rules of records apply to iterables.
- `a = b`:
    - If the `len` and `arr` fields of `a` and `b` are equal, the result is `true`.
    - Otherwise, it's false.
- `a at n`:
    - Where `n` is a `nat64`, the result is the `n`th element of `a`.
    - If `n` is greater than or equal to the length of `a`, the program throws an error.
- `a from n to m`:
    - The result is a new iterable that contains the elements of `a` from the `n`th to the `m`th element.
        - Elements are 0-indexed in Lej.
- `a & b`:
    - The result is a new iterable that contains the elements of `a` followed by the elements of `b`.

### **Iterable Operator Behavior**
Where `a` and `b` are both tuples or both lists, the following rules apply:

- All of the rules of iterables apply to tuples and lists.
- `{<VALUE>, ...}`:
    - The result is a new tuple or list that contains the given values.

## **Tuples and Lists**
Tuples and lists are iterables that are immutable and frozen, and mutable, respectively.

## **Glyphs**
Glyphs are special records of bytes for UTF-8 Unicode character convention. They represent a single Unicode code point, which is the basis for graphemes in Lej. Glyphs are a supertype of marks and runes.

Decomposed, glyphs are `rec[tup[byte], nat32, utf8]` where the first element is the byte sequence of the Unicode code point, and the second element is the Unicode code point itself, and the third element is the visual UTF-8 encoding of the Unicode code point.

### **Glyph Fields**
- `bytes` is a `itr[byte]` representing the byte sequence of the Unicode code point.
- `code` is a `nat32` representing the Unicode code point.
- `utf8` is a `utf8` representing the UTF-8 encoding of the Unicode code point.

### **Glyph Operator Behavior**
Where `a` and `b` are both glyphs, the following rules apply:

- All of the rules of records apply to glyphs.
- All of the rules of comparables apply to glyphs.
- `a = b`:
    - If the `bytes`, `code`, and `utf8` fields of `a` and `b` are all equal, the result is `true`.
        - Only the `bytes` field is actually compared for equality, though, as the `code` and `utf8` fields are derived from the `bytes` field.
    - Otherwise, it's false.
- `a < b`:
    - The result is `true` if the `code` field of `a` is less than the `code` field of `b`.
    - Otherwise, it's false.
- ``` `...` ```:
    - This syntax requires the insertion of a "character" that takes up a single Unicode code point.
        - For example, in Spanish, the character `ñ` is a single Unicode code point, so it can be represented as, say, a mark with ```mrk nWithTilde is `ñ`;```.
        - For another example, in Hindi, the character `क्` is a combination of two Unicode code points, so it cannot be represented as, say, a rune.
            - Instead, one rune for each Unicode code point would be needed, like so: ```rune ka is `क`; rune virama is `्`;```.

### **Marks and Runes**
Marks and runes are both glyphs. Marks are immutable and frozen, while runes are mutable.

## **Graphemes**
Graphemes are iterables of runes. Their two subtypes are characters and phemes.

## **Characters and Phemes**
Characters and phemes are both iterables. Characters, along with being immutable, are also frozen, meaning that their defined elements cannot be modified after they are created, but they can be overwritten. Phemes, on the other hand, are mutable and their elements can be modified after they are created, so long as they are also mutable.

Decomposed, characters are equivalent to `tup[rune]`, while phemes are equivalent to `list[rune]`.

### **Character and Pheme Operator Behavior**
Where `a` and `b` are both characters or both phemes, the following rules apply:

- All of the rules of iterables apply to characters and phemes.
- `'...'`:
    - The result is a new character or pheme.
    - Only one character or pheme can exist. However, since characters and phemes are iterables of runes, the runes, themselves, can be iterated over.

## **Textuals**
Textuals are iterables of characters or phemes. All textual subtypes are fundamentally syntactic sugar for the possible `tup[chr]`, `list[chr]`, and `list[pheme]` subtypes.

### **Textual Operator Behavior**
Where `a` and `b` are both textuals, the following rules apply:

- All of the rules of iterables apply to textuals.
- `"..."`:
    - The result is a new textual.

## **Strings, Character Texts, and Pheme Texts**
Strings, character texts, and pheme texts are all textuals. Strings, along with being immutable, are also frozen, meaning that their defined elements cannot be modified after they are created, but they can be overwritten. Character texts and pheme texts, on the other hand, are mutable and their elements can be modified after they are created, so long as they are also mutable.

Decomposed, strings are equivalent to `tup[chr]`, while character texts and pheme texts are equivalent to `list[chr]` and `list[pheme]`, respectively.

## **A Note Regarding Textuals, Graphemes, Runes, and Bytes**
Lej is unique in that it attempts to regard every level of the Unicode standard as a separate type. This is because the Unicode standard is a complex standard that must reconcile our folk-theoretic understanding of orthography with the reality of the digital world. This is why Lej has separate types for textuals, graphemes, runes, and bytes.

Essentially:
- Textuals are the type for all of the conventional notions entailed by the name.
- Graphemes are the type for the notion of a "character" whereby use of an arrow key, for instance, passes over a collection of Unicode points.
- Runes are the type for the notion of a "character" that has a distinct visually recognizable form available in the Unicode standard, which in some cases is more akin to an "accent" or a "stroke" by our folk-theoretic understanding.
- Bytes are the base numeric representations needed to generate every Unicode point available in the Unicode standard.

## **Lookups**
Lookups are iterables that are used to store key-value pairs. Their two subtypes are maps and dictionaries.
Lookups, however, are not hash maps. They're key-sorted and value-aligned iterable pairs, meaning that their `keys` and `values` attributes are sorted and aligned in ascending order by the `keys` elements' values, so programmers can iterate over them in a predictable manner.

### **Lookup Fields**
- `keys` is an `itr[T]`, where `T` is the type of the keys of the lookup.
- `values` is an `itr[U]`, where `U` is the type of the values of the lookup.

### **Lookup Operator Behavior**
Where `a` and `b` are both lookups, the following rules apply:

- All of the rules of iterables apply to lookups.
    - However, they specifically apply to `keys` and `values`.
- `{<KEY> <VALUE>, ...}`:
    - The result is a new lookup that contains the given key-value pairs.
- `a = b`:
    - If the `keys` and `values` fields of `a` and `b` are equal, the result is `true`.
    - Otherwise, it's false.
- `a where k`:
    - The result is the `nat64` index where `k` is found in `keys of a`.
    - If `k` is not found in `keys of a`, the result is `len of (keys of a)`.
- `a at (K k)`:
    - When retrieving a value from a lookup:
        - Where `k` is of the same type as those of `keys of a`, the result is the value stored in the matching index of `values of a`.
        - If `k` is not found in `keys of a`, the program throws an error.
    - When assigning a new value to a lookup:
        - Where `k` is of the same type as those of `keys of a`, the value stored in the matching index of `values of a` is overwritten with `v`.
        - If `k` is already in `keys of a`, `v` is overwritten in `values of a` at the index where `k` is found.
        - If `k` is not found in `keys of a`, `k` is inserted into `keys of a` at the sorted index, and `v` is inserted into `values of a` at the same index.
- `a from (K kM) to (K kN)`:
    - The result is a new lookup that contains the key-value pairs of `a` from the index where `kM` is found to the index where `kN` is found.
        - If `kM` is not found in `keys of a`, the program throws an error.
        - If `kN` is not found in `keys of a`, the program throws an error.
        - If `kM` is found after `kN`, the program throws an error.
- `a & b`:
    - The result is a new lookup that updates the key-value pairs of `a` with the key-value pairs of `b`.
        - If a key in `b` is already in `a`, the value in `a` is overwritten with the value in `b`.
        - If a key in `b` is not found in `a`, the key-value pair is added to `a`.

## **Maps and Dictionaries**
Maps are lookups that are immutable and frozen, meaning that their defined elements cannot be modified after they are created, but they can be overwritten. Dictionaries, on the other hand, are mutable and their elements can be modified after they are created, so long as they are also mutable.

Decomposed, maps are equivalent to `tup[tup[T], tup[U]]`, where `T` and `U` are the types of the keys and values, respectively, while dictionaries are equivalent to `list[list[T], list[T]]`.

# **FAQ**

#### **Why is Lej called "Lej"?**
Lej is named for the initials of Ludwig Egbertus Jan Brouwer, the Dutch mathematician who founded the intuitionistic school of mathematics. In computer science, Brouwer's name tied to the Heyting-Kolmogorov-Brouwer interpretation which, among other things, defines the relationship between Gentzen's intuitionistic natural deduction and the lambda calculus.

#### **Why is there an `unsure` value?**
The `unsure` value, along with Kleene logic and an exploit of Gilvenko's theorem, provides a complete intuitionistic semantics for the intuitionistic operational fragment {`and`, `or`, `not`}. The use cases for `unsure` is left to the programmer's discretion, though it has some _prima facie_ value in working with asynchronous or concurrent systems, where the success or failure of a task is not known until it terminates.

One example of this is server-client communication, like an API call, where the client doesn't know whether the server received and correctly processed a message until the client receives a response. In such cases, a default `unsure` value can be assigned to indicate that the client awaiting a response from the server, and then be re-assigned to `true` or `false` based on the success or failure, respectively, of the call.

#### **Why are there no true hash maps?**
Hash maps do not align with intuitionistic logic because their location is unprovable, as hash-maps are non-deterministic. Lej's `map` and `dict` types are deterministic and ordered (the way print dictionaries are). This increases the lookup time from O(1) to O(n log n), but it comes with other benefits:
- The probability of a hash collision is zero.
- They do not require a hash function to be computed for each key.
- Their `keys` and `values` attributes are sorted and aligned in ascending order by the `keys` elements' values, so programmers can iterate over them in a predictable manner.
- The added time complexity is not a significant issue for small data sets, and their deterministic nature makes them more reliable for larger data sets.
- It is possible to remove `dict` key-value pairs in bulk, which is not possible with hash maps.
- Simply swapping the `keys` and `values` attributes into a new `map` or `dict` provides easy reverse-lookup functionality.
- They prevent the overuse of hash maps when `rec` and `data` types would be better options, which can lead to performance issues in large-scale systems.
