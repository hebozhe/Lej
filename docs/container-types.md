# Container Types

Container types are built-in types in Lej whose construction depends on other constituent types. They are used to store and manipulate data in a structured way.

Syntactically, container type signatures are of the form `C[T1, T2, ..., Tn]`, where `C` is the container type and `T1, T2, ..., Tn` are the constituent types. The constituent types are separated by commas and enclosed in square brackets.

### Mutability and Immutability

In Lej, _mutability_ for container types is defined in terms of the ability to change the container's constituents. Conversely, _immutability_ means that the container's constituents cannot be changed once the container is created (known in languages like Python as "frozen").

Generic container types exist to permit the use of mutable and immutable containers, for instance, in a function's `take` and `want` statements. However, they cannot be used for variable assignments, so the programmer must choose the appropriate container type to control the mutability of the data in his program. When generics are used, a coder should be aware that the minimum functionality of the two types is what's permitted, so every generic container type used is immutable.

In the more conventional usage, all Lej types are immutable in the sense that their only way to be changed (for example, in terms of size) is to be reassigned. This is a design choice to make the language more predictable and easier to reason about. Without in-place changes, the programmer can be more confident about the state of the program at any given time.

This also corresponds to the definition of identity in Lej as "deep equality" (i.e., two values are equal if the _values_ of their constituents are equal, not just their references).

### The Mutability-Immutability Cascade

Because, by definition, immutable containers cannot be changed, their constituents are never allowed to be mutable. The Lej parser enforces this, so it's disallowed at a syntactic level.

However, mutable containers can contain both mutable and immutable constituents. Hence, mutability "cascades" to immutability, but not the other way around.

## Structures

Structures are Lej's most basic container type. They group together a fixed number of values of different types into a single unit. They belong to the following operational hierarchy:

| Generic Type | Immutable | Mutable | Operator Set |
|--------------|-----------|---------|--------------|
| `eval`       |           |         | {`=`}        |
| `sct`        | `rec`     | `data`  | {`=`, `of`}  |

### Records (and Data)

_Note: Only records (`rec`) are explicitly covered here, but the syntax and semantics of data (`data`) are identical except for mutability._

Records are assigned in Lej using the syntax `rec[T1, T2, ..., Tn] <NAME> is this: take <T1> <T1-NAME>, <T2> <T2-NAME>, ..., <Tn> <Tn-NAME>; ... \`, where `T1, T2, ..., Tn` are the constituent types and `<NAME>` is the name of the record, and `<T1-NAME>, <T2-NAME>, ..., <Tn-NAME>` are the names of the constituents.

### Operator `of`

The selected names of a record's constituents are what Lej can recognize to access them. The names are used in the `of` operator to access the constituents of a record.

```
from io:
    take fun putText;
\

~The record definition is global.~
rec[nat8, str] person is this: take nat8 age, str name; \

fun isAdult is this:
    take rec[nat8, str] thisPerson;
    want brou;

    give 17 < (age of thisPerson);
\

fun live is this:
    want int8;
    know rec[nat8, str] johnDoe;

    johnDoe is person with 25 as age, "John Doe" as name; \
    
    if (isAdult with johnDoe as thisPerson):
        _ is putText with "John Doe is an adult.\n" as ptxt;
    else:
        _ is putText with "John Doe is not an adult.\n" as ptxt;
    \

    give 0;
\

```

### Differences from Conventional Structures

The above example, however, is exposed to a possible error. There is no particular reason to assume that the `rec[nat8, str]` type has the same field names as the `rec[nat8, str]` named `person`. Therefore, the `(age of thisPerson)` expression is not guaranteed to exist, and the compiler will throw an error if it is not found.

Most programming languages allow custom type definitions at this level. Lej does not, because it negatively affects the ability of a coder to understand how a structure is structured and makes code less reusable.

In this case, changing the parameter to just be what is stored in the `age` constituent of the record would be a better choice.

```
from io:
    take fun putText;
\

rec[nat8, str] person is this: take nat8 age, str name; \

fun isAdult is this:
    take nat8 age;
    want brou;

    give 17 < age;
\

fun live is this:
    want int8;
    know rec[nat8, str] johnDoe;

    johnDoe is person with 25 as age, "John Doe" as name; \
    
    if isAdult with (age of johnDoe) as age:
        _ is putText with "John Doe is an adult.\n" as ptxt;
    \
    else:
        _ is putText with "John Doe is not an adult.\n" as ptxt;
    \

    give 0;
