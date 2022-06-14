"""Class for expressing physical quantities"""

from .exceptions import IncompatibleUnits

class Quantity:
    """A physical quantity consistiting of a value and fundamental units

    An instance of the Quantity class can represent any physical measurement composed
    of the 7 fundamental physical measurements (listed below).  It contains
    a scalar value and a tuple containing the exponents associated with each
    of the 7 fundamental measurements.

    The scalar value is set relative to the base units for each of the physical
    measurements.

    The fundamental measurements and associated base units are:
        - Length (meter)
        - Mass (kilogram)
        - Time (second)
        - Electric charge (coul)
        - Absolute temperature (Kelvin)
        - Intensity of lighth (candela)
        - Quantity of substance (mole)

    Constructor:

    Thare are three means for constructing a Quantity value:

    - value and fundamental unit exponents

        Args:
            value (number): numeric value in MKS units
            m (optional): exponent on the length component
            kg (optional): exponent on the mass component
            s (optional): exponent on the time component
            C (optional): exponent on the electric charge component
            K (optional): exponent on the absolute temperature component
            cand (optional): exponent on the light intensity component
            mol (optional): exponent on the substance quatnity component

    - scalar and base quantity

        Args:
            value (number): amount by which to scale the base quantity
            unit (Quantity): base value and units

    - scalar and tuple of unit exponents

        Args:
            value (number): numeric value in MKS unit
            unit (tuple): exponent values as listed above

    """
    __slots__ = ('value','unit')


    def __new__(cls, value=1, unit=None, 
            *, 
            m=0, kg=0, s=0, C=0, K=0, cand=0, mol=0):

        if unit is None:
            unit = (m,kg,s,C,K,cand,mol)
        elif isinstance(unit,Quantity):
            unit = unit.unit

        if [t for t in unit if t != 0]:
            return super(Quantity,cls).__new__(cls)
        else:
            return value


    def __init__(self, value=1, unit=None, 
            *, 
            m=0, kg=0, s=0, C=0, K=0, cand=0, mol=0):
        if unit is None:
            self.unit = (m,kg,s,C,K,cand,mol)
            self.value = value
        elif isinstance(unit,Quantity):
            self.unit = unit.unit
            self.value = value * unit.value
        elif len(unit) == 7:
            self.unit = tuple(unit)
            self.value = value
        else:
            raise TypeError("unit value must be Quantity of tuple of length 7")

    def compatible(self,other):
        try:
            return self.unit == other.unit
        except Exception as e:
            return False

    def assert_compatible(self,other):
        if not self.compatible(other):
            raise IncompatibleUnits(self,other)


    def __abs__(self):
        return Quantity(abs(self.value), unit=self.unit)

    def __add__(self,other):
        self.assert_compatible(other)
        return Quantity(self.value + other.value, unit=self.unit)

    __radd__ = __add__

    def __neg__(self):
        return Quantity(-self.value, unit=self.unit)
    
    def __sub__(self,other):
        self.assert_compatible(other)
        return Quantity(self.value - other.value, unit=self.unit)

    def __rsub__(self,other):
        self.assert_compatible(other)
        return Quantity(other.value - self.value, unit=self.unit)

    def __mul__(self,other):
        if isinstance(other,Quantity):
            unit = tuple(a + b for a,b in zip(self.unit,other.unit))
            product = Quantity(self.value * other.value, unit=unit)
        else:
            product = Quantity(self.value * other, unit=self.unit)

        return product

    __rmul__ = __mul__

    def invert(self):
        unit = tuple(-t for t in self.unit)
        return Quantity(1/self.value, unit=unit)

    def __truediv__(self,other):
        if isinstance(other,Quantity):
            unit = tuple(a - b for a,b in zip(self.unit,other.unit))
            quotient = Quantity(self.value / other.value, unit=unit)
        else:
            quotient = Quantity(self.value / other, unit=self.unit)

        return quotient

    def __rtruediv__(self,other):
        if isinstance(other,Quantity):
            unit = tuple(b-a for a,b in zip(self.unit,other.unit))
            quotient = Quantity(other.value / self.value, unit=unit)
        else:
            unit = tuple(-t for t in self.unit)
            quotient = Quantity(other / self.value, unit=unit)

        return quotient

    def __floordiv__(self,other):
        if isinstance(other,Quantity):
            unit = tuple(a - b for a,b in zip(self.unit,other.unit))
            quotient = Quantity(self.value // other.value, unit=unit)
        else:
            quotient = Quantity(self.value // other, unit=self.unit)

        return quotient

    def __rfloordiv__(self,other):
        if isinstance(other,Quantity):
            unit = tuple(b-a for a,b in zip(self.unit,other.unit))
            quotient = Quantity(other.value // self.value, unit=unit)
        else:
            unit = tuple(-t for t in self.unit)
            quotient = Quantity(other // self.value, unit=unit)

        return quotient

    def __pow__(self,n):
        unit = tuple(n*t for t in self.unit)
        return Quantity( self.value ** n, unit=unit )

    def root(self,n):
        unit = tuple(t/n for t in self.unit)
        return Quantity( self.value ** (1/n), unit=unit )

    def sqrt(self):
        return self.root(2)


    def __eq__(self, other):
        self.assert_compatible(other)
        return (self.value == other.value) and (self.unit == other.unit)
 
    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        self.assert_compatible(other)
        return self.value < other.value

    def __le__(self, other):
        self.assert_compatible(other)
        return self.value <= other.value

    def __gt__(self, other):
        self.assert_compatible(other)
        return self.value > other.value

    def __ge__(self, other):
        self.assert_compatible(other)
        return self.value >= other.value

    def __nonzero__(self):
        return True if self.value else False
    __bool__ = __nonzero__

    def __repr__(self):
        keys = ('m','kg','s','C','K','cand','mol')
        return (f"Quantity({self.value},"
                + ",".join(f"{n}={e}" for n,e in zip(keys,self.unit) if e)
                + ",)")

    def __str__(self):
        names = ('m','kg','s','C','K','cand','mol')
        num = " ".join(f"{n}" if e==1 else f"{n}^{e}" for n,e in zip(names,self.unit) if e>0)
        den = " ".join(f"{n}" if e==-1 else f"{n}^{-e}" for n,e in zip(names,self.unit) if e<0)

        if num:
            if den:
                return f"{self.value}[{num}/{den}]"
            else:
                return f"{self.value}[{num}]"
        elif den:
            return f"{self.value}[1/{den}]"
        else:
            return f"{self.value}"
