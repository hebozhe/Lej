package parser_test

import (
	"GoCompiler/parser"
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestEmpujaNodosBases(t *testing.T) {
	// Know...
	var anal parser.Analizador
	var dir string
	var err error

	// Call the working directory.
	dir, err = os.Getwd()
	if err != nil {
		t.Fatal(err)
	}
	dir = strings.Join(strings.Split(dir, "/")[:len(strings.Split(dir, "/"))-2], "/")

	// Walk the examples directory and parse each file.
	filepath.WalkDir(dir+"/examples", func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			t.Fatal(err)
		}
		if filepath.Ext(path) == ".lej" {
			anal = parser.InicAnalizador(path)
			anal = parser.EmpujaNodosBases(anal)
			fmt.Println(anal.Tokenizador.Path)
			fmt.Println(parser.HazStringDeNodos(anal.Nodos))
		}
		return nil
	})
}