\
```

However, if, perhaps, some dedicated activity will only affect a single record type, then the first example may be more appropriate, and the more advisable solution could be to store that specific functionality into a module.

## Iterables

Iterables are container types that can be iterated over. They belong to the following operational hierarchy:

| Generic Type | Immutable | Mutable | Operator Set                         |
|--------------|-----------|---------|--------------------------------------|
| `eval`       |           |         | {`=`}                                |
| `sct`        |           |         | {`=`, `of`}                          |
| `itr`        | `tup`     | `list`  | {`=`, `of`, `at`, `from`, `to`, `&`} |

### Tuples (and Lists)

_Note: Only tuples (`tup`) are explicitly covered here, but the syntax and semantics of lists (`list`) are identical except for mutability._

Tuples are assigned in Lej using the syntax `tup[T]`, where `T` is the constituent type, where `T` is the constituent type.

Decomposed, tuples (`tup`) are of the type `rec[nat64, seq[T]]`, where `nat64` is the length of the tuple and `seq[T]` is the sequence of elements of the type `T` indicated in the type signature `tup[T]`. The `seq` type is a sequence of elements of the same type, but it is not directly callable. The named fields are shown in the following code snippet:

```
rec[nat64, seq[T]] tup is this: take nat64 len, seq[T] eles; \
~eles is an uncallable field.~
```

Lists, respectively, are of the type `data[nat64, seq[T]]`, where `nat64` is the length of the list and `seq[T]` is the sequence of elements of the type `T` indicated in the type signature `list[T]`. The `seq` type is a sequence of elements of the same type, but it is not directly callable. The named fields are shown in the following code snippet:

```
data[nat64, seq[T]] list is this: take nat64 len, seq[T] eles; \
~eles is an uncallable field.~
```


### Literals with `{...}`.

Iterable literals are written as a comma-separated sequence of values enclosed in curly braces `{...}`. The values are of the same type as the tuple's constituent type.

```
tup[nat8] oneThroughFive is {1, 2, 3, 4, 5};
```

### Operator `at`

The `at` operator is used to access one element of an iterable by its index. The index is zero-based. All of the normal indexing errors apply, such as out-of-bounds errors.

```
from io:
    take fun putText, fun formatN;
\
from math:
    take fun min;
\

fun live is this:
    want int8;
    know tup[nat8] oneThroughFive;

    oneThroughFive is {1, 2, 3, 4, 5}; \

    _ is putText with "The minimum of the tuple is " as ptxt;
    _ is putText with (formatN with (min of oneThroughFive) as n) as ptxt;

    give 0;
\
```

In the case of lists, the `at` operator can also reassign elements.

```
from io:
    take fun putText, fun formatN;
\
from math:
    take fun min;
\

fun live is this:
    want int8;
    know list[nat8] oneThroughFive;

    oneThroughFive is [1, 2, 3, 4, 5]; \

    _ is putText with "The minimum of the list is " as ptxt;
    _ is putText with ((formatN with (min of oneThroughFive) as n) & "\n") as ptxt;

    (oneThroughFive at 0) is 6; \

    _ is putText with "The minimum of the list is " as ptxt;
    _ is putText with ((formatN with (min of oneThroughFive) as n) & "\n") as ptxt;

    give 0;
\
```

### Operators `from` and `to`

The `from` and `to` operators are used to create a new iterable from a sub-iterable (i.e., a slice) of the elements of an existing tuple. The `from` operator specifies the starting index (inclusive), and the `to` operator specifies the ending index (exclusive).

The full syntax is `<NAME> from <START> to <END>`, where `<NAME>` is the name of the new iterable, and `<START>` and `<END>` are the indices. The `from <START>` and `to <END>` are optional, and if omitted, the default values are `from 0` and `to (len of <NAME>)`, respectively.

```
from io:
    take fun putText, fun formatN;
\
from math:
    take fun min;
\

fun live is this:
    want int8;
    know tup[nat8] oneThroughFive;

    oneThroughFive is {1, 2, 3, 4, 5}; \

    _ is putText with "The minimum of the tuple is " as ptxt;
    _ is putText with ((formatN with (min of oneThroughFive) as n) & "\n") as ptxt;

    oneThroughThree is (oneThroughFive from 0 to 3); \

    _ is putText with "The minimum of the tuple is " as ptxt;
    _ is putText with ((formatN with (min of oneThroughThree) as n) & "\n") as ptxt;

    give 0;
