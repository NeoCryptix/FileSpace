## NeoScript Documentation

### About

NeoScript is a simple, English-based variable and file handler through the console. It is interpreted using Python, and should function normally in any Python 3 environment. It was created in early 2023 by @ViolinCat and @hydraXD.

### Config

Config.json contains the settings for the interpreter. If the JSON file is missing or invalid, a default copy will be downloaded and restored from our servers.

debugMode:
> true/false - enables or disables debug mode, containing helpful tools for programmers

debugSys:
> true/false - enables or disables showing system info in debug mode, reducing pre-run clutter in the console, only affects debugMode

runFile:
> file path as text in double-quotes - .NEO (NEOScript) file that the interpreter runs on boot

interpreterFile:
> file path as text in double-quotes - .PY (Python) file that handles the interpreting, useful for those juggling multiple versions of the interpreter

commentChar:
> any characters as text in double-quotes - when this string is present in a line, it will be marked as a comment and passed

walshMode:
> true/false - enables or disables Walsh commands, which are for fun and have no major impact on the program (inside joke, don't take it seriously)

commandDelay:
> number (decimals supported) - a value in seconds that adds a forced delay to every line in the file, essentially a global wait()

logFile:
> file path as text in double-quotes - .TXT (text) file to write debug log messages to

### Basic functions

`output()`
> Prints to console, can print text (single quotes) or a variable name (no quotes)
> > `output('Hello world')` - print text
> >
> > `output(varname)` - print variable

`new()`
> defines a variable or function
> > `name = new(str)('text')` - define string
> > 
> > `name = new(bool)(true/false)` - define Boolean
> > 
> > `name = new(int)(value)` - define integer
> > 
> > `name = new(func)('path')` - define a .NEO file to run as function
>
> > `name = new(random)({min_int}, {max_int})` - define a random integer
>
>In all cases, "name" is the callable name of the variable or function

`wait()`
> adds a delay in seconds before next line
> > `wait(1.5)` - 1 & 1/2 second delay

`toInt()`
>turns a string into an integer (fails if string is anything other than numeric characters)
>> `toInt(strname)` - converts strname string into integer, assigns it to strname

`clearConsole()`
> clears console, will attempt to run correct command after determining OS

`walsh()`
> prints a Walsh quote, requires walshMode to be True
> > `walsh(0)` - quote 0
> >
> > `walsh(1)` - quote 1
> >
> > `walsh(2)` - quote 2
> >
> > `walsh(3)` - quote 3
> >
> > `walsh(r)` - random quote

### Debug mode

Debug mode prints every single command the program runs to console, even if it would normally be hidden. It shows extra errors and line numbers for each command as well.

On run:
>`configFile` - location of config file
>
>`runFile` - location of run file
>
>`operSys` - OS info (Optional with debugSys config parameter)
>
>`pyBuild` - build of Python being used (Optional with debugSys config parameter)

on `output()`:
> `outputMsg: text ` - print text
>
> `outputVar: 

