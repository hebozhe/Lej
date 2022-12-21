package node

///////////////////////////////////////////////////////////////////////////////
// Nodes (Terminals and Nonterminals)
///////////////////////////////////////////////////////////////////////////////

type Node struct {
	Name     string // The name of the Node.
	Start    int    // Where the Node begins coverage in the Lej program.
	End      int    // Where the Node ends coverage in the Lej program.
	Scope    string // The scope to which it belongs.
	Action   string // The action that the Node performs at evaluation.
	Terminal bool   // Whether the scope is a terminal or nonterminal node.
	Literal  string // For terminals,
	Children [2]int // The positions of Left and Right, relative to its span.
	Left     *Node  // The left child of the Node.
	Right    *Node  // The right child of the Node.
}

// Builds a new terminal Node.
func BuildNewTerm(name string, start int, end int, scope string, action string, literal string) *Node {
	return &Node{
		Name:     name,
		Start:    start,
		End:      end,
		Scope:    scope,
		Action:   action,
		Terminal: true,
		Literal:  literal,
	}
}

// Builds a new nonterminal Node.
func BuildNewNonterm(name string, start int, end int, scope string, action string, children [2]int, matchSpan []*Node) *Node {
	var Left *Node
	var Right *Node
	// Leave Left and Right undefined until a sufficiently long matchSpan is presented.
	if len(matchSpan) < children[1]+1 {
		Left = &Node{}
		Right = &Node{}
	} else {
		if children[0] == children[1] {
			Left = matchSpan[children[0]]
			Right = &Node{}
		} else {
			Left = matchSpan[children[0]]
			Right = matchSpan[children[1]]
		}
	}
	return &Node{
		Name:     name,
		Start:    start,
		End:      end,
		Scope:    scope,
		Action:   action,
		Terminal: false,
		Children: children,
		Left:     Left,
		Right:    Right,
	}
}
