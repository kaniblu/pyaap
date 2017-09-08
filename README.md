# Yet Another Argument Parser

This library is based on `configargparse`, a great argument-parsing library with
some issues in usability and functionality. Some improvements include:

### Method Shortcuts ###

Now use even shorter abbreviations for repetitive method calls such as 

  - `ArgParser.a`: equivalent to `ArgParser.add`
  - `ArgParser.add_group` or `ArgParser.g`: equivalent to `ArgParser.add_argument_group`
  - `ArgParser.add_mutex_group`: equivalent to `ArgParser.add_mutually_exclusive_group`
  
### Mutex Switch Shortcuts ###

If you had to build an mutually exclusive options that store itself as destination value,  
it could quickly become tedious to type out each command for every possible option:
 
```python
mutex_group = parser.add_mutually_exclusive_group(required=True)
mutex_group.add_argument("--choose_pizza", dest="dinner", 
                         action="store_const", const="pizza", 
                         help="choose this option to eat pizza")
mutex_group.add_argument("--choose_spaghetti", dest="dinner", 
                         action="store_const", const="spaghetti", 
                         help="choose this option to eat spaghetti")
...
```

Readability of above code could be improved the code could be written as

```python
parser.add_mutex_switch("dinner", {
    "choose_pizza": "choose this option to eat pizza",
    "choose_spaghetti": "choose this option to eat spaghetti",
    ...
}, required=True)
```

This mutex option can be activated with one of the arguments: `--choose_pizza`, 
`--choose_spaghetti`, etc.

If you do not wish to have separate arguments for each option, you could switch
 the mutex style at any time.
 
 
```python
parser.add_mutex_switch("dinner", {
    "choose_pizza": "choose this option to eat pizza",
    "choose_spaghetti": "choose this option to eat spaghetti",
    ...
}, required=True, single_arg=True)
```

Now this mutex option is accessed with `--dinner='choose_pizza'`.
 
### Path Types ###

`configargparse` is known to be able to load config options from `json` or `yaml` file.
However, irritation arises if you wish to have paths as argument values. Currently, any relative paths in the config file will be treated as strings, so they are resolved from current working directory.
In most cases, however, treating them as paths relative to the path of config file is much more production. You could turn this option off with `config_path_base=False` during initialization of `ArgParser`,  