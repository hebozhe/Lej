// This package contains the grammar for the Lej parser.
package parser

type Regla struct {
	Padre     NodeType
	Hijos     []NodeType
	Guardados []uint8
}

// The gramatica for the Lej parser follows BNF-like syntax.
var gramatica = []Regla{}
