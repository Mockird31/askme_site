package test

import (
	myUniq "dz1/uniqRealization"
	"fmt"
	"strconv"
	"strings"
	"testing"
)

func parseNumericArg(args []string, index int) (int, error) {
	if index+1 > len(args) {
		return 0, fmt.Errorf("not enough arguments for %s", args[index])
	}
	value, err := strconv.Atoi(args[index+1])
	if err != nil {
		return 0, fmt.Errorf("invalid value for %s", args[index])
	}
	return value, nil
}

func parseArgs(args []string) (*myUniq.Options, error) {
	var options myUniq.Options
	i := 0
	for i < len(args) {
		arg := args[i]
		if strings.HasPrefix(arg, "-") {
			switch arg {
			case "-c":
				options.Counter = true
			case "-d":
				options.Repeated = true
			case "-u":
				options.Unique = true
			case "-i":
				options.IgnoreCase = true
			case "-f", "-s":
				value, err := parseNumericArg(args, i)
				if err != nil {
					return nil, err
				}
				if arg == "-f" {
					options.SkipFields = value
				} else {
					options.SkipChars = value
				}
				i++
			default:
				return nil, fmt.Errorf("invalid argument %s", arg)
			}
		}
		i++
	}
	return &options, nil
}

func parsingFlagsTests(flags string) (*myUniq.Options, error) {
	args := strings.Split(flags, " ")
	options, err := parseArgs(args)
	if err != nil {
		return nil, err
	}
	return options, nil
}

func TestRunUniq(t *testing.T) {
	tests := map[string]struct {
		input  string
		result string
		flags  string
	}{
		"No flags test": {
			"I love music.\nI love music.\nI love music.\n\nI love music of Kartik.\nI love music of Kartik.\nThanks.\nI love music of Kartik.\nI love music of Kartik.",
			"I love music.\n\nI love music of Kartik.\nThanks.\nI love music of Kartik.",
			"",
		},
		"Counter flag test": {
			"Golang\nGolang\nGolang\nPython\nC++\nC++\nPython\nPython",
			"3 Golang\n1 Python\n2 C++\n2 Python",
			"-c",
		},
		"Repeated flag test": {
			"Golang\nGolang\nGolang\nPython\nC++\nC++\nPython\nPython",
			"Golang\nC++\nPython",
			"-d",
		},
		"Unique flag test": {
			"Golang\nGolang\n\nGolang\nPython\nC++\nC++\nPython\nPython",
			"\nGolang\nPython",
			"-u",
		},
		"Ignore case flag test": {
			"GolAng\nGOlang\nGolaNG\nPythON\nC++\nc++\nPyTHon\npYthon",
			"GolAng\nPythON\nC++\nPyTHon",
			"-i",
		},
		"Skip fields flag test": {
			"Lang golang\nany golang\nsome golang\nsnake python\nany python",
			"Lang golang\nsnake python",
			"-f 1",
		},
		"Skip chars flag test": {
			"he golang\nshe golang\nso golang\nsn python\nan python",
			"he golang\nshe golang\nso golang\nsn python",
			"-s 2",
		},
	}
	for name, test := range tests {
		t.Run(name, func(t *testing.T) {
			t.Parallel()
			options, err := parsingFlagsTests(test.flags)
			if err != nil {
				t.Errorf("Error while parsing flags: %s", err)
			}
			data := strings.Split(test.input, "\n")
			var myUniq myUniq.Uniq

			myUniq.SetData(data)
			myUniq.SetOptions(*options)
			got := myUniq.Process()

			if strings.Join(got, "\n") != test.result {
				t.Fatalf("Expected: %s, got: %s", test.result, strings.Join(got, " "))
			}
		})
	}
}
