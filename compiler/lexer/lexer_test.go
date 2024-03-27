// This module contains the tests for the lexer package.
package lexer_test

import (
	"GoCompiler/lexer"
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

// TestBuscaProximoToken attempts to lex the input file and returns the tokens.
func TestBuscaProximoToken(t *testing.T) {
	// Know...
	var tkzd lexer.Tokenizador

	// Call the working directory.
	dir, err := os.Getwd()
	if err != nil {
		t.Fatal(err)
	}
	dir = strings.Join(strings.Split(dir, "/")[:len(strings.Split(dir, "/"))-2], "/")

	// Walk the examples directory and lex each file.
	filepath.WalkDir(dir+"/examples", func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			t.Fatal(err)
		}
		if filepath.Ext(path) == ".lej" {
			tkzd = lexer.InicTokenizador(path)
			for {
				tkzd = lexer.BuscaProximoToken(tkzd)
				fmt.Println(tkzd.Tok)
				if tkzd.Tok.Tipo == lexer.EOF {
					break
				}
			}
		}
		return nil
	})
}
