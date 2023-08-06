"""
The SI Units: "For all people, for all time"

A module to model the seven SI base units:

                    kg

            cd               m


                    SI
         mol                    s



               K           A

  ...and other derived and non-SI units for practical calculations.
"""


import functools
import json
import re
import itertools
import operator
import inspect
from collections import ChainMap
import copy
from typing import NamedTuple, Union, Tuple, List, Any, Optional, Callable
try:
    import tuplevector as vec
except ModuleNotFoundError:
    from forallpeople import tuplevector as vec


# TODO: Implement __format__ for formatting results directly
# TODO: Implement establish_context() and context_established: bool()
# create the context for the __repr__ and using .prefixed
# change all visible properties to no underscore
# create context properties that all have underscores
# Use establish context when using __repr__ for first time and addition/sub (with prefixed)

NUMBER = (int, float)


class Dimensions(NamedTuple):
    kg: float
    m: float
    s: float
    A: float
    cd: float
    K: float
    mol: float


# The single class to describe all units...Physical (as in "a physical property")
class Physical(object):
    """
    A class that defines any physical quantity that can be described
    within the BIPM SI unit system.
    """

    _prefixes = {
        "Y": 1e24,
        "Z": 1e21,
        "E": 1e18,
        "P": 1e15,
        "T": 1e12,
        "G": 1e09,
        "M": 1e06,
        "k": 1e03,
        "": 1.0,
        "m": 1e-3,
        "μ": 1e-6,
        "n": 1e-09,
        "p": 1e-12,
        "f": 1e-15,
        "a": 1e-18,
        "z": 1e-21,
        "y": 1e-24,
    }

    _superscripts = {
        "1": "¹",
        "2": "²",
        "3": "³",
        "4": "⁴",
        "5": "⁵",
        "6": "⁶",
        "7": "⁷",
        "8": "⁸",
        "9": "⁹",
        "0": "⁰",
        "-": "⁻",
        ".": "'",
    }
    _eps = 1e-7
    _total_precision = 6

    __slots__ = ("value", "dimensions", "factor", "precision", "_prefixed")

    def __init__(
        self,
        value: Union[int, float],
        dimensions: Dimensions,
        factor: float,
        precision: int = 3,
        prefixed: str = "",
    ):
        """Constructor"""
        super(Physical, self).__setattr__("value", value)
        super(Physical, self).__setattr__("dimensions", dimensions)
        super(Physical, self).__setattr__("factor", factor)
        super(Physical, self).__setattr__("precision", precision)
        super(Physical, self).__setattr__("_prefixed", prefixed)

    def __setattr__(self, _, __):
        raise AttributeError("Cannot set attribute.")

    ### API Methods ###
    @property
    def latex(self) -> str:
        return self._repr_latex_()

    @property
    def html(self) -> str:
        return self._repr_html_()

    def prefixed(self, prefixed: str = ""):
        """
        Return a Physical instance with 'prefixed' property set to 'prefix'
        """
        if self.factor != 1:
            raise AttributeError("Cannot prefix a Physical if it has a factor.")
        # check if elligible for prefixing; do not rely on __repr__ to ignore it
        return Physical(
            self.value, self.dimensions, self.factor, self.precision, prefixed
        )

    @property
    def repr(self) -> str:
        """
        Returns a repr that can be used to create another Physical instance.
        """
        repr_str = (
            "Physical(value={}, dimensions={}, factor={}, precision={}, _prefixed={})"
        )
        return repr_str.format(
            self.value, self.dimensions, self.factor, self.precision, self._prefixed
        )  # check

    def round(self, n: int):
        """
        Returns a new Physical with a new precision, 'n'. Precision controls
        the number of decimal places displayed in repr and str.
        """
        return Physical(self.value, self.dimensions, self.factor, n, self._prefixed)

    def split(self, base_value: bool = True) -> tuple:
        """
        Returns a tuple separating the value of `self` with the units of `self`.
        If base_value is True, then the value will be the value in base units. If False, then
        the apparent value of `self` will be used.

        This method is to allow flexibility in working with Physical instances when working
        with numerically optimized libraries such as numpy which cannot accept non-numerical
        objects in some of their operations (such as in matrix inversion).
        """
        if base_value:
            return (
                self.value * self.factor,
                Physical(1 / self.factor, self.dimensions, self.factor, self.precision),
            )
        return (float(self), Physical(1, self.dimensions, self.factor, self.precision))

    def sqrt(self, n: float = 2.0):
        """
        Returns a Physical instance that represents the square root of `self`.
        `n` can be set to an alternate number to compute an alternate root (e.g. 3.0 for cube root)
        """
        return self ** (1 / n)

    def in_units(self, unit_name=""):
        """
        Returns None and alters the instance into one of the elligible
        alternative units for its dimension, if it exists in the alternative_units dict;
        """
        dims = self.dimensions
        env_dims = environment.units_by_dimension
        derived = env_dims["derived"]
        defined = env_dims["defined"]
        power, dims_orig = Physical._powers_of_derived(dims, env_dims)
        if not unit_name:
            print("Available units: ")
            for key in derived.get(dims_orig, {}):
                print(key)
            for key in defined.get(dims_orig, {}):
                print(key)

        if unit_name:
            defined_match = defined.get(dims_orig, {}).get(unit_name, {})
            derived_match = derived.get(dims_orig, {}).get(unit_name, {})
            unit_match = defined_match or derived_match
            new_factor = unit_match.get("Factor", 1) ** power
            return Physical(self.value, self.dimensions, new_factor, self.precision)

    def si(self):
        """
        Return a new Physical instance with self.factor set to 1, thereby returning
        the instance to SI units display.
        """
        return Physical(self.value, self.dimensions, 1, self._precision)

    ### repr Methods (the "workhorse" of Physical) ###

    def __repr__(self):
        return self._repr_template_()

    def _repr_html_(self):
        return self._repr_template_(template="html")

    def _repr_markdown_(self):
        return self._repr_template_(template="html")

    def _repr_latex_(self):
        return self._repr_template_(template="latex")

    def _repr_template_(self, template: str = "") -> str:
        """
        Returns a string that appropriately represents the Physical
        instance. The parameter,'template', allows two optional values:
        'html' and 'latex'. which will only be utilized if the Physical
        exists in the Jupyter/iPython environment.
        """
        # Access req'd attributes
        precision = self.precision
        dims = self.dimensions
        factor = self.factor
        val = self.value
        prefix = ""
        prefixed = self._prefixed
        eps = self._eps

        # Access external environment
        env_fact = environment.units_by_factor or dict()
        env_dims = environment.units_by_dimension or dict()

        # Do the expensive vector math method (call once, only)
        power, dims_orig = Physical._powers_of_derived(dims, env_dims)

        # Determine if there is a symbol for these dimensions in the environment
        # and if the quantity is elligible to be prefixed
        symbol, prefix_bool = Physical._evaluate_dims_and_factor(
            dims_orig, factor, power, env_fact, env_dims
        )
        # Get the appropriate prefix
        if prefix_bool and prefixed:
            prefix = prefixed
        elif prefix_bool and dims_orig == Dimensions(1, 0, 0, 0, 0, 0, 0):
            prefix = Physical._auto_prefix(val, power, kg=True)
        elif prefix_bool:
            prefix = Physical._auto_prefix(val, power, kg=False)

        # Format the exponent (may not be used, though)
        exponent = Physical._format_exponent(power, repr_format=template, eps=eps)

        # Format the units
        if not symbol and Physical._dims_basis_multiple(dims):
            components = Physical._get_unit_components_from_dims(dims)
            units_symbol = Physical._get_unit_string(components, repr_format=template)
            units = units_symbol
            units = Physical._format_symbol(prefix, units_symbol, repr_format=template)
            exponent = ""
        elif not symbol:
            components = Physical._get_unit_components_from_dims(dims)
            units_symbol = Physical._get_unit_string(components, repr_format=template)
            units = units_symbol
            exponent = ""
        else:
            units = Physical._format_symbol(prefix, symbol, repr_format=template)

        # Determine the appropriate display value
        value = val * factor

        if prefix_bool:
            # If the quantity has a "pre-fixed" prefix, it will override
            # the value generated in _auto_prefix_value
            if dims_orig == Dimensions(1, 0, 0, 0, 0, 0, 0):
                value = Physical._auto_prefix_value(val, power, prefixed, kg=True)
            else:
                value = Physical._auto_prefix_value(val, power, prefixed)

        pre_super = ""
        post_super = ""
        space = " "
        if template == "latex":
            space = r"\ "
            pre_super = "^{"
            post_super = "}"
        elif template == "html":
            space = " "
            pre_super = "<sup>"
            post_super = "</sup>"

        if not exponent:
            pre_super = ""
            post_super = ""

        return f"{value:.{precision}f}{space}{units}{pre_super}{exponent}{post_super}"

    #    def __str__(self):
    #        return repr(self)

    ### Helper methods for repr methods ###

    @staticmethod
    def _evaluate_dims_and_factor(
        dims_orig: Dimensions,
        factor: Union[int, float],
        power: Union[int, float],
        env_fact: dict,
        env_dims: dict,
    ) -> tuple:
        """Part of the __str__ and __repr__ process.
	    Returns a tuple containing the
        appropriate symbol as a string (if applicable; '' if not) and a
        boolean indicating whether or not the dimension and factor combination
        is elligible for a prefix."""
        defined = Physical._get_units_by_factor(
            factor=factor, dims=dims_orig, units_env=env_fact, power=power
        )
        derived = Physical._get_derived_unit(dims=dims_orig, units_env=env_dims)
        single_dim = Physical._dims_basis_multiple(dims_orig)
        if defined:
            units_match = defined
            prefix_bool = False
        elif derived or single_dim:
            units_match = derived
            prefix_bool = True
        else:
            units_match = derived
            prefix_bool = False

        if units_match:
            name = tuple(units_match.keys())[0]
            symbol = units_match.get(name, {}).get("Symbol", "")
            symbol = symbol or name
        else:
            symbol = ""
        return (symbol, prefix_bool)

    @staticmethod
    # @functools.lru_cache(maxsize=None) #Not possible to use LRU cache here?
    def _get_units_by_factor(
        factor: float, dims: Dimensions, units_env: dict, power: Union[int, float]
    ) -> dict:
        """
        Returns a units_dict from the environment instance if the numerical
        value of 'factor' is a match for a derived unit defined in the
        environment instance and the dimensions stored in the units_dict are
        equal to 'dims'. Returns an empty dict, otherwise.
        """
        new_factor = factor ** (1 / power)
        units_match = units_env.get(
            round(new_factor, Physical._total_precision), dict()
        )
        try:
            units_name = tuple(units_match.keys())[0]
        except IndexError:
            units_name = ""
        retrieved_dims = units_match.get(units_name, dict()).get("Dimension", dict())
        if dims != retrieved_dims:
            return dict()
        return units_match

    @staticmethod
    def _get_derived_unit(dims: Dimensions, units_env: dict) -> dict:
        """
        Returns a units definition dict that matches 'dimensions'.
        If 'dimensions' is a derived unit raised to a power (e.g. N**2),
        then its original dimensions are checked instead of the altered ones.
        Returns {} if no unit definition matches 'dimensions'.
        """
        derived_units = units_env.get("derived")
        return derived_units.get(dims, dict())

    @staticmethod
    def _get_unit_string(unit_components: list, repr_format: str) -> str:
        """
        Part of the __str__ and __repr__ process. Returns a string representing
        the SI unit components of the Physical instance extracted from the list of
        tuples, 'unit_components', using 'repr_format' as given by the _repr_x_
        function it was called by. If 'repr_format' is not given, then terminal
        output is assumed.
        """
        dot_operator = "·"  # new: · , # old: ⋅
        pre_super = ""
        post_super = ""
        pre_symbol = ""
        post_symbol = ""
        if repr_format == "html":
            dot_operator = "&#8901;"  # &#183;
            pre_super = "<sup>"
            post_super = "</sup>"
        elif repr_format == "latex":
            dot_operator = r" \cdot "
            pre_symbol = "\\text{"
            post_symbol = "}"
            pre_super = "^{"
            post_super = "}"

        str_components = []
        kg_only = ""
        for symbol, exponent in unit_components:
            if exponent:
                kg_only = symbol
            if exponent == 1:
                this_component = f"{pre_symbol}{symbol}{post_symbol}"
            else:
                if not repr_format:
                    exponent = Physical._get_superscript_string(str(exponent))
                this_component = (
                    f"{pre_symbol}{symbol}{post_symbol}"
                    f"{pre_super}{exponent}{post_super}"
                )
            str_components.append(this_component)
        if kg_only == "kg":  # Hack for lone special case of a kg only Physical
            return dot_operator.join(str_components).replace("kg", "g")
        return dot_operator.join(str_components)

    @staticmethod
    def _get_unit_components_from_dims(dims: Dimensions):
        """
        Returns a list of tuples to represent the current units based
        on the current dimensions. Dimension ignored if 0.
        e.g. [('kg', 1), ('m', -1), ('s', -2)]
        """
        unit_components = []
        unit_symbols = dims._fields
        for idx, dim in enumerate(dims):
            if dim:  # int
                unit_tuple = (unit_symbols[idx], dim)
                unit_components.append(unit_tuple)
        return unit_components

    @staticmethod
    def _format_symbol(prefix: str, symbol: str, repr_format: str = "") -> str:
        """
        Returns 'symbol' formatted appropriately for the 'repr_format' output.
        """
        # if r"\text" or "^" in symbol: # in case pre-formatted latex from unit_string
        #    return symbol
        symbol_string_open = ""
        symbol_string_close = ""
        dot_operator = "·"
        ohm = "Ω"
        if repr_format == "html":
            dot_operator = "&#8901;"
            ohm = "&#0937;"
        elif repr_format == "latex":
            dot_operator = r" \cdot "
            ohm = r"\Omega"
            symbol_string_open = "\\text{"
            symbol_string_close = "}"

        symbol = (
            symbol.replace("·", symbol_string_close + dot_operator + symbol_string_open)
            .replace("*", symbol_string_close + dot_operator + symbol_string_open)
            .replace("Ω", ohm)
        )
        formatted_symbol = f"{symbol_string_open}{prefix}{symbol}{symbol_string_close}"
        if symbol.startswith(
            "\\text{"
        ):  # special case for 'single dimension' Physicals...
            formatted_symbol = f"{symbol[0:7]}{prefix}{symbol[7:]}"
        return formatted_symbol

    @staticmethod
    def _format_exponent(
        power: Union[int, float], repr_format: str = "", eps: float = 1e-7
    ) -> str:
        """
        Returns the number in 'power' as a formatted exponent for text display.
        """
        if power == 1:
            return ""

        if abs((abs(power) - round(abs(power)))) <= eps:
            power = int(round(power))
        exponent = str(power)
        if not repr_format:
            exponent = Physical._get_superscript_string(exponent)
        return exponent

    @staticmethod
    def _get_superscript_string(exponent: str) -> str:
        """Part of the __str__ and __repr__ process. Returns the unicode
        "superscript" equivalent string for a given float."""
        exponent_components = list(exponent)
        exponent_string = ""
        for component in exponent_components:
            exponent_string += Physical._superscripts[component]
        return exponent_string

    ### Mathematical helper functions ###
    @staticmethod
    def _powers_of_derived(dims: Dimensions, units_env: dict) -> Union[int, float]:
        """
        Returns an integer value that represents the exponent of a unit if the
        dimensions
        array is a multiple of one of the defined derived units in dimension_keys.
        Returns None,
        otherwise.
        e.g. a force would have dimensions = [1,1,-2,0,0,0,0] so a Physical object
        that had dimensions = [2,2,-4,0,0,0,0] would really be a force to the power of
        2.
        This function returns the 2, stating that `dims` is the second power of a
        derived dimension in `units_env`.
        """
        quotient_1 = Physical._dims_quotient(dims, units_env)
        quotient_2 = Physical._dims_basis_multiple(dims)
        if quotient_1 is not None:
            power_of_derived = vec.mean(quotient_1, ignore_empty=True)
            base_dimensions = vec.divide(dims, quotient_1, ignore_zeros=True)
            return ((power_of_derived or 1), base_dimensions)
        elif quotient_2 is not None:
            power_of_basis = vec.mean(quotient_2, ignore_empty=True)
            base_dimensions = vec.divide(dims, quotient_2, ignore_zeros=True)
            return ((power_of_basis or 1), base_dimensions)
        else:
            return (1, dims)

    @staticmethod
    def _dims_quotient(dimensions: Dimensions, units_env: dict) -> Optional[Dimensions]:
        """
        Returns a Dimensions object representing the element-wise quotient between
        'dimensions' and a defined unit if 'dimensions' is a scalar multiple
        of a defined unit in the global environment variable.
        Returns None otherwise.
        """
        derived = units_env["derived"]
        defined = units_env["defined"]
        all_units = ChainMap(defined, derived)
        for dimension_key in all_units.keys():
            if Physical._check_dims_parallel(dimension_key, dimensions):
                quotient = vec.divide(dimensions, dimension_key, ignore_zeros=True)
                return quotient
        return None

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def _check_dims_parallel(d1: Dimensions, d2: Dimensions) -> bool:
        """
        Returns True if d1 and d2 are parallel vectors. False otherwise.
        """
        return vec.multiply(d1, vec.dot(d2, d2)) == vec.multiply(d2, vec.dot(d1, d2))

    @staticmethod
    def _dims_basis_multiple(dims: Dimensions) -> Optional[Dimensions]:
        """
        Returns `dims` if `dims` is a scalar multiple of one of the basis vectors.
        Returns None, otherwise.
        This is used as a check to see if `dims` contains only a single dimension,
        even if that single dimension is to a higher power.
        e.g.
        if `dims` equals Dimensions(2, 0, 0, 0, 0, 0, 0) then `dims` will be
        returned.
        if `dims` equals Dimensions(0, 1, 1, 0, 0, 0, 0) then None will be returned.
        if `dims` equals Dimensions(0, 14, 0, 0, 0, 0, 0) then `dims` will be returned.
        """
        count = 0
        for dim in dims:
            if dim:
                count += 1
            if count > 1:
                return None
        return dims

    @staticmethod
    def _auto_prefix(value: float, power: Union[int, float], kg: bool = False) -> str:
        """
        Returns a string "prefix" of an appropriate value if self.value should be prefixed
        i.e. it is a big enough number (e.g. 5342 >= 1000; returns "k" for "kilo")
        """
        kg_factor = 1
        if kg:
            kg_factor = 1000
        prefixes = Physical._prefixes
        if abs(value) >= 1:
            for prefix, power_of_ten in prefixes.items():
                if abs(value) >= (power_of_ten / kg_factor) ** abs(power):
                    return prefix
        else:
            reverse_prefixes = sorted(prefixes.items(), key=lambda prefix: prefix[0])
            # Get the smallest prefix to start...
            previous_prefix = reverse_prefixes[0][0]
            for prefix, power_of_ten in reversed(list(prefixes.items())):
                if abs(value) < (power_of_ten / kg_factor) ** abs(power):
                    return previous_prefix
                else:
                    previous_prefix = prefix

    @staticmethod
    def _auto_prefix_kg(value: float, power: Union[int, float]) -> str:
        """
        Just like _auto_prefix but handles the one special case for "kg" because it already
        has a prefix of "k" as an SI base unit. The difference is the comparison of
        'power_of_ten'/1000 vs 'power_of_ten'.
        """
        prefixes = Physical._prefixes
        if abs(value) >= 1:
            for prefix, power_of_ten in prefixes.items():
                if abs(value) >= (power_of_ten / 1000) ** abs(power):
                    return prefix
        else:
            reverse_prefixes = sorted(prefixes.items(), key=lambda prefix: prefix[0])
            # Get the smallest prefix to start...
            previous_prefix = reverse_prefixes[0][0]
            for prefix, power_of_ten in reversed(list(prefixes.items())):
                if abs(value) < (power_of_ten / 1000) ** abs(power):
                    return previous_prefix
                else:
                    previous_prefix = prefix

    @staticmethod
    def _auto_prefix_value(
        value: float, power: Union[int, float], prefixed: str = "", kg: bool = False,
    ) -> float:
        """
        Converts the value to a prefixed value if the instance has a symbol defined in
        the environment (i.e. is in the defined units dict)
        """
        kg_factor = 1
        if kg:
            kg_factor = 1000
        prefixes = Physical._prefixes
        if prefixed:
            return value / ((prefixes[prefixed] / kg_factor) ** power)
        if abs(value) >= 1:
            for prefix, power_of_ten in prefixes.items():
                if abs(value) >= (power_of_ten / kg_factor) ** abs(power):
                    return value / ((power_of_ten / kg_factor) ** power)
        else:
            reverse_prefixes = sorted(
                prefixes.items(), key=lambda pre_fact: pre_fact[1]
            )
            # Get the smallest factor to start...
            previous_power_of_ten = reverse_prefixes[0][1]
            for prefix, power_of_ten in reversed(list(prefixes.items())):
                if abs(value) < (power_of_ten / kg_factor) ** abs(power):
                    return value / ((previous_power_of_ten / kg_factor) ** abs(power))
                else:
                    previous_power_of_ten = power_of_ten
    

    def test_for_array(self, other: Any) -> bool:
        """
        Returns True if other has attributes and methods indicative of
        an "array"-type of container, e.g. numpy.ndarray or pandas.Series,
        or pandas.DataFrame. Tests if other has the attribute '.shape'
        and if it is subscriptable (accessible by numerical index).
        """
        if hasattr(other, "shape"):
            if hasattr(other, "__getitem__"):
                return True
            elif hasattr(other, "iloc"):
                return True
        return False

    def _element_wise_ops(self, other: Any, method: Callable) -> Any:
        """
        Returns the element wise operation of 'method' on 'other'
        (an array type) with 'self'.
        """
        shape = other.shape
        new_other = copy.copy(other)
        has_iloc = hasattr(other, "iloc")
        print("runs")
        if len(shape) == 1:
            for x in range(shape[0]):
                    if has_iloc:
                        new_other.iloc[x] = method(other.iloc[x])
                    else:
                        new_other[x] = method(other[x])
        elif len(shape) == 2:
            for x in range(shape[0]):
                for y in range(shape[1]):
                    print(other[x][y])
                    if has_iloc:
                        new_other.iloc[x, y] = method(other.iloc[x,y])
                    else:
                        print(method)
                        new_other[x][y] = method(other[x][y])
        return new_other

        

 
    ### "Magic" Methods ###

    def __float__(self):
        value = self.value
        dims = self.dimensions
        factor = self.factor
        prefixed = self._prefixed
        env_dims = environment.units_by_dimension or dict()
        power, _ = Physical._powers_of_derived(dims, env_dims)
        if factor != 1:
            float_value = value * factor
        else:
            float_value = Physical._auto_prefix_value(value, power, prefixed)
        return float(float_value)

    def __int__(self):
        return int(float(self))

    def __neg__(self):
        return self * -1

    def __abs__(self):
        if self.value < 0:
            return self * -1
        return self

    def __bool__(self):
        return True

    # def __format__(self, fmt_spec = ''): # format for a custom vector2d class; how to implement on top of _repr_template_?
    #     components = (format(c, fmt_spec) for c in self)
    #     return '({}, {})'.format(*components)

    def __hash__(self):
        return hash(
            (self.value, self.dimensions, self.factor, self.precision, self._prefixed)
        )

    def __round__(self, n=0):
        return self.round(n)

    def __contains__(self, other):
        return False

    def __eq__(self, other):
        if isinstance(other, NUMBER):
            return round(self.value, Physical._total_precision) == other
        elif type(other) == str:
            return False
        elif isinstance(other, Physical) and self.dimensions == other.dimensions:
            return round(self.value, Physical._total_precision) == round(
                other.value, Physical._total_precision
            )
        else:
            raise ValueError(
                "Can only compare between Physical instances of equal dimension."
            )

    def __gt__(self, other):
        if isinstance(other, NUMBER):
            return round(self.value, Physical._total_precision) > other
        elif isinstance(other, Physical) and self.dimensions == other.dimensions:
            return round(self.value, Physical._total_precision) > round(
                other.value, Physical._total_precision
            )
        else:
            raise ValueError(
                "Can only compare between Physical instances of equal dimension."
            )

    def __ge__(self, other):
        if isinstance(other, NUMBER):
            return round(self.value, Physical._total_precision) >= other
        elif isinstance(other, Physical) and self.dimensions == other.dimensions:
            return round(self.value, Physical._total_precision) >= round(
                other.value, Physical._total_precision
            )
        else:
            raise ValueError(
                "Can only compare between Physical instances of equal dimension."
            )

    def __lt__(self, other):
        if isinstance(other, NUMBER):
            return round(self.value, Physical._total_precision) < other
        elif isinstance(other, Physical) and self.dimensions == other.dimensions:
            return round(self.value, Physical._total_precision) < round(
                other.value, Physical._total_precision
            )
        else:
            raise ValueError(
                "Can only compare between Physical instances of equal dimension."
            )

    def __le__(self, other):
        if isinstance(other, NUMBER):
            return round(self.value, Physical._total_precision) <= other
        elif isinstance(other, Physical) and self.dimensions == other.dimensions:
            return round(self.value, Physical._total_precision) <= round(
                other.value, Physical._total_precision
            )
        else:
            raise ValueError(
                "Can only compare between Physical instances of equal dimension."
            )

    def __add__(self, other):
            
        if isinstance(other, Physical):
            if self.dimensions == other.dimensions:
                try:
                    return Physical(
                        self.value + other.value,
                        self.dimensions,
                        self.factor,
                        self.precision,
                        self._prefixed,
                    )
                except:
                    raise ValueError(
                        f"Cannot add between {self} and {other}: "
                        + ".value attributes are incompatible."
                    )
            else:
                raise ValueError(
                    f"Cannot add between {self} and {other}: "
                    + ".dimensions attributes are incompatible (not equal)"
                )
        else:
            try:
                other = other / self.factor
                return Physical(
                    self.value + other,
                    self.dimensions,
                    self.factor,
                    self.precision,
                    self._prefixed,
                )
            except:
                raise ValueError(
                    f"Cannot add between {self} and {other}: "
                    + ".value attributes are incompatible."
                )

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        raise ValueError(
            "Cannot incrementally add Physical instances because they are immutable."
            + " Use 'a = a + b', to make the operation explicit."
        )

    def __sub__(self, other):
        if isinstance(other, Physical):
            if self.dimensions == other.dimensions:
                try:
                    return Physical(
                        self.value - other.value,
                        self.dimensions,
                        self.factor,
                        self.precision,
                        self._prefixed,
                    )
                except:
                    raise ValueError(f"Cannot subtract between {self} and {other}")
            else:
                raise ValueError(
                    f"Cannot subtract between {self} and {other}:"
                    + ".dimensions attributes are incompatible (not equal)"
                )
        else:
            try:
                other = other / self.factor
                return Physical(
                    self.value - other,
                    self.dimensions,
                    self.factor,
                    self.precision,
                    self._prefixed,
                )
            except:
                raise ValueError(
                    f"Cannot subtract between {self} and {other}: "
                    + ".value attributes are incompatible."
                )

    def __rsub__(self, other):
        if isinstance(other, Physical):
            return self.__sub__(other)
        else:
            try:
                other = other / self.factor
                return Physical(
                    other - self.value,
                    self.dimensions,
                    self.factor,
                    self.precision,
                    self._prefixed,
                )
            except:
                raise ValueError(
                    f"Cannot subtract between {self} and {other}: "
                    + ".value attributes are incompatible."
                )

    def __isub__(self, other):
        raise ValueError(
            "Cannot incrementally subtract Physical instances because they are immutable."
            + " Use 'a = a - b', to make the operation explicit."
        )

    def __mul__(self, other):
        if isinstance(other, NUMBER):
            return Physical(
                self.value * other,
                self.dimensions,
                self.factor,
                self.precision,
                self._prefixed,
            )

        elif isinstance(other, Physical):
            new_dims = vec.add(self.dimensions, other.dimensions)
            new_power, new_dims_orig = Physical._powers_of_derived(
                new_dims, environment.units_by_dimension
            )
            new_factor = self.factor * other.factor
            test_factor = self._get_units_by_factor(
                new_factor, new_dims_orig, environment.units_by_factor, new_power
            )
            if not test_factor:
                new_factor = 1
            try:
                new_value = self.value * other.value
            except:
                raise ValueError(
                    f"Cannot multiply between {self} and {other}: "
                    + ".value attributes are incompatible."
                )
            if new_dims == Dimensions(0, 0, 0, 0, 0, 0, 0):
                return new_value
            else:
                return Physical(new_value, new_dims, new_factor, self.precision)
        else:
            try:
                return Physical(
                    self.value * other, self.dimensions, self.factor, self.precision
                )
            except:
                raise ValueError(
                    f"Cannot multiply between {self} and {other}: "
                    + ".value attributes are incompatible."
                )

    def __imul__(self, other):
        raise ValueError(
            "Cannot incrementally multiply Physical instances because they are immutable."
            + " Use 'a = a * b' to make the operation explicit."
        )

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, NUMBER):
            return Physical(
                self.value / other,
                self.dimensions,
                self.factor,
                self.precision,
                self._prefixed,
            )
        elif isinstance(other, Physical):
            new_dims = vec.subtract(self.dimensions, other.dimensions)
            new_power, new_dims_orig = Physical._powers_of_derived(
                new_dims, environment.units_by_dimension
            )
            new_factor = self.factor / other.factor
            if not self._get_units_by_factor(
                new_factor, new_dims_orig, environment.units_by_factor, new_power
            ):
                new_factor = 1
            try:
                new_value = self.value / other.value
            except:
                raise ValueError(
                    f"Cannot divide between {self} and {other}: "
                    + ".value attributes are incompatible."
                )
            if new_dims == Dimensions(0, 0, 0, 0, 0, 0, 0):
                return new_value
            else:
                return Physical(new_value, new_dims, new_factor, self.precision)
        else:
            try:
                return Physical(
                    self.value / other, self.dimensions, self.factor, self.precision
                )
            except:
                raise ValueError(
                    f"Cannot divide between {self} and {other}: "
                    + ".value attributes are incompatible."
                )

    def __rtruediv__(self, other):
        if isinstance(other, NUMBER):
            new_value = other / self.value
            new_dimensions = vec.multiply(self.dimensions, -1)
            new_factor = self.factor ** -1  # added new_factor
            return Physical(
                new_value,
                new_dimensions,
                new_factor,  # updated from self.factor to new_factor
                self.precision,
            )
        else:
            try:
                return Physical(
                    other / self.value,
                    vec.multiply(self.dimensions, -1),
                    self.factor ** -1,  # updated to ** -1
                    self.precision,
                )
            except:
                raise ValueError(
                    f"Cannot divide between {other} and {self}: "
                    + ".value attributes are incompatible."
                )

    def __itruediv__(self, other):
        raise ValueError(
            "Cannot incrementally divide Physical instances because they are immutable."
            + " Use 'a = a / b' to make the operation explicit."
        )

    def __pow__(self, other):
        if isinstance(other, NUMBER):
            if self._prefixed:
                return float(self) ** other
            new_value = self.value ** other
            new_dimensions = vec.multiply(self.dimensions, other)
            new_factor = self.factor ** other
            return Physical(new_value, new_dimensions, new_factor, self.precision)
        else:
            raise ValueError(
                "Cannot raise a Physical to the power of \
                                     another Physical -> ({self}**{other})".format(
                    self, other
                )
            )


