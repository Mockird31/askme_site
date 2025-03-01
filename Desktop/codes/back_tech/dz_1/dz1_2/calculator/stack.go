package calculator

import (
	"errors"
)

type Stack struct {
	data []byte
}

func newStack() *Stack {
	return &Stack{}
}

func (s *Stack) push(b byte) {
	s.data = append(s.data, b)
}

func (s *Stack) isEmpty() bool {
	return len(s.data) == 0
}

func (s *Stack) pop() (byte, error) {
	if s.isEmpty() {
		return 0, errors.New("empty stack")
	}
	b := s.data[len(s.data)-1]
	s.data = s.data[:len(s.data)-1]
	return b, nil
}

func CheckParentheses(expression string) bool {
	s := newStack()
	for _, elem := range expression {
		if elem == '(' {
			s.push(byte(elem))
		} else if elem == ')' {
			_, err := s.pop()
			if err != nil {
				return false
			}
		}
	}
	return s.isEmpty()
}
