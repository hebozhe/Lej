// This file defines the lexical tokens constants of TokType for the Lej lexer,
// houses the function to generate new token structs of type Tok,
// houses the functions to check if a string can legally be considered for Tok construction,
// and houses the functions to return the respective TokType values after a check.
package lexer

// TokType represents a lexical token for Lej.
type TokType string

// Constants representing special tokens, comments, whitespace, scope operators, punctuation, variables, function keywords, function call keywords, conditional keywords, do-times loop keywords, built-in meta-function keywords, operators, and type signatures.
// All tokens being terminal symbols will be represented in ALL CAPS.
const (
	// Special tokens:
	ILL TokType = "ILL" // Illegal token
	EOF TokType = "EOF" // End of file

	// Comments:
	TILDE TokType = "~" // Comment

	// Whitespace:
	SPACE TokType = " "  // Whitespace
	NEWLN TokType = "\n" // Newline
	TAB   TokType = "\t" // Tab
	CARTN TokType = "\r" // Carriage return

	// Scope operators:
	LPAREN TokType = "(" // Left parenthesis (open)
	RPAREN TokType = ")" // Right parenthesis (close)

	// Punctuation:
	COMMA  TokType = ","  // Comma
	SEMI   TokType = ";"  // Semicolon
	COLON  TokType = ":"  // Colon
	BSLASH TokType = "\\" // Backslash
	EXCLAM TokType = "!"  // Exclamation mark

	// Variables:
	NAME   TokType = "NAME" // Identifier
	NONAME TokType = "_"    // Noname

	// Assignment Keyword:
	IS TokType = "is" // Is keyword

	// Function Keywords:
	TAKE TokType = "take" // Function argument
	WANT TokType = "want" // Function expected return
	KNOW TokType = "know" // Function local variable type info
	GIVE TokType = "give" // Function return

	// Function Call Keywords:
	WITH TokType = "with" // Function call argument
	AS   TokType = "as"   // Parameter call argument

	// Conditional Keywords:
	IF        TokType = "if"        // If statement
	ELSE      TokType = "else"      // Else statement
	OTHERWISE TokType = "otherwise" // Otherwise statement

	// Do-Times Loop Keywords:
	DO    TokType = "do"    // Do statement
	THIS  TokType = "this"  // This keyword, mainly used in function and structure definitions.
	TIMES TokType = "times" // Times keyword
	BACK  TokType = "back"  // Back keyword
	OUT   TokType = "out"   // Out keyword

	// Built-In Meta-Function Keywords:
	DIE TokType = "die" // Die function name

	// Operators:
	LBRACK TokType = "[" // Subtype delimiter open
	RBRACK TokType = "]" // Subtype delimiter close
	// Operators for Evaluables:
	EQ TokType = "=" // Assignment
	// Operators and Primitives for Brouwerians:
	AND    TokType = "and"    // Logical conjunction
	OR     TokType = "or"     // Logical disjunction
	NOT    TokType = "not"    // Logical negation
	TRUE   TokType = "true"   // Intuitionistic true
	FALSE  TokType = "false"  // Intuitionistic false
	UNSURE TokType = "unsure" // Kleene unsure
	// Operators for Comparables:
	LT TokType = "<" // Less than
	// Operators and Primitives for Naturals:
	PLUS  TokType = "+"    // Addition
	MINUS TokType = "-"    // Subtraction
	MULT  TokType = "*"    // Multiplication
	MOD   TokType = "%"    // Modulus
	MANY  TokType = "many" // Infinity
	// Operators for Runes:
	BTICK TokType = "`" // Rune literal delimiter
	// Operators for Structures:
	OF TokType = "of" // Structure field access
	// Operators for Rationals:
	DIV TokType = "/" // Division
	DEC TokType = "." // Decimal point
	// Operators for Iterables:
	AT     TokType = "at"   // Iterable element access
	FROM   TokType = "from" // Iterable range start
	TO     TokType = "to"   // Iterable range end
	CONCAT TokType = "&"    // Iterable concatenation
	// Operators for Tuples and Lists:
	LBRACE TokType = "{"
	RBRACE TokType = "}"
	// Operators for Graphemes:
	SQUO TokType = "'" // Character and pheme literal delimiter
	// Operators for Textuals:
	DQUO TokType = "\"" // String literal delimiter
	// Operators for Lookups:
	K TokType = "K" // Lookup key flag

	// Type Signatures:
	FUN   TokType = "fun"   // Function signature
	BROU  TokType = "brou"  // Brouwerian signature
	COMP  TokType = "comp"  // Comparable signature
	NAT   TokType = "N"     // Natural number signature
	NAT8  TokType = "N8"    // 8-bit natural number signature
	NAT16 TokType = "N16"   // 16-bit natural number signature
	NAT32 TokType = "N32"   // 32-bit natural number signature
	NAT64 TokType = "N64"   // 64-bit natural number signature
	INT   TokType = "Z"     // Integer number signature
	INT8  TokType = "Z8"    // 8-bit integer number signature
	INT16 TokType = "Z16"   // 16-bit integer number signature
	INT32 TokType = "Z32"   // 32-bit integer number signature
	INT64 TokType = "Z64"   // 64-bit integer number signature
	BYTE  TokType = "byte"  // Byte signature
	GLY   TokType = "gly"   // Glyph signature
	MARK  TokType = "mrk"   // Mark signature
	RUNE  TokType = "rune"  // Rune signature
	SCT   TokType = "sct"   // Structure signature
	RAT   TokType = "Q"     // Rational number signature
	RAT8  TokType = "Q8"    // 8-bit rational number signature
	RAT16 TokType = "Q16"   // 16-bit rational number signature
	RAT32 TokType = "Q32"   // 32-bit rational number signature
	RAT64 TokType = "Q64"   // 64-bit rational number signature
	REC   TokType = "rec"   // Record signature
	DATA  TokType = "data"  // Data signature
	ITR   TokType = "itr"   // Iterable signature
	TUP   TokType = "tup"   // Tuple signature
	LIST  TokType = "list"  // List signature
	GPH   TokType = "gph"   // Grapheme signature
	CHR   TokType = "chr"   // Character signature
	PHEME TokType = "pheme" // Pheme signature
	STR   TokType = "str"   // String signature
	TXT   TokType = "txt"   // Text signature
	CTXT  TokType = "ctxt"  // Character text signature
	PTXT  TokType = "ptxt"  // Pheme text signature
	LKP   TokType = "lkp"   // Lookup signature
	MAP   TokType = "map"   // Map signature
	DICT  TokType = "dict"  // Dictionary signature

	// Import Keyword:
	USE TokType = "use" // Use keyword

	// Non-Predefined Literals:
	// NAME handles the NAMELIT token type
	CMNTLIT TokType = "CMNTLIT" // Comment literal
	DIGLIT  TokType = "DIGLIT"  // Digit literal
	RUNELIT TokType = "RUNELIT" // Rune literal
	GPHLIT  TokType = "GPHLIT"  // Grapheme literal
	TXTLIT  TokType = "TXTLIT"  // Textual literal
)

