"""Defines the Opt class (main interface)."""

from copy import copy

from lethargy.errors import ArgsError, MissingOption, TransformError
from lethargy.util import argv, falsylist, identity, is_greedy, stab


class Opt:
    """Define an option to take it from a list of arguments."""

    def __init__(self, *names: str):
        self._names = {stab(name) for name in names}
        self._argc = 0  # Usually int, but can also be Ellipsis (greedy)
        self._tfm = identity

    def __copy__(self):
        new = self.__class__()
        new._names = copy(self._names)
        new._argc = self._argc
        new._tfm = self._tfm
        return new

    def __str__(self):
        if not self._names:
            return ""

        names = "|".join(sorted(sorted(self._names), key=len))

        if not isinstance(self._tfm, type):
            metavar = "value"
        else:
            metavar = self._tfm.__name__.lower()

        if is_greedy(self._argc):
            hint = f"[{metavar}]..."
        elif self._argc > 0:
            hint = " ".join([f"<{metavar}>"] * self._argc)
        else:
            return names

        return f"{names} {hint}"

    def __repr__(self):
        repr_str = ""

        # Opt(<names>)
        qname = self.__class__.__qualname__
        mapped = [repr(name) for name in self._names]
        names = ", ".join(mapped)
        repr_str += f"{qname}({names})"

        # [.takes(<n>[, <tfm>])]
        # This whole thing is optional, if there's nothing to show it won't
        # be in the repr string.
        if self._argc:
            takes = [self._argc]
            if self._tfm is not identity:
                if isinstance(self._tfm, type):
                    takes.append(self._tfm.__name__)
                else:
                    takes.append(repr(self._tfm))
            repr_str += ".takes({})".format(", ".join(map(str, takes)))

        # at <ID>
        repr_str += f" at {hex(id(self))}"

        return f"<{repr_str}>"

    def __eq__(self, other):
        try:
            return (
                self._names == other._names
                and self._argc == other._argc
                and self._tfm == other._tfm
            )
        except AttributeError:
            return NotImplemented

    def _find_in(self, args):
        """Search args for this option and return an index if it's found."""
        for name in self._names:
            try:
                return args.index(name)
            except ValueError:
                continue
        return None

    def takes(self, n, tfm=None):
        """Set the number of arguments and optional transformation for each."""
        if not is_greedy(n) and n < 1:
            msg = f"The number of arguments ({n}) must be >1 or greedy (``...``)"
            raise ValueError(msg)

        self._argc = n
        if tfm is not None:
            self._tfm = tfm

        return self

    def take_flag(self, args=argv, *, mut=True):
        """Get a bool indicating whether the option was present in the arguments."""
        idx = self._find_in(args)

        if idx is None:
            return False

        if mut:
            del args[idx]

        return True

    def take_args(self, args=argv, *, raises=False, mut=True, d=None):
        """Get the values of this option."""
        argc = self._argc

        # Taking less than 1 argument will do nothing, use take_flag instead.
        # Assume argc is numeric if it's not greedy.
        if not is_greedy(argc) and argc < 1:
            s = "s" if argc != 1 else ""
            n = "no" if argc == 0 else argc
            msg = f"'{self}' takes {n} argument{s} (did you mean to use `take_flag`?)"
            raise ArgsError(msg)

        # Is this option in the list?
        index = self._find_in(args)

        # Return early if the option isn't present.
        if index is None:
            if raises:
                msg = f"Missing required option '{self}'"
                raise MissingOption(msg)

            if is_greedy(argc):
                return falsylist() if d is None else d

            if d is None and argc != 1:
                return falsylist([None] * argc)

            # `if d is None and argc == 1` should return None anyway. As long
            # as d is None by default then this always returns correctly.
            return d

        # Start index is now set, find the index of the *final* value.
        if is_greedy(argc):
            end_idx = len(args)
        else:
            # Start index is the option name, add 1 to compensate.
            end_idx = index + argc + 1

            # Fail fast if the option expects more arguments than it has.
            if end_idx > len(args):
                # Highest index (length - 1) minus this option's index.
                actual = len(args) - 1 - index
                n = actual or "none"
                s = "s" if argc != 1 else ""
                msg = f"Expected {argc} argument{s} for option '{self}', but found {n}"
                if actual:
                    present_args = ", ".join(map(repr, args[index + 1 : end_idx]))
                    msg += f" ({present_args})"
                raise ArgsError(msg)

        # Get the list of values starting from the first value to the option.
        taken = args[index + 1 : end_idx]

        # Remove the option and its associated values from the list.
        if mut:
            del args[index:end_idx]

        # Single return value keeps the unpacking usage pattern consistent.
        if argc == 1:
            return self._transform(taken[0])

        # Return a list of transformed values.
        return [self._transform(x) for x in taken]

    def _transform(self, value):
        """Call _tfm on a string and return the result, or raise an exception union."""
        try:
            return self._tfm(value)

        except Exception as exc:
            message = f"Option '{self}' received an invalid value: {value!r}"

            # The exception needs to be a subclass of both the raised exception
            # and TransformError. This allows manually handling specific
            # exception types, _and_ automatically handling any exceptions that
            # get raised during transformation.
            name = f"<TransformError | {exc.__class__.__name__}>"
            bases = (exc.__class__, TransformError)
            new_exc = type(name, bases, {})

            raise new_exc(message) from exc


def take_opt(name, number=None, call=None, *, args=argv, required=False, mut=True):
    """Quickly take an option as flag, or with some arguments."""
    names = [name] if isinstance(name, str) else name
    opt = Opt(*names)
    if not number:
        return opt.take_flag(args, mut=mut)
    return opt.takes(number, call).take_args(args, raises=required, mut=mut)
