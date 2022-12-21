package evaluator

import (
	. "GoInterpreter/node"
	"fmt"
	"os"
)

///////////////////////////////////////////////////////////////////////////////
// Assignment Storage
///////////////////////////////////////////////////////////////////////////////

var AssignMap map[string]interface{} = map[string]interface{}{
	"unsure_count": 0,
}

///////////////////////////////////////////////////////////////////////////////
// Handling val Instantiations and Operations
///////////////////////////////////////////////////////////////////////////////

func buildTrue() []int8 {
	// For terminal "T".
	return []int8{2}
}

func buildFalse() []int8 {
	// For the terminal "F".
	return []int8{0}
}

func buildUnsure() []int8 {
	// For the terminal "U".
	unsureCount, ok := AssignMap["unsure_count"].(int)
	if ok {
		unsureCount++
		AssignMap["unsure_count"] = unsureCount
		// TODO: Why the hell is this quadrupling instead of doubling?
		var uValLen int = 2 << uint(unsureCount-1)
		fmt.Printf("unsureCount is now %d, and uValLen is now %d.\n", unsureCount, uValLen)
		var uVal []int8 = []int8{1}
		var t int8 = 2
		var f int8 = 0
		for i := 0; i < uValLen/2; i++ {
			uVal = append(uVal, t)
		}
		for i := 0; i < uValLen/2; i++ {
			uVal = append(uVal, f)
		}
		return uVal
	}
	print("unsure_count is missing.")
	os.Exit(1)
	return []int8{}
}

func doubleBools(ofVal []int8) []int8 {
	// For "U"-type vals.
	// e.g., [1 2 0] -> [1 2 0 2 0]
	return append(ofVal, ofVal[1:]...)
}

func halveBools(ofVal []int8) []int8 {
	// For "U"-type vals.
	// e.g., [1 2 0 2 0] -> [1 2 0], since half the table is redundant.
	if len(ofVal) == 3 {
		return ofVal
	}
	var boolsPart []int8 = ofVal[1:]
	var halfSize int = len(boolsPart)
	var leftHalf []int8 = boolsPart[:halfSize]
	var rightHalf []int8 = boolsPart[halfSize:]
	for i := 0; i < halfSize; i++ {
		if leftHalf[i] != rightHalf[i] {
			return ofVal
		}
	}
	return ofVal[:halfSize+1]
}

func gilvenkoize(thisVal []int8) []int8 {
	// For "U"-type vals.
	// e.g., [1 0 0 0 0 0 0 0 0] -> [0], since Gilvenko's theorem applies.
	for i := 1; i < len(thisVal); i++ {
		if thisVal[i] > 0 {
			return thisVal
		}
	}
	return []int8{0}
}

func buildNot(fromVal []int8) []int8 {
	for i := 0; i < len(fromVal); i++ {
		fromVal[i] = 2 - fromVal[i]
	}
	return fromVal
}

func buildOr(valA []int8, valB []int8) []int8 {
	// For disjunctions.
	var t int8 = 2
	var f int8 = 0
	if (valA[0] == t) || (valB[0] == t) {
		return []int8{2}
	}
	if valA[0] == f {
		return valB
	}
	if valB[0] == f {
		return valA
	}
	// Assure that both valA and valB are of equal lengths.
	for len(valA) < len(valB) {
		valA = doubleBools(valA)
	}
	for len(valB) < len(valA) {
		valB = doubleBools(valB)
	}
	for i := 0; i < len(valA); i++ {
		if valA[i] < valB[i] {
			valA[i] = valB[i]
		}
	}
	return gilvenkoize(halveBools(valA))
}

func buildAnd(valA []int8, valB []int8) []int8 {
	// For conjunctions.
	var t int8 = 2
	var f int8 = 0
	if (valA[0] == f) || (valB[0] == f) {
		return []int8{0}
	}
	if valA[0] == t {
		return valB
	}
	if valB[0] == t {
		return valA
	}
	// Assure that both valA and valB are of equal lengths.
	for len(valA) < len(valB) {
		valA = doubleBools(halveBools(valA))
	}
	for len(valB) < len(valA) {
		valB = doubleBools(valB)
	}
	for i := 0; i < len(valA); i++ {
		if valA[i] > valB[i] {
			valA[i] = valB[i]
		}
	}
	return gilvenkoize(valA)
}

func evaluateValExpr(valExpr *Node) []int8 {
	// For already assigned VAL-VARs.
	fmt.Printf("Evaluating %v\n", valExpr)
	if valExpr.Name == "VAL-VAR" {
		var valIDKey string = valExpr.Left.Literal
		valIDValue, ok := AssignMap[valIDKey]
		if !ok {
			fmt.Println(valIDKey, " is not a valid VAL ID.")
			os.Exit(1)
		}
		valIDValueChecked, ok := valIDValue.([]int8)
		if !ok {
			fmt.Println(valIDKey, " is of the wrong type ", valIDValueChecked, ".")
			os.Exit(1)
		}
		return valIDValueChecked
	}
	// For all terminals.
	if valExpr.Action == "buildTrue" {
		return buildTrue()
	}
	if valExpr.Action == "buildFalse" {
		return buildFalse()
	}
	if valExpr.Action == "buildUnsure" {
		return buildUnsure()
	}
	if valExpr.Action == "LEFT" {
		return evaluateValExpr(valExpr.Left)
	}
	// For all nonterminals.
	if valExpr.Action == "buildNot" {
		var leftSide []int8 = evaluateValExpr(valExpr.Left)
		return buildNot(leftSide)
	}
	if valExpr.Action == "buildOr" {
		var leftSide []int8 = evaluateValExpr(valExpr.Left)
		var rightSide []int8 = evaluateValExpr(valExpr.Right)
		return buildOr(leftSide, rightSide)
	}
	if valExpr.Action == "buildAnd" {
		var leftSide []int8 = evaluateValExpr(valExpr.Left)
		var rightSide []int8 = evaluateValExpr(valExpr.Right)
		return buildAnd(leftSide, rightSide)
	}
	fmt.Printf("%s to perform action %s cannot be correctly evaluated.\n", valExpr.Name, valExpr.Action)
	os.Exit(1)
	return []int8{}
}

func assignVal(thisNode *Node) {
	if thisNode.Left.Name == "VAL-VAR" {
		var assignKey string = thisNode.Left.Left.Literal
		var assignValue []int8
		assignValue = evaluateValExpr(thisNode.Right)
		AssignMap[assignKey] = evaluateValExpr(thisNode.Right)
		fmt.Printf("%s successfully assigned to %v.\n\n", assignKey, assignValue)
		return
	}
	fmt.Printf("Invalid type for assignVal.\n")
	os.Exit(1)
	return
}

///////////////////////////////////////////////////////////////////////////////
// Walking the AST
///////////////////////////////////////////////////////////////////////////////

func WalkTree(thisTree *Node) {
	if thisTree.Action == "BOTH" {
		WalkTree(thisTree.Left)
		WalkTree(thisTree.Right)
		return
	}
	if thisTree.Action == "LEFT" {
		WalkTree(thisTree.Left)
		return
	}
	if thisTree.Action == "RIGHT" {
		WalkTree(thisTree.Right)
		return
	}
	if thisTree.Action == "assignVal" {
		assignVal(thisTree)
		return
	}
	fmt.Printf("%s's %s has not yet been implemented.\n", thisTree.Name, thisTree.Action)
	os.Exit(1)
	return
}
