package main

import (
	. "GoInterpreter/evaluator"
	. "GoInterpreter/lexer"
	. "GoInterpreter/node"
	. "GoInterpreter/parser"
	"fmt"
)

func main() {
	var lejToks []*Node = Tokenize("../Examples/valAssignments.lej")
	fmt.Printf("%v\n", lejToks)
	var lejTree *Node = Parse(lejToks)
	/* if lejJSONBytes, err := json.MarshalIndent(lejTree, "", "\t"); err == nil {
		fmt.Println(string(lejJSONBytes))
	} */
	WalkTree(lejTree)
}
