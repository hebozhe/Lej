## Type Signatures

Lej requires type signatures for every defined element in a program.

Type inference is not supported in Lej, and this is mainly due to a demand that Lej adhere to the Gricean principle of _quantity_, which states that a speaker should provide as much information as is needed for the listener to understand the speaker's intended meaning. Type inference forces coders to mentally infer types, which can lead to misunderstandings and bugs.

Type signatures for primitive types are written as the type names, alone. For example, the type signature for a generic natural-number-operator-compatible type is `N`, and for a specific natural number is one of `nat8`, `nat16`, `nat32`, or `nat64`.

Type signatures for container types are written as the type name followed by the type signatures of the container's contents. For example, the type signature for a record type is `rec[T1, T2, ...]`, where `T1`, `T2`, etc., are the types of the record's fields.

---

#### [Back to the Table of Contents](README.md)