# -*- coding: utf-8 -*-
"""
Plural forms and in-word representation for numerals.
"""
from __future__ import division
from decimal import Decimal
import six

FRACTIONS = (
    (u"десята", u"десятих", u"десятих"),
    (u"сота", u"сотих", u"сотих"),
    (u"тисячна", u"тисячних", u"тисячних"),
    (u"десятитисячна", u"десятитисячних", u"десятитисячних"),
    (u"стотисячних", u"стотисячних", u"стотисячних"),
    (u"мільйони", u"мільйонних", u"мільйонних"),
    (u"десятиммільйонна", u"десятимільйонних", u"десятимільйонних"),
    (u"стомільйонна", u"стомільйонниї", u"стомільйонних"),
    (u"мілярдна", u"мілярдних", u"мілярдних"),
    )  #: Forms (1, 2, 5) for fractions

ONES = {
    0: (u"",       u"",       u""),
    1: (u"один",   u"одна",   u"одна"),
    2: (u"два",    u"дві",    u"дві"),
    3: (u"три",    u"три",    u"три"),
    4: (u"чотири", u"чотири", u"чотири"),
    5: (u"п'ять",   u"п'ять",   u"п'ять"),
    6: (u"шість",  u"шість",  u"шість"),
    7: (u"сім",   u"сім",   u"сім"),
    8: (u"вісім", u"вісім", u"вісім"),
    9: (u"дев'ять", u"дев'ять", u"дев'ять"),
    }  #: Forms (MALE, FEMALE, NEUTER) for ones

TENS = {
    0: u"",
    # 1 - окремий випадок
    10: u"десять",
    11: u"одинадцять",
    12: u"дванадцять",
    13: u"тринадцять",
    14: u"чотирнадцять",
    15: u"п'ятнадцять",
    16: u"шістнадцять",
    17: u"сімнадцять",
    18: u"вісімнадцять",
    19: u"дев'ятнадцять",
    2: u"двадцять",
    3: u"тридцять",
    4: u"сорок",
    5: u"п'ятдесят",
    6: u"шістдесят",
    7: u"сімдесят",
    8: u"вісімдесят",
    9: u"дев'яносто",
    }  #: Tens

HUNDREDS = {
    0: u"",
    1: u"сто",
    2: u"двісті",
    3: u"триста",
    4: u"чотириста",
    5: u"п'ятсот",
    6: u"шістьсот",
    7: u"сімсот",
    8: u"вісімсот",
    9: u"дев'ятсот",
    }  #: Hundreds

MALE = 1    #: sex - male
FEMALE = 2  #: sex - female
NEUTER = 3  #: sex - neuter

def print_utf(s):
    if six.PY3:
        out = s
    else:
        out = s.encode('UTF-8')
    print(out)


def check_length(value, length):
    """
    Checks length of value

    @param value: value to check
    @type value: C{str}

    @param length: length checking for
    @type length: C{int}

    @return: None when check successful

    @raise ValueError: check failed
    """
    _length = len(value)
    if _length != length:
        raise ValueError("length must be %d, not %d" % \
                         (length, _length))
                         
def check_positive(value, strict=False):
    """
    Checks if variable is positive

    @param value: value to check
    @type value: C{integer types}, C{float} or C{Decimal}

    @return: None when check successful

    @raise ValueError: check failed
    """
    if not strict and value < 0:
        raise ValueError("Value must be positive or zero, not %s" % str(value))
    if strict and value <= 0:
        raise ValueError("Value must be positive, not %s" % str(value)) 
        

def split_values(ustring, sep=u','):
    """
    Splits unicode string with separator C{sep},
    but skips escaped separator.
    
    @param ustring: string to split
    @type ustring: C{unicode}
    
    @param sep: separator (default to u',')
    @type sep: C{unicode}
    
    @return: tuple of splitted elements
    """
    assert isinstance(ustring, six.text_type), "uvalue must be unicode, not %s" % type(ustring)
    # unicode have special mark symbol 0xffff which cannot be used in a regular text,
    # so we use it to mark a place where escaped column was
    ustring_marked = ustring.replace(u'\,', u'\uffff')
    items = tuple([i.strip().replace(u'\uffff', u',') for i in ustring_marked.split(sep)])
    return items        



