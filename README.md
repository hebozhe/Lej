# **Lej**: A Semantically Intuitionistic, Syntactically Intuitive Language

# **Overview**
Lej (pronounced as "ledge") is a statically typed, compiled programming language that aims to provide a simple and intuitive syntax while allowing access to both classical and intuitionistic semantics. It is being developed under these maxims, in loose order of priority:

- **Access to both classical and intuitionistic worlds.** Brouwerian types work normally if you have only `true` and `false` values. `unsure` values behave reliably intuitionistically for the available logical operators.
- **Simple and intuitive syntax.** The syntax is designed to be easy to read and write for beginners and seasoned programmers alike. A single symbol does a single thing, for a single type.
- **Mandated functional purity.** Every function **_must_** return a value, no exceptions.
- **No undefined or null types.** Lej does not have a type for `None`, `nil`, `null`, `nix`, or any other empty value. `undefined` is an error, not a type.
- **Guaranteed precision.** There is no `float` type in Lej. Types are closed under their permitted operations, so there is no loss of precision in arithmetic operations.

If you want to know more about what the hell I'm up to, [I wrote docs](docs/README.md).