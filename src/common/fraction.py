'''
Created on Nov 29, 2010

@author: Niriel
'''

def best_rationals(afloat):
    """Approximate afloat with fractions.
    
    Generate triples (num, den, error) where num/den is a best rational
    approximation of the float afloat and error is the difference (afloat -
    num/den).

    A generator of the best rational approximations of a float using continued
    fractions. (see http://en.wikipedia.org/wiki/Continued_fraction)

    Possible improvements left to the interested reader:
      - extend the generator to support decimal.Decimal numbers.
      - extend the generator to support gmpy.mpf numbers.

    Code snippet by Gribouillis on Sep 18th, 2009
    http://www.daniweb.com/code/snippet223956.html

    """
    afloat, lastnum, num = ((-afloat, -1, int(-afloat)) if afloat < 0
                            else (afloat, 1, int(afloat)))
    lastden, den = 0, 1
    rest, quot = afloat, int(afloat)
    while True:
        yield num, den, afloat - float(num) / den
        rest = 1.0 / (rest - quot)
        quot = int(rest)
        lastnum, num, lastden, den = (num, quot * num + lastnum,
                                      den, quot * den + lastden)

def best_rational(afloat, tolerance):
    gen = best_rationals(afloat)
    num, den, err = next(gen)
    while abs(err) > tolerance:
        num, den, err = next(gen)
    return num, den, err

if __name__ == "__main__":
    import pygame
    pygame.init()
    modes = pygame.display.list_modes()
    for x, y in modes:
        f = float(x) / y
        num, den, err = best_rational(f, 0.01)
        print "%4i x %4i (%i/%i) %f" % (x, y, num, den, f)
    pygame.quit()
