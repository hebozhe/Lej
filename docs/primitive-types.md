# Primitive Types

Primitive types are those types which do not require any container to be well-defined. They are the building blocks of all other types in Lej.

## Brouwerians

Brouwerians name both the generic type and the only subtype of Brouwerians. They belong to the following operational hierarchy:

| Generic Type | Immutable | Mutable | Operator Set              |
|--------------|-----------|---------|---------------------------|
| `eval`       |           |         | {`=`}                     |
| `brou`       | `brou`    |         | {`=`, `and`, `or`, `not`} |

### Brouwerian Primitives

The Brouwerian primitives are `true`, `false`, and `unsure`. They evaluate according to the following tables:

| `and`    | `true`   | `false` | `unsure` |
|----------|----------|---------|----------|
| `true`   | `true`   | `false` | `unsure` |
| `false`  | `false`  | `false` | `false`  |
| `unsure` | `unsure` | `false` | `unsure` |

| `or`     | `true` | `false`  | `unsure` |
|----------|--------|----------|----------|
| `true`   | `true` | `true`   | `true`   |
| `false`  | `true` | `false`  | `unsure` |
| `unsure` | `true` | `unsure` | `unsure` |

| `not` | `true`  | `false` | `unsure` |
|-------|---------|---------|----------|
|       | `false` | `true`  | `unsure` |

These tables correspond directly to the Kleene logic K3, which is a three-valued logic system. The `unsure` value is used to represent the absence of a truth value, which is useful in cases where a value is not yet known or cannot be determined.

### Gilvenko's Theorem and `unsure`

To give Lej a fully intuitionistic evaluation system, a lemma from Gilvenko's theorem is used to force all classical contradictions from `unsure` to `false`. Then, by negation, Gilvenko's theorem holds for all intuitionistic tautologies in this operator set.

This works by giving each evaluation a classical "tail" representing a distinct column in a classical truth-table when presented with a new proposition (which is illustrated this [`V`: `CT`], where `V` is the Brouwerian value and `CT` is the classical tail).

Thus, the strong and weak laws of excluded middle are `unsure` when the constituent primitive is `unsure`, but their double-negations evaluate to `true`

```
~
For the purposes of illustration:
    In the K3/intuitionistic head, 0 is false, 1 is unsure, and 2 is true.
    In the classical tail, 0 is false and 1 is true.
    So, Lej-true is [2: 1], Lej-false is [0: 0], and Lej-unsure is [1: ...].
~

~The (strong) law of excluded middle.~
brou slem is unsure or (not unsure);
~
- [1: 10] or (not [1: 10])
- [1: 10] or [1: 01]
- [1: 11]
- [1: 1]
~

brou dnlem is not not slem;
~
- not not [1: 1]
- not [1: 0]
- not [0: 0] from Gilvenko's lemma
- [2: 1]
~

~The weak law of excluded middle.~
brou wlem is (not unsure) or (not not unsure);
~
- (not [1: 10]) or (not not [1: 10])
- [1: 01] or (not [1: 01])
- [1: 01] or [0: 10]
- [1: 11]
- [1: 1]
~

brou dnwlem is not not wlem;
~
- not not [1: 1]
- not [1: 0]
- not [0: 0] from Gilvenko's lemma
- [2: 1]
~
```

Note that tail values are saved in the `brou` type after evaluation, but are not accessible to the programmer and are automatically shortened when the first and second halves of a Brouwerian are the same.

This also means that Brouwerian `unsure` tails grow at a rate of 2<sup>n</sup>, where n is the number of `unsure` values in the expression. So, another scheme is used to keep the tails short and manageable.

## Natural Numbers

Natural numbers name all numbers from 0 to 2<sup>64</sup>-1, what other programming languages call "unsigned integers". They belong to the following operational hierarchy:

| Generic Type | Immutable                           | Mutable | Operator Set              |
|--------------|-------------------------------------|---------|---------------------------|
| `eval`       |                                     |         | {`=`}                     |
| `comp`       |                                     |         | {`=`, `<`}                |
| `N`          | {`nat8`, `nat16`, `nat32`, `nat64`} |         | {`=`, `<`, `+`, `*`, `%`} |


### `nat8`, `nat16`, `nat32`, `nat64`

These are the four subtypes of `N`. They are used to represent natural numbers of 8, 16, 32, and 64 bits, respectively.

Because overflows are underflows are treated as erors in Lej, the maximum value of each subtype is 2<sup>8n</sup>-1, where n is the number of bits in the subtype.

This also means that, unlike other languages, subtraction `-` is not a valid operator for `natX` types, because `0 - 1`, for example, would make every `natX` type an `intX` type.

```
fun isPrime is this:
    take nat64 n;
    want brou;
    know nat64 i;

    if n < 2: give false; \

    i is 2;
    for some time, do this:
        if n < (i * i): out! \
        if n % i = 0: give false; \
        i is i + 1;
    \

    give true;
\
```

## Bytes

Bytes name all numbers from 0 to 255 and are an alias for `nat8` with some caveats for explicit use in textual creation and manipulation. They belong to the following operational hierarchy:

| Generic Type | Immutable | Mutable | Operator Set              |
|--------------|-----------|---------|---------------------------|
| `eval`       |           |         | {`=`}                     |
| `comp`       |           |         | {`=`, `<`}                |
| `N`          | `byte`    |         | {`=`, `<`, `+`, `*`, `%`} |

### Text and `byte`

`byte` is used to represent a single byte of data. The parser and the compiler will expect `byte` to be used in textual contexts, or when collecting data from a network.

It is because of this feature that text-based types include all of the `comp` operators, making Unicode code points comparable.

```
fun isAscii is this:
    take byte b;
    want brou;

    if b < 128: give true; \
    give false; \
\

fun howManyBitsInPost is this:
    take itr[byte] bs;
    want nat64;

    give (len of bs) * 8;
\
```

## Integers

Integers name all numbers from -2<sup>64</sup> to 2<sup>64</sup>-1. They belong to the following operational hierarchy:

| Generic Type | Immutable                           | Mutable | Operator Set                   |
|--------------|-------------------------------------|---------|--------------------------------|
| `eval`       |                                     |         | {`=`}                          |
| `comp`       |                                     |         | {`=`, `<`}                     |
| `N`          |                                     |         | {`=`, `<`, `+`, `*`, `%`}      |
| `Z`          | {`int8`, `int16`, `int32`, `int64`} |         | {`=`, `<`, `+`, `*`, `%`, `-`} |

### `int8`, `int16`, `int32`, `int64`

These are the four subtypes of `Z`. They are used to represent integers of 8, 16, 32, and 64 bits, respectively.

Because overflows are underflows are treated as erors in Lej, the minimum value of each subtype is -2<sup>8n</sup> and the maximum value is 2<sup>8n</sup>-1, where n is the number of bits in the subtype.

```
fun abs is this:
    take N n;
    want int64;

    if n < 0: give n * -1; \
    give n;
\
```

---

#### [Back to the Table of Contents](README.md)

