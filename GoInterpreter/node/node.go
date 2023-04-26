package node

///////////////////////////////////////////////////////////////////////////////
// Nodes (Terminals and Nonterminals)
///////////////////////////////////////////////////////////////////////////////

type Node struct {
	Name     string // The name of the Node.
	Start    int    // Where the Node begins coverage in the Lej program.
	End      int    // Where the Node ends coverage in the Lej program.
	Terminal bool   // Whether the scope is a terminal or nonterminal node.
	Lit      string // For terminals only.
	// For nonterminals only:
	Scope string // The scope to which it belongs.
	Left  *Node  // The left child of the Node.
	Right *Node  // The right child of the Node.
}

func Term(name string, end int, lit string) Node {
	var term Node = Node{}
	term.Name = name
	term.Start = end - len(lit)
	term.End = end
	term.Terminal = true
	term.Lit = lit
	return term
}

func NonTerm(name string, scope string, left *Node, right *Node) Node {
	var nonterm Node = Node{}
	nonterm.Name = name
	nonterm.Terminal = false
	nonterm.Scope = scope
	nonterm.Left = left
	nonterm.Right = right
	// Remaining pieces of data can be inferred from the child nodes.
	nonterm.Start = nonterm.Left.Start
	nonterm.End = nonterm.Right.End
	// Force the scope of children to the same scope.
	return nonterm
}
