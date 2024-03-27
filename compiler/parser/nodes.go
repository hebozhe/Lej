package parser

import "GoCompiler/lexer"

// NodeType is the type of a node in the AST, which cross-aliases the lexer's TokType.
type NodeType lexer.TokType

// Constants representing the different types of nodes in the AST.
// All nodes here being nonterminal symbols will be represented in PascalCase.
const ()

// Nodo represents a node in the AST.
type Nodo struct {
	Tipo    NodeType    // The type of the node.
	Lit     string      // The literal value of the node.
	Niv     uint        // The level of the node in the AST.
	Bitspan [2]uint     // The span of the node in bytes.
	Linspan [2]uint     // The span of the node in lines.
	Hijos   []*NodeType // The children of the node.
}

// nuNodoBase creates a new base node from a token.
func nuNodoBase(tok lexer.Tok) Nodo {
	return Nodo{
		Tipo:    NodeType(tok.Tipo),
		Lit:     tok.Lit,
		Niv:     0,
		Bitspan: [2]uint{tok.Ini, tok.Fin},
		Linspan: [2]uint{tok.Lin, tok.Lin},
		Hijos:   []*NodeType{},
	}
}

// empujaNodoBase pushes a new base node onto the stack of nodes.
func empujaNodoBase(t lexer.Tokenizador, ns []Nodo) []Nodo {
	return append(ns, nuNodoBase(lexer.BuscaProximoToken(t).Tok))
}