def _get_float_remainder(fvalue, signs=9):
    """
    Get remainder of float, i.e. 2.05 -> '05'

    @param fvalue: input value
    @type fvalue: C{integer types}, C{float} or C{Decimal}

    @param signs: maximum number of signs
    @type signs: C{integer types}

    @return: remainder
    @rtype: C{str}

    @raise ValueError: fvalue is negative
    @raise ValueError: signs overflow
    """
    check_positive(fvalue)
    if isinstance(fvalue, six.integer_types):
        return "0"
    if isinstance(fvalue, Decimal) and fvalue.as_tuple()[2] == 0:
        # Decimal.as_tuple() -> (sign, digit_tuple, exponent)
        # если экспонента "0" -- значит дробной части нет
        return "0"

    signs = min(signs, len(FRACTIONS))

    # нужно remainder в строке, потому что дробные X.0Y
    # будут "ломаться" до X.Y
    remainder = str(fvalue).split('.')[1]
    iremainder = int(remainder)
    orig_remainder = remainder
    factor = len(str(remainder)) - signs

    if factor > 0:
        # после запятой цифр больше чем signs, округляем
        iremainder = int(round(iremainder / (10.0**factor)))
    format = "%%0%dd" % min(len(remainder), signs)

    remainder = format % iremainder

    if len(remainder) > signs:
        # при округлении цифр вида 0.998 ругаться
        raise ValueError("Signs overflow: I can't round only fractional part \
                          of %s to fit %s in %d signs" % \
                         (str(fvalue), orig_remainder, signs))

    return remainder


def choose_plural(amount, variants):
    """
    Choose proper case depending on amount

    @param amount: amount of objects
    @type amount: C{integer types}

    @param variants: variants (forms) of object in such form:
        (1 object, 2 objects, 5 objects).
    @type variants: 3-element C{sequence} of C{unicode}
        or C{unicode} (three variants with delimeter ',')

    @return: proper variant
    @rtype: C{unicode}

    @raise ValueError: variants' length lesser than 3
    """
    
    if isinstance(variants, six.text_type):
        variants = split_values(variants)
    check_length(variants, 3)
    amount = abs(amount)
    
    if amount % 10 == 1 and amount % 100 != 11:
        variant = 0
    elif amount % 10 >= 2 and amount % 10 <= 4 and \
         (amount % 100 < 10 or amount % 100 >= 20):
        variant = 1
    else:
        variant = 2
    
    return variants[variant]


def get_plural(amount, variants, absence=None):
    """
    Get proper case with value

    @param amount: amount of objects
    @type amount: C{integer types}

    @param variants: variants (forms) of object in such form:
        (1 object, 2 objects, 5 objects).
    @type variants: 3-element C{sequence} of C{unicode}
        or C{unicode} (three variants with delimeter ',')

    @param absence: if amount is zero will return it
    @type absence: C{unicode}

    @return: amount with proper variant
    @rtype: C{unicode}
    """
    if amount or absence is None:
        return u"%d %s" % (amount, choose_plural(amount, variants))
    else:
        return absence


def _get_plural_legacy(amount, extra_variants):
    """
    Get proper case with value (legacy variant, without absence)

    @param amount: amount of objects
    @type amount: C{integer types}

    @param variants: variants (forms) of object in such form:
        (1 object, 2 objects, 5 objects, 0-object variant).
        0-object variant is similar to C{absence} in C{get_plural}
    @type variants: 3-element C{sequence} of C{unicode}
        or C{unicode} (three variants with delimeter ',')

    @return: amount with proper variant
    @rtype: C{unicode}
    """
    absence = None
    if isinstance(extra_variants, six.text_type):
        extra_variants = split_values(extra_variants)
    if len(extra_variants) == 4:
        variants = extra_variants[:3]
        absence = extra_variants[3]
    else:
        variants = extra_variants
    return get_plural(amount, variants, absence)


def gryvens(amount, zero_for_kopeck=False):
    """
    Get string for money

    @param amount: amount of money
    @type amount: C{integer types}, C{float} or C{Decimal}

    @param zero_for_kopeck: If false, then zero kopecks ignored
    @type zero_for_kopeck: C{bool}

    @return: in-words representation of money's amount
    @rtype: C{unicode}

    @raise ValueError: amount is negative
    """

    check_positive(amount)

    pts = []
    amount = round(amount, 2)
    pts.append(sum_string(int(amount), 1, (u"гривня", u"гривні", u"гривень")))
    remainder = _get_float_remainder(amount, 2)
    iremainder = int(remainder)

    if iremainder != 0 or zero_for_kopeck:
        # якщо 3.1, то це 10 копійок, а не одна
        if iremainder < 10 and len(remainder) == 1:
            iremainder *= 10
        pts.append(sum_string(iremainder, 2,
                              (u"копійка", u"копійки", u"копійок")))

    return u" ".join(pts)


def in_words_int(amount, gender=MALE):
    """
    Integer in words

    @param amount: numeral
    @type amount: C{integer types}

    @param gender: gender (MALE, FEMALE or NEUTER)
    @type gender: C{int}

    @return: in-words reprsentation of numeral
    @rtype: C{unicode}

    @raise ValueError: amount is negative
    """
    check_positive(amount)

    return sum_string(amount, gender)

