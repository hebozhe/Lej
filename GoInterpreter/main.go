package main

import (
	. "GoInterpreter/lexer"
	. "GoInterpreter/node"
	"fmt"
	"os"
)

func main() {
	lejProg, err := os.ReadFile("../Examples/brouAssignments.lej")
	if err != nil {
		fmt.Printf("The file could not be read.\n")
	}
	var lejToks []Node = Lex(string(lejProg))
	fmt.Printf("%v\n", lejToks)
}
