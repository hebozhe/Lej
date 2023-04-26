package errors

import (
	"fmt"
	"os"
)

func ThrowError(name string, span string, start int, end int) {
	switch name {
	case "Invalid Literal":
		fmt.Printf("\n%s:\n The characters \"%s\" from position %d to %d do not form a valid keyword, identifier, or integer literal.\n", name, span, start, end)
	case "Invalid Identifier":
		fmt.Printf("\n%s:\n The characters \"%s\" from position %d to %d do not form a valid identifier.\nA valid identifier must start with a lowercase ASCII character and contain only uppercase ASCII characters or digits after the first.\n", name, span, start, end)
	default:
		fmt.Printf("\nLej's creators forgot to explain what \"%s from %d to %d\" even means.\n", name, start, end)
	}
	fmt.Print("This Lej program has terminated.\n")
	os.Exit(1)
}
