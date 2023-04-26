package lexer

import (
	. "GoInterpreter/errors"
	. "GoInterpreter/node"
)

func primValue(r rune) uint8 {
	switch r {
	// 0 means endchar, so check whether a token is an ID or keyword.
	// 1 means primitive symbol, so check a token whether ID of keyword and also add the symbol.
	// 2 means encloser, so continue the scan to the next identical encloser, and assign the str/text literal.
	// 3 means comment tick, so continue the scan to the next identical encloser, and do nothing with it.
	// 4 means it's not a primitive.
	// Whitespaces:
	case ' ', '\n', '\t':
		return 0
	// Arithmetic operators:
	case '+', '-', '/', '.':
		return 1
	// Arithmetic evaluators:
	case '=', '>', '<':
		return 1
	// Delimiters:
	case '[', ']', '(', ')':
		return 1
	// Line ends:
	case ';', ':', '!':
		return 1
	// Strings:
	case '\'':
		return 2
	// Comments
	case '`':
		return 3
	default:
		return 4
	}
}

var keywords map[string]string = map[string]string{
	// Assignment keywords:
	"def": "def", "as": "as",
	// Reassignment keywords:
	"redef": "redef",

	// Type declarations:
	"chr":  "chr",
	"brou": "brou",
	"nat":  "nat", "nat8": "nat8", "nat16": "nat16", "nat32": "nat32", "nat64": "nat64",
	"int": "int", "int8": "int8", "int16": "int16", "int32": "int32", "int64": "int64",
	"rat": "rat",
	"map": "map", "dict": "dict",
	"tup": "tup", "list": "list",
	"str": "str", "text": "text",
	"rec": "rec", "data": "data",
	"fun": "fun",
	"gen": "gen",

	// Logical primitives:
	"T": "<brouLit>", "U": "<brouLit>", "F": "<brouLit>",

	// Logical operators:
	"and": "and", "or": "or", "not": "not",

	// "this":
	"this": "this",

	// Loop-specific keywords:
	"do": "do", "times": "do", "until": "until",
	"back": "back", "up": "up", "out": "out",

	// Function keywords:
	"take": "take", "expect": "expect", "give": "give",
	"what": "what", "gives": "gives", "with": "with",

	// Module importing:
	"use": "use", "from": "from",
}

// Outside of primitives, the only remaining characters are alphanumeric.
// That means they're keywords, identifiers, or natural=number literals.
func decideTerm(ofstr string, start int, end int) Node {
	var firstChar rune = rune(ofstr[0])
	if 'a' <= firstChar && firstChar <= 'z' { // It's a keyword or identifier
		// Check for keyword status vs. identifier status.
		val, ok := keywords[ofstr]
		if ok { // It's a keyword.
			return Term(val, end, ofstr)
		}
		for _, c := range ofstr { // Make sure the identifier is valid.
			if !(('a' <= c && c <= 'z') || ('A' <= c && c <= 'Z') || ('0' <= c && c <= '9')) {
				ThrowError("Invalid Identifier", ofstr, start, end)
			}
		}
		return Term("<id>", end, ofstr)
	}
	if ofstr == "T" || ofstr == "U" || ofstr == "F" { // It's a Brouwerian literal.
		val, _ := keywords[ofstr]
		return Term(val, end, ofstr)
	}
	if '0' <= firstChar && firstChar <= '9' {
		// Confirm it's an natural-number literal.
		for _, c := range ofstr {
			if !('0' <= c && c <= '9') {
				ThrowError("Invalid Literal", ofstr, start, end)
			}
		}
		return Term("<natLit>", end, ofstr)
	}
	// It's ill-formed.
	ThrowError("Invalid Literal", ofstr, start, end)
	return Node{} // Never gets reached. Only makes Go happy.
}

func Lex(input string) []Node {
	var tok string = ""
	var terms []Node = []Node{}
	var holdoff int = -1
	for i, c := range input {
		if i < holdoff {
			continue
		}
		switch primValue(c) {
		case 4: // Just add c to tok.
			tok += string(c)
		case 3: // Capture the entire comment and discard it.
			tok += string(c)
			for _, sc := range input[i+1:] {
				tok += string(sc)
				if sc == c {
					if tok[len(tok)-2] != '\\' {
						break
					}
				}
			}
			holdoff = i + len(tok)
			tok = ""
		case 2: // Capture the entire str/text literal and create a terminal for it.
			tok += string(c)
			for _, sc := range input[i+1:] {
				tok += string(sc)
				if sc == c {
					if tok[len(tok)-2] != '\\' {
						break
					}
				}
			}
			terms = append(terms, Term("strTextLit", i, tok)) // The str/text literal.
			tok = ""
		case 1: // First, decide which terminal the token is; then, add the terminal.
			if tok != "" {
				terms = append(terms, decideTerm(tok, i-len(tok), i))
			}
			terms = append(terms, Term(string(c), i, string(c)))
			tok = ""
		case 0:
			if tok != "" {
				terms = append(terms, decideTerm(tok, i-len(tok), i))
			}
			tok = ""
		}
	}
	return terms
}