// Tok represents a token with its type, literal value, position, and line number.
type Tok struct {
	Tipo TokType
	Lit  string
	Ini  uint
	Fin  uint
	Lin  uint
}

type TTFeed struct {
	tipo TokType
	enc  bool // Whether the token was found (encontrado).
}

// nuTTFeed creates a new TTFeed struct with the given type and encoding.
func nuTTFeed(tipo TokType, enc bool) TTFeed {
	return TTFeed{tipo, enc}
}

// nuTok creates a new token with the given type, literal value, position, and line number.
func nuTok(tipo TokType, lit string, ini uint, fin uint, lin uint) Tok {
	return Tok{tipo, lit, ini, fin, lin}
}

// esEspacio checks if the given character is a whitespace character.
func esEspacio(b byte) bool {
	// Know...
	var cTok TokType = TokType(b)
	return cTok == SPACE || cTok == NEWLN || cTok == TAB || cTok == CARTN
}

// esLetra checks if the given character is a letter.
func esLetra(b byte) bool {
	// Know...
	var c int32 = int32(b)
	return ('a'-1 < c && c < 'z'+1) || ('A'-1 < c && c < 'Z'+1)
}

// esDigito checks if the given character is a digit.
func esDigito(b byte) bool {
	// Know...
	var c int32 = int32(b)
	return '0'-1 < c && c < '9'+1
}

