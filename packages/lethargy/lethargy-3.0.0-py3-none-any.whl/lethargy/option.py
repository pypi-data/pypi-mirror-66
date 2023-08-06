"""Defines the Opt class (main interface)."""

from lethargy.errors import ArgsError, MissingOption, TransformError
from lethargy.util import argv, falsylist, identity, is_greedy, tryposixname


class Option:
    """Define an option to take it from a list of arguments."""

    def __init__(self, name, number=0, tfm=None):
        self.names = set(map(tryposixname, [name] if isinstance(name, str) else name))
        self.argc = number  # Invalid values are handled by the setter.
        self.tfm = tfm or identity

    def __str__(self):
        if not self.names:
            return ""

        names = "|".join(sorted(sorted(self.names), key=len))

        if not isinstance(self.tfm, type):
            metavar = "value"
        else:
            metavar = self.tfm.__name__.lower()

        if is_greedy(self.argc):
            args = f"[{metavar}]..."
        elif self.argc > 0:
            args = " ".join([f"<{metavar}>"] * self.argc)
        else:
            return names

        return f"{names} {args}"

    def __repr__(self):
        repr_str = ""

        # Option(<names>)
        qname = type(self).__qualname__
        mapped = [repr(name) for name in self.names]
        names = ", ".join(mapped)
        repr_str += f"{qname}({names})"

        # [.takes(<n>[, <tfm>])]
        # This whole thing is optional. If there's nothing
        # to show, it won't be in the final string.
        if self.argc:
            takes = [self.argc]
            if self.tfm is not identity:
                if isinstance(self.tfm, type):
                    takes.append(self.tfm.__name__)
                else:
                    takes.append(repr(self.tfm))
            repr_str += ".takes({})".format(", ".join(map(str, takes)))

        # at <ID>
        repr_str += f" at {hex(id(self))}"

        return f"<{repr_str}>"

    @property
    def argc(self):
        """Get the number of arguments this option takes."""
        return self._argc

    @argc.setter
    def argc(self, value):
        if not is_greedy(value) and value < 0:
            msg = f"The number of arguments ({value}) must be >1 or greedy (``...``)"
            raise ValueError(msg)
        self._argc = value

    def find_in(self, args):
        """Search args for this option and return an index if it's found."""
        for name in self.names:
            try:
                return args.index(name)
            except ValueError:
                continue
        return None

    def take_flag(self, args=argv, *, mut=True):
        """Get a bool indicating whether the option was present in the arguments."""
        index = self.find_in(args)

        if index is None:
            return False

        if mut:
            del args[index]

        return True

    def take_args(self, args=argv, *, required=False, mut=True):
        """Get the values of this option."""
        argc = self.argc

        if not argc:
            msg = f"'{self}' takes no arguments (did you mean to use `take_flag`?)"
            raise RuntimeError(msg)

        # Is this option in the list?
        index = self.find_in(args)

        # Return early if the option isn't present.
        if index is None:
            if required:
                msg = f"Missing required option '{self}'"
                raise MissingOption(msg)

            if is_greedy(argc):
                return falsylist()

            if argc != 1:
                return falsylist([None] * argc)

            return None

        # Start index is now set, find the index of the *final* value.
        if is_greedy(argc):
            end_idx = None
        else:
            # Start index is the option name, add 1 to compensate.
            end_idx = index + argc + 1

            # Fail fast if the option expects more arguments than it has.
            if end_idx > len(args):
                # Highest index (length - 1) minus this option's index.
                number_found = len(args) - 1 - index
                n = number_found or "none"
                s = "s" if argc != 1 else ""
                msg = f"Expected {argc} argument{s} for option '{self}', but found {n}"
                if number_found:
                    given = ", ".join(map(repr, args[index + 1 : end_idx]))
                    msg += f" ({given})"
                raise ArgsError(msg)

        # Get the list of values starting from the first value to the option.
        taken = args[index + 1 : end_idx]

        # Remove the option and its associated values from the list.
        if mut:
            del args[index:end_idx]

        # Single return value keeps the unpacking usage pattern consistent.
        if argc == 1:
            return self.transform(taken[0])

        # Return a list of transformed values.
        return [self.transform(x) for x in taken]

    def transform(self, value):
        """Call _tfm on a string and return the result, or raise an exception union."""
        try:
            return self.tfm(value)

        except Exception as exc:
            message = f"Option '{self}' received an invalid value: {value!r}"

            # The exception needs to be a subclass of both the raised exception
            # and TransformError. This allows manually handling specific
            # exception types, _and_ automatically handling all exceptions that
            # get raised during transformation.
            name = f"TransformError[{type(exc).__name__}]"
            bases = (TransformError, type(exc))
            new_exc = type(name, bases, {})

            raise new_exc(message) from exc


def take_opt(name, number=None, call=None, *, args=argv, required=False, mut=True):
    """Quickly take an option as flag, or with some arguments if also given a number."""
    if not number:
        return Option(name).take_flag(args, mut=mut)

    opt = Option(name, number, call)

    return opt.take_args(args, required=required, mut=mut)
