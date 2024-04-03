# Generic Types

Generic types in Lej are defined by the operators they permit, which are sorted into larger operator sets. They are as follows:

| Generic Type | Signature | Operator Set                               |
|--------------|-----------|--------------------------------------------|
| Functions    | `fun`     | N/A                                        |
| Evaluables   | `eval`    | {`=`}                                      |
| Brouwerians  | `brou`    | `eval` ∪ {`and`, `or`, `not`}              |
| Comparables  | `comp`    | `eval` ∪ {`<`}                             |
| Structures   | `sct`     | `eval` ∪ {`of`}                            |
| Naturals     | `N`       | `comp` ∪ {`+`, `*`, `%`}                   |
| Integers     | `Z`       | `N` ∪ {`-`}                                |
| Rationals    | `Q`       | `Z` ∪ `sct` ∪ {`/`}                        |
| Iterables    | `itr`     | `comp` ∪ `sct` ∪ {`at`, `from`, `to`, `&`} |
| Glyphs       | `gly`     | `itr`                                      |
| Graphemes    | `gph`     | `itr`                                      |
| Textuals     | `txt`     | `itr`                                      |
| Lookups      | `lkp`     | `itr` ∪ {`where`, `K`}                     |

Allowed operations between any two types are simply the intersection of their operator sets. For some examples, the operator set for `N` and `Z` is that of `N`, but the operator set for `itr` and `Q` is that of `comp`.

Generics can only be used in `take` and `want` statements of functions. This is because generic types do not speak to the mutability, sizes, or other properties that their member subtypes do.

---

#### [Back to the Table of Contents](README.md)