\
```

In the case of lists, the `from` and `to` operators can also reassign elements.

```
from io:
    take fun putText, fun formatN;
\
from math:
    take fun min;
\

fun live is this:
    want int8;
    know list[nat8] oneThroughFive;

    oneThroughFive is [1, 2, 3, 4, 5]; \

    _ is putText with "The minimum of the list is " as ptxt;
    _ is putText with ((formatN with (min of oneThroughFive) as n) & "\n") as ptxt;

    oneThroughFive from 0 to 3 is {6, 7, 8}; \

    _ is putText with "The minimum of the list is " as ptxt;
    _ is putText with (formatN with (min of oneThroughFive) as n) & "\n" as ptxt;

    give 0;
\
```

### Operator `&`

The `&` operator is used to concatenate two iterables. The two iterables must have the same constituent type.

```
from io:
    take fun putText, fun formatItr;
\

fun live is this:
    want int8;
    know tup[nat8] oneThroughThree, tup[nat8] fourThroughFive;

    oneThroughThree is {1, 2, 3};
    fourThroughFive is {4, 5};

    oneThroughFive is (oneThroughThree & fourThroughFive);

    _ is putText with "The tuple is " as ptxt;
    _ is putText with ((formatItr with oneThroughFive as i) & "\n") as ptxt;

    give 0;