// esNAMETok checks if the given string is a valid identifier by checking if it obeys strict camelCase rules.
func esNAMETok(bs []byte) bool {
	// Know...
	var i uint
	var sLen uint
	var c int32

	sLen = uint(len(bs)) // The legal characters are among the ASCII characters, so are bytes.

	if sLen == 0 {
		return false
	}
	if bs[0] < 'a' || 'z' < bs[0] {
		return false
	}

	i = 1
	for i < sLen {
		c = int32(bs[i])
		if !(('a'-1 < c && c < 'z'+1) || ('A'-1 < c && c < 'Z'+1) || ('0'-1 < c && c < '9'+1)) {
			return false
		}
		i = i + 1
	}
	return true
}

// This section of code returns TTFeed structs with the respective TokType values after a check.

// quePalabraMonobitoSimbolicaEs returns a TTFeed struct of mono-byte symbolic tokens,
// or ILL if the given byte is not a mono-byte symbolic token.
func quePalabraMonobitoSimbolicaEs(b byte) TTFeed {
	// Know...
	var cTok TokType = TokType(b)
	switch cTok {
	// Punctuations for Various Uses:
	case TILDE:
		return nuTTFeed(TILDE, true)
	case LPAREN:
		return nuTTFeed(LPAREN, true)
	case RPAREN:
		return nuTTFeed(RPAREN, true)
	case COMMA:
		return nuTTFeed(COMMA, true)
	case SEMI:
		return nuTTFeed(SEMI, true)
	case COLON:
		return nuTTFeed(COLON, true)
	case BSLASH:
		return nuTTFeed(BSLASH, true)
	case EXCLAM:
		return nuTTFeed(EXCLAM, true)
	case LBRACK:
		return nuTTFeed(LBRACK, true)
	case RBRACK:
		return nuTTFeed(RBRACK, true)
	case LBRACE:
		return nuTTFeed(LBRACE, true)
	case RBRACE:
		return nuTTFeed(RBRACE, true)
	case BTICK:
		return nuTTFeed(BTICK, true)
	case SQUO:
		return nuTTFeed(SQUO, true)
	case DQUO:
		return nuTTFeed(DQUO, true)
	// The operators below are not punctuations, but they are single-byte characters.
	// Operators for Evaluables:
	case EQ:
		return nuTTFeed(EQ, true)
	// Operators for Comparables:
	case LT:
		return nuTTFeed(LT, true)
	// Operators for Naturals and Integers:
	case PLUS:
		return nuTTFeed(PLUS, true)
	case MINUS:
		return nuTTFeed(MINUS, true)
	case MULT:
		return nuTTFeed(MULT, true)
	case MOD:
		return nuTTFeed(MOD, true)
	// Operators for Rationals:
	case DIV:
		return nuTTFeed(DIV, true)
	case DEC:
		return nuTTFeed(DEC, true)
	case CONCAT:
		return nuTTFeed(CONCAT, true)
	// The noname token is not a punctuation, but it is a single-byte character.
	case NONAME:
		return nuTTFeed(NONAME, true)
	default:
		return nuTTFeed(ILL, false)
	}
}