class Environment:
    """
    A class that contains information about the units definitions that will be used
    by each Physical instance. Each Physical instance requests units definition
    information from the single Environment instance (OMG! Singleton!)
    """

    environment = {}
    units_by_dimension = {"derived": dict(), "defined": dict()}
    units_by_factor = dict()
    unit_vars = {}

    def __init__(self, physical_class):
        self._physical_class = physical_class

    def __call__(self, env_name: str, ret:bool = False):
        self.environment = self._load_environment(env_name)
        for name, definition in self.environment.items():
            factor = round(definition.get("Factor", 1), Physical._total_precision)
            dimension = definition.get("Dimension")
            value = definition.get("Value", 1)
            if factor == 1 and value == 1:
                self.units_by_dimension["derived"].setdefault(dimension, dict()).update(
                    {name: definition}
                )
            elif factor != 1:
                self.units_by_dimension["defined"].setdefault(dimension, dict()).update(
                    {name: definition}
                )
                self.units_by_factor.update({factor: {name: definition}})

        return self._instantiator(self.environment, self._physical_class, ret)


    def _load_environment(self, env_name: str):
        """
        Returns a dict that describes a set of unit definitions as contained in the
        JSON file titled "'env_name'.json" after the 'Dimension' definition is converted to
        an Dimensions object and any factors are checked for safety then evaluated.
        Raises error if file not found.
        """
        dim_array_not_defn = (
            "Dimension array not defined in environment"
            " .json file, '{env_name}.json', for unit '{unit}'"
        )
        unit_factor_not_eval = (
            "Unit definition in '{env_name}.json': Factor"
            "must be an arithmetic expr (as a str), a float,"
            "or an int: not '{factor}'."
        )

        path = __file__.strip("__init__.py")
        filename = path + env_name + ".json"
        with open(filename, "r", encoding="utf-8") as json_unit_definitions:
            units_environment = json.load(json_unit_definitions)

        # Load definitions
        arithmetic_expr = re.compile(r"[0-9.*/+-]")
        for unit, definitions in units_environment.items():
            dimensions = definitions.get("Dimension", ())
            factor = definitions.get("Factor", "1")
            symbol = definitions.get("Symbol", "")
            if not dimensions:
                raise DimensionError(dim_array_not_defn.format(env_name, unit))
            else:
                units_environment[unit]["Dimension"] = Dimensions(*dimensions)

            if type(factor) is str and not arithmetic_expr.match(factor):
                raise ValueError(unit_factor_not_eval.format(unit, env_name, factor))
            else:
                factor = str(factor)
                units_environment[unit]["Factor"] = eval(factor)
        return units_environment

    @staticmethod
    def _instantiator(environment: dict, physical_class, ret: bool = False):
        """
        Returns None; updates the globals dict with the units defined in the "definitions"
        portion of the environment dict. This is the method that instantiates all of the
        unit symbols defined in the environment json file.
        """
        to_globals = {}
        # Transfer definitions
        for unit, definitions in environment.items():
            dimensions = definitions["Dimension"]
            factor = definitions.get("Factor", 1)
            symbol = definitions.get("Symbol", "")
            value = definitions.get("Value", 1)
            if symbol:
                to_globals.update(
                    {unit: physical_class(1 / factor, dimensions, factor)}
                )
            else:
                to_globals.update({unit: physical_class(value, dimensions, factor)})
        Environment.unit_vars = to_globals
        if ret:
            return to_globals
        globals().update(to_globals)


