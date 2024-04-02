// This file defines the lexical tokens constants of TokType for the Lej lexer,
// houses the function to generate new token structs of type Tok,
// houses the functions to check if a string can legally be considered for Tok construction,
// and houses the functions to return the respective TokType values after a check.
package lexer

// TokTipo represents a lexical token for Lej.
type TokTipo string

// Constants representing special tokens, comments, whitespace, scope operators, punctuation, variables, function keywords, function call keywords, conditional keywords, do-times loop keywords, built-in meta-function keywords, operators, and type signatures.
// All tokens being terminal symbols will be represented in ALL CAPS.
const (
	// Special tokens:
	ILL TokTipo = "ILL" // Illegal token
	EOF TokTipo = "EOF" // End of file

	// Comments:
	TILDE TokTipo = "~" // Comment

	// Whitespace:
	SPACE TokTipo = " "  // Whitespace
	NEWLN TokTipo = "\n" // Newline
	TAB   TokTipo = "\t" // Tab
	CARTN TokTipo = "\r" // Carriage return

	// Scope operators:
	LPAREN TokTipo = "(" // Left parenthesis (open)
	RPAREN TokTipo = ")" // Right parenthesis (close)

	// Punctuation:
	COMMA  TokTipo = ","  // Comma
	SEMI   TokTipo = ";"  // Semicolon
	COLON  TokTipo = ":"  // Colon
	BSLASH TokTipo = "\\" // Backslash
	EXCLAM TokTipo = "!"  // Exclamation mark

	// Variables:
	NAME   TokTipo = "NAME" // Identifier
	NONAME TokTipo = "_"    // Noname

	// Assignment Keyword:
	IS TokTipo = "is" // Is keyword

	// Function Keywords:
	TAKE TokTipo = "take" // Function argument
	WANT TokTipo = "want" // Function expected return
	KNOW TokTipo = "know" // Function local variable type info
	GIVE TokTipo = "give" // Function return

	// Function Call Keywords:
	WITH TokTipo = "with" // Function call argument
	AS   TokTipo = "as"   // Parameter call argument

	// Conditional Keywords:
	IF        TokTipo = "if"        // If statement
	ELSE      TokTipo = "else"      // Else statement
	OTHERWISE TokTipo = "otherwise" // Otherwise statement

	// For-Some-Time Loop Keywords:
	FOR  TokTipo = "for"  // For statement
	SOME TokTipo = "some" // Some keyword
	TIME TokTipo = "time" // Time keyword
	DO   TokTipo = "do"   // Do statement
	THIS TokTipo = "this" // This keyword, mainly used in function and structure definitions.
	BACK TokTipo = "back" // Back keyword
	OUT  TokTipo = "out"  // Out keyword

	// Built-In Meta-Function Keywords:
	LIVE TokTipo = "live" // Live function name
	DIE  TokTipo = "die"  // Die function name

	// Operators:
	LBRACK TokTipo = "[" // Subtype delimiter open
	RBRACK TokTipo = "]" // Subtype delimiter close
	// Operators for Evaluables:
	EQ TokTipo = "=" // Assignment
	// Operators and Primitives for Brouwerians:
	AND    TokTipo = "and"    // Logical conjunction
	OR     TokTipo = "or"     // Logical disjunction
	NOT    TokTipo = "not"    // Logical negation
	TRUE   TokTipo = "true"   // Intuitionistic true
	FALSE  TokTipo = "false"  // Intuitionistic false
	UNSURE TokTipo = "unsure" // Kleene unsure
	// Operators for Comparables:
	LT TokTipo = "<" // Less than
	// Operators and Primitives for Naturals:
	PLUS  TokTipo = "+"    // Addition
	MINUS TokTipo = "-"    // Subtraction
	MULT  TokTipo = "*"    // Multiplication
	MOD   TokTipo = "%"    // Modulus
	MANY  TokTipo = "many" // Infinity
	// Operators for Runes:
	BTICK TokTipo = "`" // Rune literal delimiter
	// Operators for Structures:
	OF TokTipo = "of" // Structure field access
	// Operators for Rationals:
	DIV TokTipo = "/" // Division
	DEC TokTipo = "." // Decimal point
	// Operators for Iterables:
	AT     TokTipo = "at"   // Iterable element access
	FROM   TokTipo = "from" // Iterable range start
	TO     TokTipo = "to"   // Iterable range end
	CONCAT TokTipo = "&"    // Iterable concatenation
	// Operators for Tuples and Lists:
	LBRACE TokTipo = "{"
	RBRACE TokTipo = "}"
	// Operators for Graphemes:
	SQUO TokTipo = "'" // Character and pheme literal delimiter
	// Operators for Textuals:
	DQUO TokTipo = "\"" // String literal delimiter
	// Operators for Lookups:
	K TokTipo = "K" // Lookup key flag

	// Type Signatures:
	FUN   TokTipo = "fun"   // Function signature
	BROU  TokTipo = "brou"  // Brouwerian signature
	COMP  TokTipo = "comp"  // Comparable signature
	NAT   TokTipo = "N"     // Natural number signature
	NAT8  TokTipo = "nat8"  // 8-bit natural number signature
	NAT16 TokTipo = "nat16" // 16-bit natural number signature
	NAT32 TokTipo = "nat32" // 32-bit natural number signature
	NAT64 TokTipo = "nat64" // 64-bit natural number signature
	INT   TokTipo = "Z"     // Integer number signature
	INT8  TokTipo = "int8"  // 8-bit integer number signature
	INT16 TokTipo = "int16" // 16-bit integer number signature
	INT32 TokTipo = "int32" // 32-bit integer number signature
	INT64 TokTipo = "int64" // 64-bit integer number signature
	BYTE  TokTipo = "byte"  // Byte signature
	GLY   TokTipo = "gly"   // Glyph signature
	MARK  TokTipo = "mrk"   // Mark signature
	RUNE  TokTipo = "rune"  // Rune signature
	SCT   TokTipo = "sct"   // Structure signature
	RAT   TokTipo = "Q"     // Rational number signature
	RAT8  TokTipo = "rat8"  // 8-bit rational number signature
	RAT16 TokTipo = "rat16" // 16-bit rational number signature
	RAT32 TokTipo = "rat32" // 32-bit rational number signature
	RAT64 TokTipo = "rat64" // 64-bit rational number signature
	REC   TokTipo = "rec"   // Record signature
	DATA  TokTipo = "data"  // Data signature
	ITR   TokTipo = "itr"   // Iterable signature
	TUP   TokTipo = "tup"   // Tuple signature
	LIST  TokTipo = "list"  // List signature
	GPH   TokTipo = "gph"   // Grapheme signature
	CHR   TokTipo = "chr"   // Character signature
	PHEME TokTipo = "pheme" // Pheme signature
	TXT   TokTipo = "txt"   // Textual signature
	STR   TokTipo = "str"   // String signature
	TEXT  TokTipo = "text"  // Text signature
	LKP   TokTipo = "lkp"   // Lookup signature
	MAP   TokTipo = "map"   // Map signature
	DICT  TokTipo = "dict"  // Dictionary signature

	// Type Aliasing:
	SEE TokTipo = "see" // Type aliasing

	// Non-Predefined Literals:
	// NAME handles the NAMELIT token type
	CMNTLIT TokTipo = "CMNTLIT" // Comment literal
	DIGLIT  TokTipo = "DIGLIT"  // Digit literal
	RUNELIT TokTipo = "RUNELIT" // Rune literal
	GPHLIT  TokTipo = "GPHLIT"  // Grapheme literal
	TXTLIT  TokTipo = "TXTLIT"  // Textual literal
)