// quePalabraMonobitoAlfanumericaEs returns a TTFeed struct of reserved words, most of which are more than one byte long,
// or ILL if the given byte is not a reserved word.
func quePalabraReservadaAlfanumericaEs(bs []byte) TTFeed {
	// Know...
	var sTok TokType = TokType(bs)
	switch sTok {
	// Assignment Keyword:
	case IS:
		return nuTTFeed(IS, true)
	// Function Keywords:
	case TAKE:
		return nuTTFeed(TAKE, true)
	case WANT:
		return nuTTFeed(WANT, true)
	case KNOW:
		return nuTTFeed(KNOW, true)
	case GIVE:
		return nuTTFeed(GIVE, true)
	// Function Call Keywords:
	case WITH:
		return nuTTFeed(WITH, true)
	case AS:
		return nuTTFeed(AS, true)
	// Conditional Keywords:
	case IF:
		return nuTTFeed(IF, true)
	case ELSE:
		return nuTTFeed(ELSE, true)
	case OTHERWISE:
		return nuTTFeed(OTHERWISE, true)
	// Do-Times Loop Keywords:
	case DO:
		return nuTTFeed(DO, true)
	case THIS:
		return nuTTFeed(THIS, true)
	case TIMES:
		return nuTTFeed(TIMES, true)
	case BACK:
		return nuTTFeed(BACK, true)
	case OUT:
		return nuTTFeed(OUT, true)
	// Built-In Meta-Function Keywords:
	case DIE:
		return nuTTFeed(DIE, true)
	// Operators and Primitives for Brouwerians:
	case AND:
		return nuTTFeed(AND, true)
	case OR:
		return nuTTFeed(OR, true)
	case NOT:
		return nuTTFeed(NOT, true)
	case TRUE:
		return nuTTFeed(TRUE, true)
	case FALSE:
		return nuTTFeed(FALSE, true)
	case UNSURE:
		return nuTTFeed(UNSURE, true)
	// Stucture Field Access:
	case OF:
		return nuTTFeed(OF, true)
	// Operators for Iterables:
	case AT:
		return nuTTFeed(AT, true)
	case FROM:
		return nuTTFeed(FROM, true)
	case TO:
		return nuTTFeed(TO, true)
	// Type Signatures:
	case FUN:
		return nuTTFeed(FUN, true)
	case BROU:
		return nuTTFeed(BROU, true)
	case COMP:
		return nuTTFeed(COMP, true)
	case NAT:
		return nuTTFeed(NAT, true)
	case NAT8:
		return nuTTFeed(NAT8, true)
	case NAT16:
		return nuTTFeed(NAT16, true)
	case NAT32:
		return nuTTFeed(NAT32, true)
	case NAT64:
		return nuTTFeed(NAT64, true)
	case INT:
		return nuTTFeed(INT, true)
	case INT8:
		return nuTTFeed(INT8, true)
	case INT16:
		return nuTTFeed(INT16, true)
	case INT32:
		return nuTTFeed(INT32, true)
	case INT64:
		return nuTTFeed(INT64, true)
	case BYTE:
		return nuTTFeed(BYTE, true)
	case GLY:
		return nuTTFeed(GLY, true)
	case MARK:
		return nuTTFeed(MARK, true)
	case RUNE:
		return nuTTFeed(RUNE, true)
	case SCT:
		return nuTTFeed(SCT, true)
	case RAT:
		return nuTTFeed(RAT, true)
	case RAT8:
		return nuTTFeed(RAT8, true)
	case RAT16:
		return nuTTFeed(RAT16, true)
	case RAT32:
		return nuTTFeed(RAT32, true)
	case RAT64:
		return nuTTFeed(RAT64, true)
	case REC:
		return nuTTFeed(REC, true)
	case DATA:
		return nuTTFeed(DATA, true)
	case ITR:
		return nuTTFeed(ITR, true)
	case TUP:
		return nuTTFeed(TUP, true)
	case LIST:
		return nuTTFeed(LIST, true)
	case GPH:
		return nuTTFeed(GPH, true)
	case CHR:
		return nuTTFeed(CHR, true)
	case PHEME:
		return nuTTFeed(PHEME, true)
	case STR:
		return nuTTFeed(STR, true)
	case TXT:
		return nuTTFeed(TXT, true)
	case CTXT:
		return nuTTFeed(CTXT, true)
	case PTXT:
		return nuTTFeed(PTXT, true)
	case LKP:
		return nuTTFeed(LKP, true)
	case MAP:
		return nuTTFeed(MAP, true)
	case DICT:
		return nuTTFeed(DICT, true)
	// Import Keyword:
	case USE:
		return nuTTFeed(USE, true)
	// Miscellaneous alphabetic constants and keywords:
	case MANY:
		return nuTTFeed(MANY, true)
	case K:
		return nuTTFeed(K, true)
	default:
		return nuTTFeed(ILL, false)
	}
}
