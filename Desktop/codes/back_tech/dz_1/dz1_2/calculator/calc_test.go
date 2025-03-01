package calculator

import (
	"testing"
)

func TestCalcExpression(t *testing.T) {
	tests := []struct {
		input    string
		expected float64
		hasError bool
	}{
		{"1+1", 2, false},
		{"2-1", 1, false},
		{"3*3", 9, false},
		{"10/2", 5, false},
		{"10/(5-5)", 0, true}, 
		{"(2+3)*4", 20, false},
		{"2+(3*4)", 14, false},
		{"((2+3)*4)/2", 10, false},
		{"5+", 0, true}, 
		{"abc", 0, true},
	}

	for _, test := range tests {
		result, err := CalcExpression(test.input)
		if test.hasError {
			if err == nil {
				t.Errorf("Expected error for input %q, but got none", test.input)
			}
		} else {
			if err != nil {
				t.Errorf("Unexpected error for input %q: %v", test.input, err)
			}
			if result != test.expected {
				t.Errorf("For input %q expected %v but got %v", test.input, test.expected, result)
			}
		}
	}
}
