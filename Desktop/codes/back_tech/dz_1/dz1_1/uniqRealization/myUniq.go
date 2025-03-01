package myUniq

import (
	"bufio"
	fileWorker "dz1/fileWorker"
	"flag"
	"os"
	"strconv"
	"strings"
)

type Options struct {
	Counter    bool
	Repeated   bool
	Unique     bool
	IgnoreCase bool
	SkipFields int
	SkipChars  int
	inputFile  string
	OutputFile string
}

type Uniq struct {
	data    []string
	options Options
}

func (u *Uniq) SetData(data []string) {
	u.data = data
}

func (u *Uniq) SetOptions(options Options) {
	u.options = options
}

func ParseArgs() *Options {
	options := Options{}

	flag.BoolVar(&options.Counter, "c", false, "counts the number of occurrences of a string")
	flag.BoolVar(&options.Repeated, "d", false, "prints only Repeated lines")
	flag.BoolVar(&options.Unique, "u", false, "prints only unique lines")
	flag.BoolVar(&options.IgnoreCase, "i", false, "ignores case")

	flag.IntVar(&options.SkipFields, "f", 0, "skips the first N fields")
	flag.IntVar(&options.SkipChars, "s", 0, "skips the first N characters")

	flag.Parse()

	args := flag.Args()
	if len(args) > 0 {
		options.inputFile = args[0]
	}
	if len(args) > 1 {
		options.OutputFile = args[1]
	}
	return &options
}

func NewUniq(options *Options) (*Uniq, error) {
	var data []string
	var err error
	if options.inputFile != "" {
		data, err = fileWorker.ReadFile(options.inputFile)
		if err != nil {
			return nil, err
		}
	} else {
		scanner := bufio.NewScanner(os.Stdin)
		for scanner.Scan() {
			data = append(data, scanner.Text())
		}

		err = scanner.Err()
		if err != nil {
			return nil, err
		}
	}
	return &Uniq{data: data, options: *options}, nil
}

func (u *Uniq) commonHandle() []string {
	var result []string
	var lastLine string
	for _, line := range u.data {
		if lastLine != line {
			result = append(result, line)
		}
		lastLine = line
	}
	return result
}

func (u *Uniq) counterHandle() []string {
	var result []string
	lastLine := u.data[0]
	var counter int = 0

	for i := 0; i < len(u.data); i++ {
		if lastLine != u.data[i] {
			result = append(result, strconv.Itoa(counter)+" "+u.data[i-1])
			counter = 1
		} else {
			counter++
		}
		lastLine = u.data[i]
	}
	result = append(result, strconv.Itoa(counter)+" "+u.data[len(u.data)-1])
	return result
}

func (u *Uniq) RepeatedHandle() []string {
	var result []string
	var lastLine string
	var isRepeated bool
	for _, line := range u.data {
		if lastLine == line && !isRepeated {
			isRepeated = true
			result = append(result, line)
		} else {
			isRepeated = false
		}
		lastLine = line
	}
	return result
}

func (u *Uniq) uniqueHandle() []string {
	var result []string
	dataLen := len(u.data)

	if dataLen == 0 {
		return result
	}

	for i := 0; i < dataLen; i++ {
		if i == 0 && u.data[i] != u.data[i+1] {
			result = append(result, u.data[i])
		} else if i == dataLen-1 && u.data[i] != u.data[i-1] {
			result = append(result, u.data[i])
		} else if i > 0 && i < dataLen-1 && u.data[i] != u.data[i-1] && u.data[i] != u.data[i+1] {
			result = append(result, u.data[i])
		}
	}
	return result
}

func (u *Uniq) ignoreCaseHandle() []string {
	var tempLine string
	var result []string
	for _, line := range u.data {
		if !strings.EqualFold(line, tempLine) {
			result = append(result, line)
		}
		tempLine = line
	}
	return result
}

func (u *Uniq) removeDuplicateLines(lines []string) []string {
	var result []string
	var lastLine string
	for i, line := range lines {
		if lastLine != line {
			result = append(result, u.data[i])
		}
		lastLine = line
	}
	return result
}

func (u *Uniq) skipFieldsHandle() []string {
	var result []string
	var lines = make([]string, len(u.data))

	for i, line := range u.data {
		words := strings.Fields(line)
		if len(words) > u.options.SkipFields {
			lines[i] = strings.Join(words[u.options.SkipFields:], " ")
		} else {
			lines[i] = line
		}
	}

	result = u.removeDuplicateLines(lines)

	return result
}

func (u *Uniq) skipCharsHandle() []string {
	var result []string
	var lines = make([]string, len(u.data))

	for i, line := range u.data {
		if len(line) > u.options.SkipChars {
			lines[i] = line[u.options.SkipChars:]
		} else {
			lines[i] = line
		}
	}

	result = u.removeDuplicateLines(lines)

	return result
}

func (u *Uniq) Process() []string {
	handlers := []struct {
		condition bool
		handler   func() []string
	}{
		{u.options.Counter, u.counterHandle},
		{u.options.Repeated, u.RepeatedHandle},
		{u.options.Unique, u.uniqueHandle},
		{u.options.IgnoreCase, u.ignoreCaseHandle},
		{u.options.SkipFields != 0, u.skipFieldsHandle},
		{u.options.SkipChars != 0, u.skipCharsHandle},
	}
	var result []string
	flagUsed := false
	for _, h := range handlers {
		if h.condition {
			result = h.handler()
			flagUsed = true
		}
	}
	if !flagUsed {
		result = u.commonHandle()
	}
	return result
}