\
```

## Glyphs

Glyphs are container types that can be used to store a single Unicode code point. They belong to the following operational hierarchy:

| Generic Type | Immutable | Mutable | Operator Set                              |
|--------------|-----------|---------|-------------------------------------------|
| `eval`       |           |         | {`=`}                                     |
| `comp`       |           |         | {`=`, `<`}                                |
| `sct`        |           |         | {`=`, `of`}                               |
| `itr`        |           |         | {`=`, `of`, `at`, `from`, `to`, `&`}      |
| `gly`        | `mrk`     | `rune`  | {`=`, `<`, `of`, `at`, `from`, `to`, `&`} |

### Marks (and Runes)

_Note: Only marks (`mrk`) are explicitly covered here, but the syntax and semantics of runes (`rune`) are identical except for mutability._

Decomposed, marks (`mrk`) are of the type `tup[byte]`. The byte types are specifically used to label `nat8` values that are used to encode Unicode code points.

Decomposed, runes (`rune`) are of the type `list[byte]`.

### Literals with ``` `.` ```

Glyph literals are written as a single Unicode code point enclosed in backticks `` `.` ``. However, only a single Unicode code point can be stored in a glyph.

```
mrk a is `a`;
mrk accentMark is `´`;
```

### A Warning on `&` with Glyphs

The `&` operator is defined for glyphs. However, this does not guarantee that the resulting glyph will be a valid Unicode code point. If it is not, the compiler will throw an error.

## Graphemes

While glyphs hold Unicode code points, our conventional notion of a "character" is more complex. A grapheme ("character") can be composed of multiple Unicode code points, such as the the accent mark glyph ``` `´` ``` with alphabet glyph ``` `e` ```. These together form the grapheme `'é'`. Graphemes are Unicode characters that are displayed as a single unit, which is a collection of Unicode code points.

Graphemes are container types that can be used to store a single Unicode grapheme. They belong to the following operational hierarchy:

| Generic Type | Immutable | Mutable | Operator Set                              |
|--------------|-----------|---------|-------------------------------------------|
| `eval`       |           |         | {`=`}                                     |
| `comp`       |           |         | {`=`, `<`}                                |
| `sct`        |           |         | {`=`, `of`}                                |
| `itr`        |           |         | {`=`, `of`, `at`, `from`, `to`, `&`}      |
| `gph`        |           |         | {`=`, `<`, `of`, `at`, `from`, `to`, `&`} |
| `gly`        |           |         | {`=`, `<`, `of`, `at`, `from`, `to`, `&`} |
| `gph`        | `chr`     | `pheme` | {`=`, `<`, `of`, `at`, `from`, `to`, `&`} |

### Characters (and Phemes)

_Note: Only characters (`chr`) are explicitly covered here, but the syntax and semantics of phemes (`pheme`) are identical except for mutability._

Decomposed, characters (`chr`) are of the type `tup[mrk]`. The glyph types are specifically used to store Unicode code points.

Decomposed, phemes (`pheme`) are of the type `list[rune]`.

### Literals with ``` '.' ```

Grapheme literals are written as a single Unicode grapheme enclosed in backticks `` `.` ``. However, only a single Unicode grapheme can be stored in a grapheme.

If a grapheme is also a single Unicode code point, it can be stored in a grapheme.

```
chr a is 'a';
chr accentMark is '´';
chr aAccent is 'á';
```

### A Warning on `&` with Graphemes

The `&` operator is defined for graphemes. However, this does not guarantee that the resulting grapheme will be a valid Unicode grapheme. If it is not, the compiler will throw an error.

## Textuals

Textuals are container types that can be used to store a sequence of Unicode code points. They belong to the following operational hierarchy:

| Generic Type | Immutable | Mutable | Operator Set                              |
|--------------|-----------|---------|-------------------------------------------|
| `eval`       |           |         | {`=`}                                     |
| `comp`       |           |         | {`=`, `<`}                                |
| `sct`        |           |         | {`=`, `of`}                               |
| `itr`        |           |         | {`=`, `of`, `at`, `from`, `to`, `&`}      |
| `gly`        |           |         | {`=`, `<`, `of`, `at`, `from`, `to`, `&`} |
| `gph`        |           |         | {`=`, `<`, `of`, `at`, `from`, `to`, `&`} |
| `txt`        | `str`     | `text`  | {`=`, `<`, `of`, `at`, `from`, `to`, `&`} |

### Strings (and Texts)

Decomposed, strings (`str`) are of the type `tup[chr]`. The character types are specifically used to store Unicode graphemes.

Decomposed, texts (`text`) are of the type `list[pheme]`.

### Literals with ``` "..." ```

Textual literals are written as a sequence of Unicode graphemes enclosed in double quotes `"...".`

```
str helloWorld is "Hello, world!";
```

### Working with Textuals

The full decomposition of a string (`str`) type is `tup[tup[tup[tup[byte]]]]`. In other words, a string is a tuple of characters (`tup[chr]`), a character is a tuple of marks (`tup[mrk]`), and a mark is a tuple of bytes (`tup[byte]`). This complicates textuals on a semantic level, but it's a necessary complexity to handle the full range of Unicode characters and to provide a complete inventory of available manipulations, including both the more folk-understood notion of "characters" (graphemes) and the more technical notion of Unicode code points (glyphs).

Further, since Lej is motivated first by intuitionistic logic, which itself is in the tradition of constructive mathematics, the complexity of textuals is a necessary to build strings (and texts) from the ground up. This is in contrast to other languages that treat strings as a fundamental type, or that gloss over the complexity of Unicode characters.

In contrast, Lej is also built to uphold Gricean maxims, so all of the added "syntactic sugar" exists to uphold the principle of quantity. The optional complexity is there if a coder needs it, but it's not absolutely necessary to perform basic textual manipulations.

## Lookups

Lookups are container types that store sequences of key-value pairs housing only unique keys. They belong to the following operational hierarchy:

| Generic Type | Immutable | Mutable | Operator Set                                       |
|--------------|-----------|---------|----------------------------------------------------|
| `eval`       |           |         | {`=`}                                              |
| `sct`        |           |         | {`=`, `of`}                                        |
| `itr`        |           |         | {`=`, `of`, `at`, `from`, `to`, `&`}               |
| `lkp`        | `map`     | `dict`  | {`=`, `of`, `at`, `from`, `to`, `&`, `where`, `K`} |

### Maps (and Dictionaries)

_Note: Only maps (`map`) are explicitly covered here, but the syntax and semantics of dictionaries (`dict`) are identical except for mutability._

Maps are assigned in Lej using the syntax `map[TK, TV]`, where `TK` is the key type and `TV` is the value type.

Decomposed, maps (`map`) are of the type `rec[tup[TK], tup[TV]]`, where `TK` and `TV` are the key and value types, respectively. Due to this structure, keys and values are not found via hashing. Instead, the `tup[TK]` is an ordered tuple with only unique elements, and the corresponding `tup[TV]` is the value associated with the key, as noted by their common index. Its named fields are shown in the following code snippet:

```
rec[tup[TK], tup[TV]] map is this: take tup[TK] keys, tup[TV] vals; \
```

Thus, it's better to think of lookups in Lej as parallel arrays, where the key and value are stored in the same index in their respective arrays.

### Literals with `{...}`

Lookup literals are written as a comma-separated sequence of key-value pairs enclosed in curly braces `{...}`. The key-value pairs are separated by spaces.

```
map[nat8, str] numberNames is {1 "one", 2 "two", 3 "three"};
```

### Operators `where` and `K`

The syntax for the `where` operator is `<NAME> where K <KEY>`, where `<NAME>` is the name of the lookup, and `<KEY>` is the key to be found in the lookup. `K` is a keyword that indicates that an index is being searched in the lookup by the contents of the element. If the key is not found, the compiler throws an error. If the key is found, the compiler returns the index of the key in the lookup.

This flexibility allows both key and value lookups, along with the `at` operator.
- A key lookup is `(keys of <NAME>) at (<NAME> where K <KEY>)`.
- A value lookup is `(vals of <NAME>) at (<NAME> where K <KEY>)`.

```
from io:
    take fun putText;
