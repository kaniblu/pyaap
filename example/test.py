"""Resolving Path Arguments in Configs Relative to the Configs' Path

Run this test script from a directory other than where it resides, and you will
still be able to read from `a.txt`.

e.g.
```
    cd /
    python <path to example>/test.py --config <path to example>/config.yml
"""

from yaap import path
from yaap import ArgParser


if __name__ == "__main__":
    parser = ArgParser(allow_config=True)
    parser.a("--foo", type=path)
    parser.add_mutex_switch("bar", {"this", "that"})

    args = parser.parse_args()

    print("Arguments: ")
    print(args)

    txt = open(args.foo, "r").read()

    print("Contents of foo: ")
    print(txt)

    assert txt == "This text is originally from \"a.txt\""