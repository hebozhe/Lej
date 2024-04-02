# Type Aliases

Lej allows you to define type aliases with the `type` keyword. Type aliases are useful for creating shorter names for complex types.

Type aliases are replaced with their underlying type expression during the parsing phase. This means that type aliases are not stored in the AST and do not affect the semantics of the program.

Lej uses `see <ALIAS> as <TYPE>;` to define a type alias, where `<ALIAS>` is the alias name and `<TYPE>` is the type expression.

```
see human as rec[str, nat16, brou];

human person is this:
    take str name, nat16 age, brou isAlive;
\
```

In the example above, `human` is a type alias for the record type `rec[str, nat16, brou]`. The `person` type is defined as a record with fields `name`, `age`, and `isAlive`.

---

#### [Back to the Table of Contents](README.md)