if not "environment" in globals():
    environment = Environment(Physical)

# The seven SI base units...
_the_si_base_units = {
    "kg": Physical(1, Dimensions(1, 0, 0, 0, 0, 0, 0), 1.0),
    "m": Physical(1, Dimensions(0, 1, 0, 0, 0, 0, 0), 1.0),
    "s": Physical(1, Dimensions(0, 0, 1, 0, 0, 0, 0), 1.0),
    "A": Physical(1, Dimensions(0, 0, 0, 1, 0, 0, 0), 1.0),
    "cd": Physical(1, Dimensions(0, 0, 0, 0, 1, 0, 0), 1.0),
    "K": Physical(1, Dimensions(0, 0, 0, 0, 0, 1, 0), 1.0),
    "mol": Physical(1, Dimensions(0, 0, 0, 0, 0, 0, 1), 1.0),
}
globals().update(_the_si_base_units)

try: 
    from IPython.core.magic import (Magics, magics_class, line_magic, register_line_magic)
    from IPython import get_ipython
    from IPython.display import Latex, Markdown
    __Jupyter = get_ipython()
    __shell = __Jupyter.kernel.shell


    @register_line_magic
    def env(line):
        __shell.drop_by_id(environment.unit_vars)
        new_environment = environment(line.replace('"', "").replace("'",''), ret = True)
        #new_environment.update(_the_si_base_units)
        __shell.push(_the_si_base_units, interactive=True)
        __shell.push(new_environment, interactive=True)

    def load_ipython_extension(ipython):
        """This function is called when the extension is
        loaded. It accepts an IPython InteractiveShell
        instance. We can register the magic with the
        `register_magic_function` method of the shell
        instance."""
        ipython.register_magic_function(env, 'line')
        __shell.push(_the_si_base_units)
except:
    pass

        