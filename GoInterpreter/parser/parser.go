package parser

import (
	. "GoInterpreter/node"
	"fmt"
	"os"
)

///////////////////////////////////////////////////////////////////////////////
// Mapping Nonterminal Nodes
///////////////////////////////////////////////////////////////////////////////

var NonTerminalsMap map[string]*Node = map[string]*Node{
	// Completed lines:
	"CODE-BLOCK CODE-BLOCK": BuildNewNonterm("CODE-BLOCK", 0, 0, "g", "BOTH", [2]int{0, 1}, []*Node{}),
	"ASGN-STMT":             BuildNewNonterm("CODE-BLOCK", 0, 0, "g", "LEFT", [2]int{0, 0}, []*Node{}),
	// VAL (logical value) assignments and operations:
	"DEF VAL-VAR AS VAL-EXPR ;":       BuildNewNonterm("ASGN-STMT", 0, 0, "g", "assignVal", [2]int{1, 3}, []*Node{}),
	"VAL ID":                          BuildNewNonterm("VAL-VAR", 0, 0, "g", "idAssert", [2]int{1, 1}, []*Node{}),
	"NOT VAL-SUBEXPR":                 BuildNewNonterm("VAL-SUBEXPR", 0, 0, "g", "buildNot", [2]int{1, 1}, []*Node{}),
	"NOT VAL-VAR":                     BuildNewNonterm("VAL-SUBEXPR", 0, 0, "g", "buildNot", [2]int{1, 1}, []*Node{}),
	"( VAL-SUBEXPR OR VAL-SUBEXPR )":  BuildNewNonterm("VAL-SUBEXPR", 0, 0, "g", "buildOr", [2]int{1, 3}, []*Node{}),
	"( VAL-VAR OR VAL-SUBEXPR )":      BuildNewNonterm("VAL-SUBEXPR", 0, 0, "g", "buildOr", [2]int{1, 3}, []*Node{}),
	"( VAL-SUBEXPR OR VAL-VAR )":      BuildNewNonterm("VAL-SUBEXPR", 0, 0, "g", "buildOr", [2]int{1, 3}, []*Node{}),
	"( VAL-VAR OR VAL-VAR )":          BuildNewNonterm("VAL-SUBEXPR", 0, 0, "g", "buildOr", [2]int{1, 3}, []*Node{}),
	"( VAL-SUBEXPR AND VAL-SUBEXPR )": BuildNewNonterm("VAL-SUBEXPR", 0, 0, "g", "buildAnd", [2]int{1, 3}, []*Node{}),
	"( VAL-VAR AND VAL-SUBEXPR )":     BuildNewNonterm("VAL-SUBEXPR", 0, 0, "g", "buildAnd", [2]int{1, 3}, []*Node{}),
	"( VAL-SUBEXPR AND VAL-VAR )":     BuildNewNonterm("VAL-SUBEXPR", 0, 0, "g", "buildAnd", [2]int{1, 3}, []*Node{}),
	"( VAL-VAR AND VAL-VAR )":         BuildNewNonterm("VAL-SUBEXPR", 0, 0, "g", "buildAnd", [2]int{1, 3}, []*Node{}),
	"( VAL-VAR )":                     BuildNewNonterm("VAL-SUBEXPR", 0, 0, "g", "LEFT", [2]int{1, 1}, []*Node{}),
	"( VAL-SUBEXPR )":                 BuildNewNonterm("VAL-SUBEXPR", 0, 0, "g", "LEFT", [2]int{1, 1}, []*Node{}),
	"VAL-SUBEXPR OR VAL-SUBEXPR":      BuildNewNonterm("VAL-EXPR", 0, 0, "g", "buildOr", [2]int{0, 2}, []*Node{}),
	"VAL-VAR OR VAL-SUBEXPR":          BuildNewNonterm("VAL-EXPR", 0, 0, "g", "buildOr", [2]int{0, 2}, []*Node{}),
	"VAL-SUBEXPR OR VAL-VAR":          BuildNewNonterm("VAL-EXPR", 0, 0, "g", "buildOr", [2]int{0, 2}, []*Node{}),
	"VAL-VAR OR VAL-VAR":              BuildNewNonterm("VAL-EXPR", 0, 0, "g", "buildOr", [2]int{0, 2}, []*Node{}),
	"VAL-SUBEXPR AND VAL-SUBEXPR":     BuildNewNonterm("VAL-EXPR", 0, 0, "g", "buildAnd", [2]int{0, 2}, []*Node{}),
	"VAL-VAR AND VAL-SUBEXPR":         BuildNewNonterm("VAL-EXPR", 0, 0, "g", "buildAnd", [2]int{0, 2}, []*Node{}),
	"VAL-SUBEXPR AND VAL-VAR":         BuildNewNonterm("VAL-EXPR", 0, 0, "g", "buildAnd", [2]int{0, 2}, []*Node{}),
	"VAL-VAR AND VAL-VAR":             BuildNewNonterm("VAL-EXPR", 0, 0, "g", "buildAnd", [2]int{0, 2}, []*Node{}),
	"VAL-SUBEXPR":                     BuildNewNonterm("VAL-EXPR", 0, 0, "g", "LEFT", [2]int{0, 0}, []*Node{}),
}

