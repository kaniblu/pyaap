import os
import types
import functools

import configargparse


def path(x):
    return str(x)


class ArgParser(configargparse.ArgParser):
    @classmethod
    def attach_methods(cls, target):
        target.add_mutex_switch = \
            types.MethodType(cls.add_mutex_switch, target)
        target.a = types.MethodType(cls.a, target)
        target.g = types.MethodType(cls.g, target)
        target.add_group = types.MethodType(cls.add_group, target)
        target.add_mutex_group = types.MethodType(cls.add_mutex_group, target)
        target.add_mutex_switch = types.MethodType(cls.add_mutex_switch, target)

        return target

    def __init__(self, *args, allow_config=False, config_path_base=True,
                 **kwargs):
        super(ArgParser, self).__init__(*args, fromfile_prefix_chars="@",
                                        **kwargs)

        self.a = types.MethodType(
            functools.update_wrapper(ArgParser.a, ArgParser.add),
            self)
        self.g = types.MethodType(
            functools.update_wrapper(ArgParser.g, ArgParser.add_argument_group),
            self)
        self.add_group = types.MethodType(
            functools.update_wrapper(ArgParser.add_group,
                                     ArgParser.add_argument_group),
            self)
        self.add_mutex_group = types.MethodType(
            functools.update_wrapper(ArgParser.add_mutex_group,
                                     ArgParser.add_mutually_exclusive_group),
            self)

        self.config_path_base = config_path_base

        if allow_config:
            self.add("--config", is_config_file=True)

    def a(self, *args, **kwargs):
        return self.add(*args, **kwargs)

    def g(self, *args, **kwargs):
        return self.add_group(*args, **kwargs)

    def add_group(self, *args, **kwargs):
        return self.add_argument_group(*args, **kwargs)

    def add_argument_group(self, *args, **kwargs):
        group = super(ArgParser, self).add_argument_group(*args, **kwargs)
        group = self.attach_methods(group)

        return group

    def add_mutex_group(self):
        return self.add_mutually_exclusive_group()

    def add_mutex_switch(parser, dest, arguments=set(), default=None,
                         single_arg=False, required=False):
        """Adds mutually exclusive switch arguments.

        Args:
            arguments: a dictionary that maps switch name to helper text. Use
                sets to skip help texts.
        """

        if default is not None:
            assert default in arguments

        if isinstance(arguments, set):
            arguments = {k: None for k in arguments}

        if not single_arg:
            mg = parser.add_mutually_exclusive_group(required=required)

            for name, help_text in arguments.items():
                kwargs = {
                    "action": "store_const",
                    "dest": dest,
                    "const": name,
                    "help": help_text
                }

                if default == name:
                    kwargs["default"] = name

                mg.add_argument("--{}".format(name), **kwargs)

            return mg
        else:
            kwargs = {
                "dest": dest,
                "type": str,
                "default": default,
                "help": "\n".join("{}: {}".format(k, v)
                                  for k, v in arguments.items()),
                "choices": list(arguments.keys())
            }

            return parser.add_argument("--{}".format(dest), **kwargs)

    def _resolve_relative_path(self, args, base_path):
        for action in self._actions:
            if action.type != path:
                continue

            dest = action.dest
            arg_val = getattr(args, dest, None)

            if arg_val is None:
                continue

            def _resolve(path):
                if not os.path.isabs(path):
                    return os.path.join(base_path, path)

                return path

            if isinstance(arg_val, list):
                new_val = [_resolve(v) for v in arg_val]
            else:
                new_val = _resolve(arg_val)

            setattr(args, dest, new_val)

    def parse_args(self, *parsed_args, **kwargs):
        parsed_args = super(ArgParser, self).parse_args(*parsed_args, **kwargs)

        if hasattr(parsed_args, "config") and parsed_args.config is not None \
                and self.config_path_base:
            config_path = os.path.abspath(parsed_args.config)
            work_path = os.path.dirname(config_path)
        else:
            work_path = os.getcwd()

        self._resolve_relative_path(parsed_args, work_path)

        return parsed_args

    def __str__(self):
        return "\n".join(["{}: {}".format(k, v) for k, v in vars()])