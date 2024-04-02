// This package contains the grammar for the Lej parser.
package parser

type Regla struct {
	Padre     NodoTipo
	Hijos     []NodoTipo
	Guardados []uint8
}

func nuRegla(padre NodoTipo, hijos []NodoTipo, guardados []uint8) Regla {
	return Regla{
		Padre:     padre,
		Hijos:     hijos,
		Guardados: guardados,
	}
}