// Tok represents a token with its type, literal value, position, and line number.
type Tok struct {
	Tipo TokTipo
	Lit  string
	Ini  uint
	Fin  uint
	Lin  uint
}

type TTFeed struct {
	tipo TokTipo
	enc  bool // Whether the token was found (encontrado).
}

// nuTTFeed creates a new TTFeed struct with the given type and encoding.
func nuTTFeed(tipo TokTipo, enc bool) TTFeed {
	return TTFeed{tipo, enc}
}

// nuTok creates a new token with the given type, literal value, position, and line number.
func nuTok(tipo TokTipo, lit string, ini uint, fin uint, lin uint) Tok {
	return Tok{tipo, lit, ini, fin, lin}
}

// esEspacio checks if the given character is a whitespace character.
func esEspacio(b byte) bool {
	// Know...
	var cTok TokTipo = TokTipo(b)
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
	var cTok TokTipo = TokTipo(b)
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
	var sTok TokTipo = TokTipo(bs)
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
	// For-Some-Time Loop Keywords:
	case FOR:
		return nuTTFeed(FOR, true)
	case SOME:
		return nuTTFeed(SOME, true)
	case TIME:
		return nuTTFeed(TIME, true)
	case DO:
		return nuTTFeed(DO, true)
	case THIS:
		return nuTTFeed(THIS, true)
	case BACK:
		return nuTTFeed(BACK, true)
	case OUT:
		return nuTTFeed(OUT, true)
	// Built-In Meta-Function Keywords:
	case LIVE:
		return nuTTFeed(LIVE, true)
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
	case TXT:
		return nuTTFeed(TXT, true)
	case STR:
		return nuTTFeed(STR, true)
	case TEXT:
		return nuTTFeed(TEXT, true)
	case LKP:
		return nuTTFeed(LKP, true)
	case MAP:
		return nuTTFeed(MAP, true)
	case DICT:
		return nuTTFeed(DICT, true)
	// Type Aliasing:
	case SEE:
		return nuTTFeed(SEE, true)
	// Miscellaneous alphabetic constants and keywords:
	case MANY:
		return nuTTFeed(MANY, true)
	case K:
		return nuTTFeed(K, true)
	default:
		return nuTTFeed(ILL, false)
	}
}
