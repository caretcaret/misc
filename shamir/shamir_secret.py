#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Hello. The relevant function is "shamir_encode_mod" near the bottom, and the code that
# is run for the puzzle is at the very bottom.

# just copy-paste from the cells on the spreadsheet
cmu_15151_keys = """18  3160789073494119219975331859145791391225
40  1430753135701996376091780726929221817853
73  3601587717365841116603405186656734077573
79  2034501823308056841524863145092917416189
97  1995711117311035856962319837529675076607
118 5001440633677503365395752170148235181012
119 3338377719893825243809988869620252276083
123 4479588741951725678337213005293084504837
42  5061366445202978452194823992965648787703
111 3405443855661534639995093803487642629128
89  4877867186248262391136095188120539284870
105 2005750596510445079089370869214840025521
112 1818992470717480645841810607996977208947
81  2368606111217307274996086667651901889357
51  4448762988142812169341807951645265944915
72  40907233691467918899167851274008377018
122 3320221971152170136977331357469183035041
108 1296213743595134193248223327191708892647
95  4334973695381323474632615166511877602948
31  3420214921806336614995655537365141890922
85  2104490815193184780168999427611018898796
92  5314012844263658042045226726436758678320
101 28798584943212353004233860337575850809"""

mod_value = 5992830235524142758386850633773258681119

data_to_use = cmu_15151_keys


class Fraction(object):
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator
        self.simplify()

    def value(self):  # Returns the closest integer less than the fraction.
        if self.denominator == 1:
            return self.numerator
        else:
            return self.numerator / self.denominator  # avoids float division

    def simplify(self):
        gcf = gcd(self.numerator, self.denominator)
        self.numerator /= gcf
        self.denominator /= gcf
        if self.denominator < 0:
            self.numerator = -self.numerator
            self.denominator = -self.denominator

    def reciprocal(self):
        return Fraction(self.denominator, self.numerator)

    def __add__(self, other):
        if type(other) == Fraction:
            return Fraction(self.numerator * other.denominator + other.numerator * self.denominator, self.denominator * other.denominator)
        else:
            return self + Fraction(other, 1)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __neg__(self):
        return Fraction(-self.numerator, self.denominator)

    def __mul__(self, other):
        if type(other) == Fraction:
            return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)
        else:
            return Fraction(self.numerator * other, self.denominator)

    def __rmul__(self, other):
        return self * other

    def __div__(self, other):
        if type(other) == Fraction:
            return Fraction(self.numerator * other.denominator, self.denominator * other.numerator)
        else:
            return Fraction(self.numerator, self.denominator * other.numerator)

    def __rdiv__(self, other):
        return other * self.reciprocal()

    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)
        else:
            return '(' + str(self.numerator) + '/' + str(self.denominator) + ')'


def gcd(u, v):
    while v:
        u, v = v, u % v
    return abs(u)


class Polynomial(object):
    def __init__(self, *coefficients):
        self.coefficients = coefficients

    def evaluate(self, x):
        return sum([c * x ** power for power, c in enumerate(self.coefficients)])

    def __add__(self, other):
        if type(other) == Polynomial:
            out_list = [0] * max(len(self.coefficients), len(other.coefficients))
            for power, c1 in enumerate(self.coefficients):
                out_list[power] += c1
            for power, c2 in enumerate(other.coefficients):
                out_list[power] += c2
            return Polynomial(*tuple(out_list))
        else:
            return self.__add__(self, Polynomial(other))

    def __mul__(self, other):
        if type(other) == Polynomial:
            out_tuple = (0,) * (len(self.coefficients) + len(other.coefficients) - 1)
            for p1, c1 in enumerate(self.coefficients):
                for p2, c2 in enumerate(other.coefficients):
                    out_list = list(out_tuple)
                    out_list[p1 + p2] += c1 * c2
                    out_tuple = tuple(out_list)
            return Polynomial(*out_tuple)

        else:
            return self.__mul__(Polynomial(other))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __sub__(self, other):
        return self + (-1) * other

    def __div__(self, other):
        # other must be a number
        return self * (1 / other)

    def __eq__(self, other):
        return True in [c1 == c2 for c1, c2 in zip(self.coefficients, other.coefficients)]

    def __str__(self):
        terms = [str(c) + 'x^' + str(power) for power, c in enumerate(self.coefficients)]
        return ' + '.join(terms)


