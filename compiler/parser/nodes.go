package parser

import (
	"GoCompiler/lexer"
)

// NodoTipo is the type of a node in the AST, which cross-aliases the lexer's TokType.
type NodoTipo lexer.TokTipo

// Constants representing the different types of nodes in the AST.
// All nodes here being nonterminal symbols will be represented in PascalCase.
const (
	RatExpr NodoTipo = "RatExpr"
)

// Nodo represents a node in the AST.
type Nodo struct {
	Tipo    NodoTipo // The type of the node.
	Lit     string   // The literal value of the node.
	Niv     uint     // The level of the node in the AST.
	Bitspan [2]uint  // The span of the node in bytes.
	Linspan [2]uint  // The span of the node in lines.
	Indices [2]uint  // The indices of the nodes of the first and last children.
	Hijos   []*Nodo  // The children of the node.
}

// nuNodoBase creates a new base node from a token.
func nuNodoBase(tok lexer.Tok, dex uint) Nodo {
	return Nodo{
		Tipo:    NodoTipo(tok.Tipo),
		Lit:     tok.Lit,
		Niv:     0,
		Bitspan: [2]uint{tok.Ini, tok.Fin},
		Linspan: [2]uint{tok.Lin, tok.Lin},
		Indices: [2]uint{dex, dex},
		Hijos:   []*Nodo{},
	}
}

type Analizador struct {
	Tokenizador lexer.Tokenizador
	Nodos       []Nodo
}

func InicAnalizador(path string) Analizador {
	return Analizador{
		Tokenizador: lexer.InicTokenizador(path),
		Nodos:       []Nodo{},
	}
}

func HazStringDeNodos(ns []Nodo) string {
	if len(ns) == 0 {
		return ""
	}

	return string(ns[0].Tipo) + " " + HazStringDeNodos(ns[1:])
}

// empujaNodoBase pushes a base node onto the node stack.
func empujaNodoBase(a Analizador) Analizador {
	// Know...
	a.Tokenizador = lexer.BuscaProximoToken(a.Tokenizador)
	a.Nodos = append(a.Nodos, nuNodoBase(a.Tokenizador.Tok, uint(len(a.Nodos))))
	return a
}

func EmpujaNodosBases(a Analizador) Analizador {
	// If all of the nodes have been pushed, return the analyzer.
	if a.Tokenizador.Tok.Tipo == lexer.EOF {
		return a
	}

	a = empujaNodoBase(a)
	switch a.Tokenizador.Tok.Tipo {
	// If the token is a semicolon, right parenthesis, right bracket, right brace, backslash, or EOF return the analyzer.
	case lexer.SEMI, lexer.RPAREN, lexer.RBRACK, lexer.RBRACE, lexer.BSLASH, lexer.EOF:
		return a
	// If the token is a comment, ignore it.
	case lexer.CMNTLIT:
		a.Nodos = a.Nodos[:len(a.Nodos)-1]
		return EmpujaNodosBases(a)
	default:
		return EmpujaNodosBases(a)
	}
}
