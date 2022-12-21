package parser

import (
	. "GoInterpreter/node"
	"fmt"
	"os"
)

///////////////////////////////////////////////////////////////////////////////
// Mapping Terminal Nodes
///////////////////////////////////////////////////////////////////////////////

var TerminalsMap map[string]*Node = map[string]*Node{
	// Assignment keywords:
	"def": BuildNewTerm("DEF", 0, 0, "g", "", "def"),
	"as":  BuildNewTerm("AS", 0, 0, "g", "", "as"),
	// Identifiers are found separately.
	// Logical literals:
	"T": BuildNewTerm("VAL-SUBEXPR", 0, 0, "g", "buildTrue", "T"),
	"U": BuildNewTerm("VAL-SUBEXPR", 0, 0, "g", "buildUnsure", "U"),
	"F": BuildNewTerm("VAL-SUBEXPR", 0, 0, "g", "buildFalse", "F"),
	// Logical operators:
	"and": BuildNewTerm("AND", 0, 0, "g", "", "and"),
	"or":  BuildNewTerm("OR", 0, 0, "g", "", "or"),
	"not": BuildNewTerm("NOT", 0, 0, "g", "", "not"),
	// Delimiters:
	";": BuildNewTerm(";", 0, 0, "g", "", ";"),
	"(": BuildNewTerm("(", 0, 0, "g", "", "("),
	")": BuildNewTerm(")", 0, 0, "g", "", ")"),
	// Type keywords:
	"val": BuildNewTerm("VAL", 0, 0, "g", "", "val"),
}

// Creates a new terminal ID Node.
func BuildNewIDNode(start int, end int, scope string, literal string) *Node {
	return BuildNewTerm("ID", start, end, scope, "", literal)
}

// Determines whether a given string qualifies as an ID literal.
func canBeNewID(s string) bool {
	if _, ok := TerminalsMap[s]; ok {
		return false
	}
	if !('a' <= s[0] && s[0] <= 'z') {
		return false
	}
	for _, c := range s {
		if !(('a' <= c && c <= 'z') ||
			('A' <= c && c <= 'Z') ||
			('0' <= c && c <= '9')) {
			return false
		}
	}
	return true
}

///////////////////////////////////////////////////////////////////////////////
// Tokenizer
///////////////////////////////////////////////////////////////////////////////

func Tokenize(thisPath string) []*Node {
	var tokenArr []*Node
	lejFile, err := os.ReadFile(thisPath)
	if err != nil {
		panic(err)
	}
	var lejText string = string(lejFile) + " "
	// fmt.Printf(lejText + "\n")
	// var whitespaces [2]byte = [2]byte{' ', '\n'}
	var i int = 0
	var curScope string = "g"
	for j := 1; j < len(lejText); j++ {
		// Skip slice-leading whitespace characters.

		for lejText[i] == ' ' || lejText[i] == '\n' {
			i += 1
			if i == j {
				break
			}
		}
		// Append identifiers in current chunk.
		var curChunk string = lejText[i:j]
		var nextChunk string = lejText[i : j+1]
		// fmt.Printf("'%s' '%s'\n", curChunk, nextChunk)
		// Skip empty chunks.
		if curChunk == "" {
			continue
		}
		// Check for new terminal ID nodes.
		if canBeNewID(curChunk) {
			// Skip if the next chunk can be an identifier, too.
			if canBeNewID(nextChunk) {
				continue
			}
			// Skip if the next chunk can be a primitive.
			if _, ok := TerminalsMap[nextChunk]; ok {
				continue
			}
			var idNode *Node = BuildNewIDNode(i, j, curScope, curChunk)
			tokenArr = append(tokenArr, idNode)
			// fmt.Printf("Added identifier: %s\n", idNode.Literal)
			i = j
			continue
		}
		// Append primitive terminal Nodes.
		if tn, ok := TerminalsMap[curChunk]; ok {
			// Skip if the next chunk can be an identifier.
			if canBeNewID(nextChunk) {
				continue
			}
			var nextTNode *Node = BuildNewTerm(tn.Name, i, j, curScope, tn.Action, curChunk)
			tokenArr = append(tokenArr, nextTNode)
			// fmt.Printf("Added primitive: %s\n", foundTNode.Name)
			i = j
			continue
		}
		// Panic, because the character is foreign.
		fmt.Printf("This chunk could not be tokenized: %s\n", curChunk)
		os.Exit(1)
	}
	return tokenArr
}
