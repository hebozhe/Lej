// This package contains the lexer for the Lej compiler. The lexer is responsible for tokenizing the input source code.
package lexer

import (
	"io"
	"os"
)

type Tokenizador struct {
	Path  string
	Ini   uint
	Fin   uint
	Lin   uint
	Tok   Tok
	Bitos []byte
	Blen  uint
}

func leeLejBytes(path string) []byte {
	// Know...
	var file *os.File
	var err error
	var lejBytes []byte

	if path[len(path)-4:] != ".lej" {
		ErrExtensionNoCorrecta(path, path, 0)
	}

	file, err = os.Open(path)
	if err != nil {
		ErrArchivoNoEncontrado(path, path, 0)
	}

	defer file.Close()

	lejBytes, err = io.ReadAll(file)
	if err != nil {
		ErrArchivoNoLegible(path, "", 0)
	}

	return lejBytes
}

func InicTokenizador(path string) Tokenizador {
	// Know
	var bitos []byte
	var tok Tok

	bitos = leeLejBytes(path)
	tok = nuTok(ILL, "", 0, 0, 0)
	return Tokenizador{Path: path, Ini: 0, Fin: 1, Lin: 1, Tok: tok, Bitos: bitos, Blen: uint(len(bitos))}
}

func colocaHastaCerrar(t Tokenizador, cerSim TokTipo) Tokenizador {
	for {
		if t.Fin == t.Blen {
			ErrStringIlegal(t.Path, string(t.Bitos[t.Ini:t.Fin]), t.Lin)
		}
		if TokTipo(t.Bitos[t.Fin]) == NEWLN {
			t.Lin = t.Lin + 1
			continue
		}
		if TokTipo(t.Bitos[t.Fin]) == cerSim && TokTipo(t.Bitos[t.Fin-1]) != BSLASH {
			t.Fin = t.Fin + 1
			return t
		}
		t.Fin = t.Fin + 1
	}
}

func BuscaProximoToken(t Tokenizador) Tokenizador {
	// Know...
	var newTTF TTFeed
	var newTok Tok

	// If the end of the file has been reached, return an EOF token.
	if t.Fin == t.Blen {
		t.Tok = nuTok(EOF, "", t.Fin, t.Fin, t.Lin)
		return t
	}

	// If the inititial byte is a space, skip it.
	if esEspacio(t.Bitos[t.Ini]) {
		if TokTipo(t.Bitos[t.Ini]) == NEWLN {
			t.Lin = t.Lin + 1
		}
		t.Ini = t.Fin
		t.Fin = t.Ini + 1
		return BuscaProximoToken(t)
	}

	// Check if the token is a reserved mono-bit symbol.
	newTTF = quePalabraMonobitoSimbolicaEs(t.Bitos[t.Ini])
	if newTTF.enc {
		switch newTTF.tipo {
		case TILDE: // Comments can collect arbitrary characters until closed.
			t = colocaHastaCerrar(t, TILDE)
			newTok = nuTok(CMNTLIT, string(t.Bitos[t.Ini:t.Fin]), t.Ini, t.Fin, t.Lin)
		case BTICK: // Glyphs can collect arbitrary characters until closed (though only 1 is legal).
			t = colocaHastaCerrar(t, BTICK)
			newTok = nuTok(RUNELIT, string(t.Bitos[t.Ini:t.Fin]), t.Ini, t.Fin, t.Lin)
		case SQUO: // Graphemes can collect arbitrary characters until closed (though only 1 is legal).
			t = colocaHastaCerrar(t, SQUO)
			newTok = nuTok(GPHLIT, string(t.Bitos[t.Ini:t.Fin]), t.Ini, t.Fin, t.Lin)
		case DQUO: // Textuals can collect arbitrary characters until closed.
			t = colocaHastaCerrar(t, DQUO)
			newTok = nuTok(TXTLIT, string(t.Bitos[t.Ini:t.Fin]), t.Ini, t.Fin, t.Lin)
		default:
			newTok = nuTok(newTTF.tipo, string(t.Bitos[t.Ini:t.Fin]), t.Ini, t.Fin, t.Lin)
		}

		t.Tok = newTok
		t.Ini = t.Fin
		t.Fin = t.Ini + 1
		return t
	}

	// Check if the token is a digit literal.
	if esDigito(t.Bitos[t.Ini]) {
		for {
			if esDigito(t.Bitos[t.Fin]) {
				t.Fin = t.Fin + 1
				continue
			}
			newTok = nuTok(DIGLIT, string(t.Bitos[t.Ini:t.Fin]), t.Ini, t.Fin, t.Lin)
			t.Tok = newTok
			t.Ini = t.Fin
			t.Fin = t.Ini + 1
			return t
		}
	}

	// Check if the token is a string literal, either a keyword or a name.
	if esLetra(t.Bitos[t.Ini]) {
		for {
			if esLetra(t.Bitos[t.Fin]) || esDigito(t.Bitos[t.Fin]) {
				t.Fin = t.Fin + 1
				continue
			}
			break
		}

		// Check if the token is a reserved alphanumeric word.
		newTTF = quePalabraReservadaAlfanumericaEs(t.Bitos[t.Ini:t.Fin])
		if newTTF.enc {
			newTok = nuTok(newTTF.tipo, string(t.Bitos[t.Ini:t.Fin]), t.Ini, t.Fin, t.Lin)
			t.Tok = newTok
			t.Ini = t.Fin
			t.Fin = t.Ini + 1
			return t
		}

		// Check if the token is a name (i.e., an identifier).
		if esNAMETok(t.Bitos[t.Ini:t.Fin]) {
			newTok = nuTok(NAME, string(t.Bitos[t.Ini:t.Fin]), t.Ini, t.Fin, t.Lin)
			t.Tok = newTok
			t.Ini = t.Fin
			t.Fin = t.Ini + 1
			return t
		}

		// If the token is not a reserved alphanumeric word or a name, it is an illegal string.
		ErrTokenNoIdentificado(t.Path, string(t.Bitos[t.Ini:t.Fin]), t.Lin)
	}
	ErrTokenNoIdentificado(t.Path, string(t.Bitos[t.Ini:t.Fin]), t.Lin)
	return t // This line will never be reached.
}
