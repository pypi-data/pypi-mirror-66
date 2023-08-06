# C package manager python package (works with `github`)


# Installation
```bash
pip install cpacman
```

# Run
```bash
# installing packages from file 
cpacman -r             requirements.cpacman
cpacman --requirements requirements.cpacman

# installing packages from all .cpacman files reqursively
cpacman -ri
cpacman --reqursive_install

# you can remove all not .c .h .cpacman files
cpacman -r requirements.cpacman -с
cpacman -r requirements.cpacman --clean
```

# Flags
|short|long|help|default|
|-----|-    |-  |-|
|-r|--requirements_file| Sets file to be read for packages|None|
|-c|--clean|If setted all not .c .h .cpp .hpp .cpacman| False|
||--install| Sets line to be parsed for package| None|
|-ri|--reqursive_install| If setted it will install packages from all .cpacman files|False|


# Requirements file schema
```bash
path/for/package > url
```

# Example:
- **Requirements file path:** `/Desktop/my_project/requirements.cpacman`
- **Line in file to be processed:** `array/arraylib > author/arraylib`
- **This package will be loaded and saved to:** `./Desktop/my_project/array/arraylib/(files)`


# Correct examples
```bash
string > https://github.com/YoungMeatBoy/stringlib.git
string > https://github.com/YoungMeatBoy/stringlib
string > github.com/YoungMeatBoy/stringlib.git
string > github.com/YoungMeatBoy/stringlib
string > YoungMeatBoy/stringlib.git
string > YoungMeatBoy/stringlib
string/lib > YoungMeatBoy/string
```