def shamir_decode(xs, ys):  # THIS IS FOR REGULAR SHAMIR WITHOUT MODS.
    xs = [Fraction(x, 1) for x in xs]
    ys = [Fraction(y, 1) for y in ys]
    basis_polynomials = []
    for index, this_x, this_y in zip(xrange(len(xs)), xs, ys):
        current_basis_poly = Polynomial(this_y)
        other_xs = xs[1:] if index == 0 else xs[:-1] if index == len(xs) - 1 else xs[:index] + xs[index + 1:]
        for other_x in other_xs:
            current_basis_poly *= Polynomial(-other_x, 1)
            current_basis_poly /= (this_x - other_x)
        basis_polynomials.append(current_basis_poly)
    final_polynomial = Polynomial(0)
    for poly in basis_polynomials:
        final_polynomial += poly
    print final_polynomial
    print long(final_polynomial.coefficients[0].value())


def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    return b, x, y


def modular_inverse(divisor, mod_value):
    g, x, y = egcd(divisor, mod_value)
    if g != 1:
        return None  # modular inverse does not exist, which does not happen with a prime mod_value
    else:
        return x % mod_value


def shamir_decode_mod(xs, ys, mod_value):
    basis_constants = []
    for index, this_x, this_y in zip(xrange(len(xs)), xs, ys):
        current_basis_constant = this_y
        other_xs = xs[1:] if index == 0 else xs[:-1] if index == len(xs) - 1 else xs[:index] + xs[index + 1:]
        for other_x in other_xs:
            current_basis_constant *= -other_x
            divisor = this_x - other_x
            if divisor < 0:
                divisor += mod_value
            current_basis_constant *= modular_inverse(divisor, mod_value)
        basis_constants.append(current_basis_constant)
    return sum(basis_constants) % mod_value


def shamir_encode(secret, k, n, mod_value=None):
    from random import randint
    polynomial_coeff = [secret]
    random_int_max = max(mod_value, secret)
    for i in xrange(k - 1):
        polynomial_coeff.append(randint(0, random_int_max))
    secret_poly = Polynomial(*polynomial_coeff)
    keys = []
    for i in xrange(1, n + 1):
        if mod_value is not None:
            keys.append((i, secret_poly.evaluate(i) % mod_value))
        else:
            keys.append((i, secret_poly.evaluate(i)))
    return keys


def bigint_decode(number):
    digits = list(str(number))
    if len(digits) % 2 != 0:
        raise ValueError
    result = ""
    while digits:
        a, b = digits.pop(0), digits.pop(0)
        character_digits = int(a + b)
        if character_digits >= 128 + 10 - 97:
            raise ValueError
        result += chr(character_digits - 10 + 97)
    return result


def extract_values(source):
    lines = [line.split() for line in source.split('\n')]
    xlist = [int(line[0]) for line in lines]
    ylist = [long(line[1]) for line in lines]
    return (xlist, ylist)


def cumulative_shamir_decode(xlist, ylist, mod_value):
    for i in xrange(1, len(xlist) + 1):
        secret = shamir_decode_mod(xlist[:i], ylist[:i], mod_value)
        print secret


if __name__ == '__main__':
    # This is the actual decoding of keys.
    xlist, ylist = extract_values(cmu_15151_keys)

    secret = shamir_decode_mod(xlist, ylist, mod_value)
    print secret

    try:
        print bigint_decode(secret)
    except ValueError:
        print "The secret integer cannot be parsed to form a string."
"""
    import time
    start = time.clock()
    for i in xrange(10000):
        secret = shamir_decode_mod(xlist, ylist, mod_value)
    end = time.clock()

    print (end - start)
"""
    # Here is generating keys, then decoding it.
    #keys = shamir_encode(1234, 3, 6, mod_value)
    #xlist = [int(line[0]) for key in keys]
    #ylist = [long(line[1]) for key in keys]
    #shamir_decode_mod(xlist, ylist, mod_value)
