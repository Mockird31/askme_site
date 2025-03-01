package calculator

import (
	"fmt"
	"strconv"
	"strings"
	"unicode"
)

type tokenType int

const (
	NUMBER tokenType = iota
	PLUS
	MINUS
	MULTIPLY
	DIVIDE
	LPAREN
	RPAREN
	UNARY_MINUS
	INVALID
)

type token struct {
	operation tokenType
	value     string
}

type MyCalculator struct {
	expression string
	tokens     []token
}

func newCalculator(expression string) *MyCalculator {
	calc := &MyCalculator{expression: expression}
	return calc
}

func (calc *MyCalculator) tokenize() error {
	runes := []rune(strings.ReplaceAll(calc.expression, " ", ""))
	for i := 0; i < len(runes); {
		switch {
		case runes[i] == '-' && (i == 0 || (i > 0 && (calc.tokens[len(calc.tokens)-1].operation == LPAREN || calc.tokens[len(calc.tokens)-1].operation == PLUS || calc.tokens[len(calc.tokens)-1].operation == MINUS || calc.tokens[len(calc.tokens)-1].operation == MULTIPLY || calc.tokens[len(calc.tokens)-1].operation == DIVIDE))):
			// Check if the next character is an opening parenthesis
			if i+1 < len(runes) && runes[i+1] == '(' {
				// This is a unary minus before a parenthesis
				calc.tokens = append(calc.tokens, token{UNARY_MINUS, "-"})
				i++
			} else {
				// This is a negative number
				start := i
				i++
				for i < len(runes) && (unicode.IsDigit(runes[i]) || runes[i] == '.') {
					i++
				}
				calc.tokens = append(calc.tokens, token{NUMBER, string(runes[start:i])})
			}
		case unicode.IsDigit(runes[i]) || runes[i] == '.':
			start := i
			for i < len(runes) && (unicode.IsDigit(runes[i]) || runes[i] == '.') {
				i++
			}
			calc.tokens = append(calc.tokens, token{NUMBER, string(runes[start:i])})
		case runes[i] == '+':
			calc.tokens = append(calc.tokens, token{PLUS, string(runes[i])})
			i++
		case runes[i] == '-':
			calc.tokens = append(calc.tokens, token{MINUS, string(runes[i])})
			i++
		case runes[i] == '*':
			calc.tokens = append(calc.tokens, token{MULTIPLY, string(runes[i])})
			i++
		case runes[i] == '/':
			calc.tokens = append(calc.tokens, token{DIVIDE, string(runes[i])})
			i++
		case runes[i] == '(':
			calc.tokens = append(calc.tokens, token{LPAREN, string(runes[i])})
			i++
		case runes[i] == ')':
			calc.tokens = append(calc.tokens, token{RPAREN, string(runes[i])})
			i++
		default:
			return fmt.Errorf("invalid char %c", runes[i])
		}
	}
	return nil
}

func (calc *MyCalculator) parse() (float64, error) {
	pos := 0
	
	var parseExpression func() (float64, error)
	var parseTerm func() (float64, error)
	var parsePrimary func() (float64, error)

	parsePrimary = func() (float64, error) {
		if pos >= len(calc.tokens) {
			return 0, fmt.Errorf("unexpected end of expression")
		}
		tok := calc.tokens[pos]
		pos++

		switch tok.operation {
		case NUMBER:
			return strconv.ParseFloat(tok.value, 64)
		case UNARY_MINUS:
			result, err := parsePrimary()
			if err != nil {
				return 0, err
			}
			return -result, nil
		case LPAREN:
			result, err := parseExpression()
			if err != nil {
				return 0, err
			}
			if pos >= len(calc.tokens) || calc.tokens[pos].operation != RPAREN {
				return 0, fmt.Errorf("missing closing parenthesis")
			}
			pos++
			return result, nil
		default:
			return 0, fmt.Errorf("unexpected token: %s", tok.value)
		}
	}

	parseTerm = func() (float64, error) {
		result, err := parsePrimary()
		if err != nil {
			return 0, err
		}
		for pos < len(calc.tokens) && (calc.tokens[pos].operation == MULTIPLY || calc.tokens[pos].operation == DIVIDE) {
			op := calc.tokens[pos]
			pos++
			next, err := parsePrimary()
			if err != nil {
				return 0, err
			}
			if op.operation == MULTIPLY {
				result *= next
			} else {
				if next == 0 {
					return 0, fmt.Errorf("division by zero")
				}
				result /= next
			}
		}
		return result, nil
	}

	parseExpression = func() (float64, error) {
		result, err := parseTerm()
		if err != nil {
			return 0, err
		}
		for pos < len(calc.tokens) && (calc.tokens[pos].operation == PLUS || calc.tokens[pos].operation == MINUS) {
			op := calc.tokens[pos]
			pos++
			next, err := parseTerm()
			if err != nil {
				return 0, err
			}
			if op.operation == PLUS {
				result += next
			} else {
				result -= next
			}
		}
		return result, nil
	}

	return parseExpression()
}

func CalcExpression(expression string) (float64, error) {
	calc := newCalculator(expression)
	result := 0.0
	err := calc.tokenize()
	if err != nil {
		return result, err
	}
	result, err = calc.parse()
	if err != nil {
		return 0.0, err
	}
	return result, nil
}