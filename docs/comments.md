# Comments

Comments in Lej are enclosed in `~` characters. They can be used to document code, explain logic, or temporarily disable code.

Because comments are ignored by the parser, they can be placed anywhere in the code. They're also multi-line, so you can write as much as you want between the `~` characters.

A tilde character preceded by a backslash (`\~`) will be treated as a literal tilde character, not the start or end of a comment.

```
~ This is a single-line comment. ~

~ This is a multi-line comment.
It can span multiple lines. ~

~ The comment \~s below temporarily disable the code.~
~
nat64 x is 5;
~

~ Comments can also exist inline, though this is generally discouraged.~
nat64 y ~the variable on the y axis~ is 10;
```

Except for documentation purposes, comments should be used sparingly. If you find yourself needing lots of comments, consider refactoring your code to make it more readable.

---

#### [Back to the Table of Contents](README.md)