\

fun live is this:
    want int8;
    know map[nat8, str] numberNames;

    numberNames is {1 "one", 2 "two", 3 "three"};

    _ is putText with "The value of 2 is " as ptxt;
    _ is putText with ((vals of numberNames) at (numberNames where K 2)) as ptxt;

    give 0;
\
```

Updating values is only available to dictionaries (`dict`), and it obeys a similar syntax to the `where` operator. The syntax for the `K` operator is `(<NAME> at K <KEY>) is <VALUE>;`, where `<NAME>` is the name of the dictionary, `<KEY>` is the key to be updated, and `<VALUE>` is the new value to be assigned to the key. If the key is not found, it is inserted into `keys` and `vals` at the . If the key is found, the compiler updates the value of the key in the dictionary.

```
from io:
    take fun putText;
\

fun live is this:
    want int8;
    know dict[nat8, str] numberNames;

    numberNames is {1 "one", 2 "two", 3 "three"};

    _ is putText with "The value of 2 is " as ptxt;
    _ is putText with ((vals of numberNames) at (numberNames where K 2)) as ptxt;

    (numberNames at K 2) is "dos"; \

    _ is putText with "The value of 2 is " as ptxt;
    _ is putText with ((vals of numberNames) at (numberNames where K 2)) as ptxt;

    give 0;
\
```

### Operator `&`

The `&` operator is used to concatenate two lookups. The two lookups must have the same key and value types. If there are duplicate keys, the resulting lookup will prioritize the key-value pairs from the right lookup.

```
from io:
    take fun putText, fun formatItr;
\

fun live is this:
    want int8;
    know map[nat8, str] numberNames, map[nat8, str] moreNumberNames;

    numberNames is {1 "one", 2 "two", 3 "three", 4 "fore"};
    moreNumberNames is {4 "four", 5 "five", 6 "six"};

    numberNames is (numberNames & moreNumberNames);

    _ is putText with "The lookup is " as ptxt;
    _ is putText with ((formatItr with numberNames as i) & "\n") as ptxt;

    give 0;
\
```

### Differences from Conventional Lookups

Most programming languages implement lookups in the form of hash maps, where the key is hashed to find the value. Lej does not build in this functionality for the following reasons:

- Hashing limits the kinds of types that can be used as keys. In Lej, any type can be used as a key.
- Hashing always carries a risk of collision. Since Lej demands a level of provability and determinism that does not allow for indeterminacy, ruling out hashing as an option.
- The type system of Lej is operationally structured, and every subtype is an operational superset of its parent type. Hashing would introduce operators outside of the operational hierarchy, which would be a violation of the language's design principles.


This comes with one major tradeoff:

- Key searching is _O(n log n)_ in Lej, since `where` conducts a binary search. This is slower than the _O(1)_ time complexity of hash maps.

And it also comes with some benefits:

- The `where` operator is more flexible than a hash map, since it can search for any element in the lookup, not just the key.
- The risk of collisions is eliminated.
- The `from` and `to` operators can be used to slice lookups, which is not a feature of hash maps.
- Since keys and variables are stored as iterables, they allow much more flexibility with their use. They can be passed as function parameters, for instance, without needing to be harvested from the lookup.

---

#### [Back to the Table of Contents](README.md)