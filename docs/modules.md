# Modules

Modules are the primary way to organize code in Lej. They are used to group related code together and to control the visibility of code.

## Module Imports

Modules can be imported into other modules at the top of the file. This is done with a `from <MODULE>: take <TYPE> <NAME>, ...; \` block, where `<MODULE>` is the name of the module, `<TYPE>` is the type of the thing to be imported, `<NAME>` is the name of thing to be imported from the module.

```
from math:
    take fun sum;
\
```

If a type alias is present in the module, it can be used for the `<TYPE>` field in the import.

```
from someModule:
    take typeAliasFromThatModule thatThing;
\
```

## Module Exports

The public-private distinction does not exist in Lej. All globals in a module are public.

If a module is not found in any of the search locations, the compiler will throw an error.

## Module Search Priority

Module search priority is as follows:
1. The standard library,
2. The program's directory,
3. The program's subdirectories,
4. The program's superdirectories, and
5. The first-matching subdirectory of the program's workspace.

## Module Naming

Modules are named with the `.lej` extension. The name of the module is the name of the file without the extension.

---

#### [Back to the Table of Contents](README.md)