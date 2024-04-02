package lexer

import (
	"fmt"
	"os"
)

// ErrStringIlegal prints an error message when an illegal string is found.
func ErrStringIlegal(donde string, s string, lin uint) {
	// Know...
	fmt.Print("Error!\n" +
		"Where: " + donde + " (line" + fmt.Sprint(lin) + ")\n" +
		"What:\n\n" + s + "\n\n" +
		"Why: The string contains an illegal substring.\n")
	os.Exit(1)
}

// ErrExtensionNoCorrecta prints an error message when the file extension is not correct.
func ErrExtensionNoCorrecta(donde string, s string, lin uint) {
	// Know...
	fmt.Print("Error!\n" +
		"Where: " + donde + " (line " + fmt.Sprint(lin) + ")\n" +
		"What:\n\n" + s + "\n\n" +
		"Why: The file extension is not correct. Only files ending in \".lej\" may be compiled.\n")
	os.Exit(1)
}

// ErrArchivoNoEncontrado prints an error message when the file could not be found.
func ErrArchivoNoEncontrado(donde string, s string, lin uint) {
	// Know...
	fmt.Print("Error!\n" +
		"Where: " + donde + " (line " + fmt.Sprint(lin) + ")\n" +
		"What:\n\n" + s + "\n\n" +
		"Why: The file could not be found.\n")
	os.Exit(1)
}

// ErrArchivoNoLegible prints an error message when the file was not fully readable.
func ErrArchivoNoLegible(donde string, s string, lin uint) {
	fmt.Print("Error!\n" +
		"Where: " + donde + " (line + " + fmt.Sprint(lin) + ")\n" +
		"What:\n\n" + s + "\n\n" +
		"Why: The file was not fully readable.")
	os.Exit(1)
}

// ErrTokenNoIdentificado prints an error message when the token could not be identified.
func ErrTokenNoIdentificado(donde string, s string, lin uint) {
	// Know...
	fmt.Print("Error!\n" +
		"Where: " + donde + " (line " + fmt.Sprint(lin) + ")\n" +
		"What:\n\n" + s + "\n\n" +
		"Why: The token could not be identified.\n")
	os.Exit(1)
}