///////////////////////////////////////////////////////////////////////////////
// Recursive, Iterative Parser
///////////////////////////////////////////////////////////////////////////////

func extractNodeNames(fromNodes []*Node) string {
	var nodeNames string = ""
	for n := range fromNodes {
		nodeNames += fromNodes[n].Name + " "
	}
	//fmt.Printf("'%s'\n", nodeNames[:len(nodeNames)-1])
	return nodeNames[:len(nodeNames)-1]
}

func idAssert(intoTokens []*Node, withID *Node) []*Node {
	fmt.Printf("idAssert TRIGGERED FOR %s!\n", withID.Left.Literal)
	var updatedTokens []*Node
	for _, node := range intoTokens {
		if node.Name == "ID" && node.Literal == withID.Left.Literal {
			var name string = withID.Name
			var start int = node.Start
			var end int = node.End
			var scope string = node.Scope
			var xidNode *Node = BuildNewNonterm(name, start, end, scope, "LEFT", [2]int{0, 0}, []*Node{node})
			updatedTokens = append(updatedTokens, xidNode)
		} else {
			updatedTokens = append(updatedTokens, node)
		}
	}
	fmt.Println("*" + extractNodeNames(intoTokens))
	return updatedTokens
}

func Parse(lejTokens []*Node) *Node {
	for j := 5; j > 0; j-- {
		var i int = 0
		for i < (len(lejTokens)-j)+1 {
			var tokSlice []*Node = lejTokens[i : i+j]
			var tokNames string = extractNodeNames(tokSlice)
			var newNode *Node
			if nonterm, ok := NonTerminalsMap[tokNames]; ok {
				if nonterm.Children[0] == nonterm.Children[1] { // This production rule only one Left Node.
					newNode = BuildNewNonterm(nonterm.Name, 0, 0, "?", nonterm.Action, nonterm.Children, tokSlice)
					fmt.Printf("%v\n", newNode)
					var s int = newNode.Left.Start
					var e int = newNode.Left.End
					var scope string = newNode.Left.Scope
					newNode = BuildNewNonterm(newNode.Name, s, e, scope, newNode.Action, newNode.Children, tokSlice)
					fmt.Printf("%v\n", newNode)
					fmt.Printf("L: %s -> %s :: %s\n", newNode.Name, newNode.Left.Name, tokNames)
				} else { // This production rule has a Left Node and a Right Node.
					newNode = BuildNewNonterm(nonterm.Name, 0, 0, "?", nonterm.Action, nonterm.Children, tokSlice)
					fmt.Printf("%v\n", newNode)
					var s int = newNode.Left.Start
					var e int = newNode.Right.End
					var scope string = newNode.Left.Scope
					newNode = BuildNewNonterm(newNode.Name, s, e, scope, newNode.Action, newNode.Children, tokSlice)
					fmt.Printf("%v\n", newNode)
					fmt.Printf("LR: %s -> %s %s :: %s\n", newNode.Name, newNode.Left.Name, newNode.Right.Name, tokNames)
				}
				lejTokens[i] = newNode
				// idAssert actions occur mid-parse.
				if newNode.Action == "idAssert" {
					lejTokens = idAssert(lejTokens, newNode)
				}
				copy(lejTokens[i+1:], lejTokens[i+j:])
				lejTokens = lejTokens[:(len(lejTokens)-j)+1]
				fmt.Printf("**%s\n\n", extractNodeNames(lejTokens))
				return Parse(lejTokens)
			} else {
				i += 1
			}
		}
	}
	if len(lejTokens) > 1 {
		// Panic, because the parser couldn't complete the parse.
		fmt.Printf("This collection of tokens cannot be parsed.\n")
		os.Exit(1)
	}
	return lejTokens[0]
}

func PrintParse(fromToks []*Node) *Node {
	var lejTree *Node = Parse(fromToks)
	fmt.Printf("%v\n", lejTree)
	return lejTree
}