def in_words_float(amount, _gender=FEMALE):
    """
    Float in words

    @param amount: float numeral
    @type amount: C{float} or C{Decimal}

    @return: in-words reprsentation of float numeral
    @rtype: C{unicode}

    @raise ValueError: when ammount is negative
    """
    check_positive(amount)

    pts = []
    # преобразуем целую часть
    pts.append(sum_string(int(amount), 2,
                          (u"ціла", u"цілих", u"цілих")))
    # теперь то, что после запятой
    remainder = _get_float_remainder(amount)
    signs = len(str(remainder)) - 1
    pts.append(sum_string(int(remainder), 2, FRACTIONS[signs]))

    return u" ".join(pts)


def in_words(amount, gender=None):
    """
    Numeral in words

    @param amount: numeral
    @type amount: C{integer types}, C{float} or C{Decimal}

    @param gender: gender (MALE, FEMALE or NEUTER)
    @type gender: C{int}

    @return: in-words reprsentation of numeral
    @rtype: C{unicode}

    raise ValueError: when amount is negative
    """
    check_positive(amount)
    if isinstance(amount, Decimal) and amount.as_tuple()[2] == 0:
        # если целое,
        # т.е. Decimal.as_tuple -> (sign, digits tuple, exponent), exponent=0
        # то как целое
        amount = int(amount)
    if gender is None:
        args = (amount,)
    else:
        args = (amount, gender)
    # если целое
    if isinstance(amount, six.integer_types):
        return in_words_int(*args)
    # если дробное
    elif isinstance(amount, (float, Decimal)):
        return in_words_float(*args)
    # ни float, ни int, ни Decimal
    else:
        # до сюда не должно дойти
        raise TypeError(
            "amount should be number type (int, long, float, Decimal), got %s"
            % type(amount))


def sum_string(amount, gender, items=None):
    """
    Get sum in words

    @param amount: amount of objects
    @type amount: C{integer types}

    @param gender: gender of object (MALE, FEMALE or NEUTER)
    @type gender: C{int}

    @param items: variants of object in three forms:
        for one object, for two objects and for five objects
    @type items: 3-element C{sequence} of C{unicode} or
        just C{unicode} (three variants with delimeter ',')

    @return: in-words representation objects' amount
    @rtype: C{unicode}

    @raise ValueError: items isn't 3-element C{sequence} or C{unicode}
    @raise ValueError: amount bigger than 10**11
    @raise ValueError: amount is negative
    """
    if isinstance(items, six.text_type):
        items = split_values(items)
    if items is None:
        items = (u"", u"", u"")

    try:
        one_item, two_items, five_items = items
    except ValueError:
        raise ValueError("Items must be 3-element sequence")

    check_positive(amount)

    if amount == 0:
        return u"нуль %s" % five_items

    into = u''
    tmp_val = amount

    # одиниці
    into, tmp_val = _sum_string_fn(into, tmp_val, gender, items)
    # тисячі
    into, tmp_val = _sum_string_fn(into, tmp_val, FEMALE,
                                    (u"тисяча", u"тисячі", u"тисяч"))
    # мільйони
    into, tmp_val = _sum_string_fn(into, tmp_val, MALE,
                                    (u"мільйон", u"мільйони", u"мільйонів"))
    # мільярди
    into, tmp_val = _sum_string_fn(into, tmp_val, MALE,
                                    (u"мільярд", u"мільярда", u"мільярдів"))
    if tmp_val == 0:
        return into
    else:
        raise ValueError("Cannot operand with numbers bigger than 10**11")


def _sum_string_fn(into, tmp_val, gender, items=None):
    """
    Make in-words representation of single order

    @param into: in-words representation of lower orders
    @type into: C{unicode}

    @param tmp_val: temporary value without lower orders
    @type tmp_val: C{integer types}

    @param gender: gender (MALE, FEMALE or NEUTER)
    @type gender: C{int}

    @param items: variants of objects
    @type items: 3-element C{sequence} of C{unicode}

    @return: new into and tmp_val
    @rtype: C{tuple}

    @raise ValueError: tmp_val is negative
    """
    if items is None:
        items = (u"", u"", u"")
    one_item, two_items, five_items = items
    
    check_positive(tmp_val)

    if tmp_val == 0:
        return into, tmp_val

    words = []

    rest = tmp_val % 1000
    tmp_val = tmp_val // 1000
    if rest == 0:
        # последние три знака нулевые
        if into == u"":
            into = u"%s " % five_items
        return into, tmp_val

    # начинаем подсчет с rest
    end_word = five_items

    # сотни
    words.append(HUNDREDS[rest // 100])

    # десятки
    rest = rest % 100
    rest1 = rest // 10
    # особый случай -- tens=1
    tens = rest1 == 1 and TENS[rest] or TENS[rest1]
    words.append(tens)

    # одиниці
    if rest1 < 1 or rest1 > 1:
        amount = rest % 10
        end_word = choose_plural(amount, items)
        words.append(ONES[amount][gender-1])
    words.append(end_word)

    # добавляем то, что уже было
    words.append(into)

    # убираем пустые подстроки
    words = filter(lambda x: len(x) > 0, words)

    # склеиваем и отдаем
    return u" ".join(words).strip(), tmp_val
