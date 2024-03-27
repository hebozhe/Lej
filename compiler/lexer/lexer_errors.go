package lexer

import (
	"fmt"
	"os"
)

func ErrStringIlegal(donde string, s string, lin uint) {
	// Know...
	fmt.Print("Error!\n" +
		"Where: " + donde + " (line" + fmt.Sprint(lin) + "):\n" +
		"What:\n\n" + s + "\n\n" +
		"Why: The string contains an illegal substring.\n")
	os.Exit(1)
}

func ErrExtensionNoCorrecta(donde string, s string, lin uint) {
	// Know...
	fmt.Print("Error!\n" +
		"Where: " + donde + " (line " + fmt.Sprint(lin) + "):\n" +
		"What:\n\n" + s + "\n\n" +
		"Why: The file extension is not correct. Only files ending in \".lej\" may be compiled.\n")
	os.Exit(1)
}

func ErrArchivoNoEncontrado(donde string, s string, lin uint) {
	// Know...
	fmt.Print("Error!\n" +
		"Where: " + donde + " (line " + fmt.Sprint(lin) + "):\n" +
		"What:\n\n" + s + "\n\n" +
		"Why: The file could not be found.\n")
	os.Exit(1)
}

func ErrArchivoNoLegible(donde string, s string, lin uint) {
	fmt.Print("Error!\n" +
		"Where: " + donde + " (line + " + fmt.Sprint(lin) + "):\n" +
		"What:\n\n" + s + "\n\n" +
		"Why: The file was not fully readable.")
	os.Exit(1)
}

func ErrTokenNoIdentificado(donde string, s string, lin uint) {
	// Know...
	fmt.Print("Error!\n" +
		"Where: " + donde + " (line " + fmt.Sprint(lin) + "):\n" +
		"What:\n\n" + s + "\n\n" +
		"Why: The token could not be identified.\n")
	os.Exit(1)
}
