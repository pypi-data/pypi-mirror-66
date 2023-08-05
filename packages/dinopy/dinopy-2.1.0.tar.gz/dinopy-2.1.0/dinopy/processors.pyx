# -*- coding: utf-8 -*-
"""The processors module offers functions that operate on iterators (for example as provided
by :meth:`dinopy.FastaReader.lines()`)
.
At the moment, the following processors are provided:

    * :meth:`qgrams`
    * :meth:`reverse_complement`
    * :meth:`complement`

Work in progress processors include:

    * :code:`suffix_array` (using the induced sorting algorithm)
    * :code:`qgram_index` (using a two-pass algorithm)

"""
import collections
import sys
import itertools
import numpy as np
from collections import Counter
from random import choice

from dinopy.shaping import windows, _windows_bytes, _windows_unicode, _windows_unicode_view, _windows_bytearray
from .exceptions import InvalidDtypeError, InvalidEncodingError

cimport cython
from cpython.mem cimport PyMem_Free

from .definitions cimport _iupac_mapping
from .shaping cimport _apply_shape_int
from dinopy cimport wrap_sais
from .definitions import two_bit, four_bit

def qgrams(source, object qgram_shape, object dtype=None, type encoding=None, bint wrap=False, bint sentinel=False):
    """Construct an iterator of qgrams of any given iterable source, using the specified shape.

    Arguments:
        source (Iterable): Any iterable source or iterable of iterable sources.
             So "ACGT", ["ACGT"] and ["ACGT", "ACGT"] would all be valid.

        qgram_shape (object): Any input that describes a q-gram shape as defined in :mod:`dinopy.shape`; for example 5 or ``"##_#"``.

        dtype (type): Data type of the source. One of ``None``, ``bytes``, ``bytearray``, ``basenumbers``, ``str`` (see `dtype`, Default: ``None``).
            This is mainly a performance hint;
            if for example your source iterable supplies str items, specifying ``str`` will result in dinopy
            picking the respective *low level* function for generating str-q-grams, instead of having to guess
            each time a new item is processed (which is the case with the default dtype value of ``None``).

        encoding (type): One of :code:`None`, :code:`two_bit`, :code:`four_bit` (Default: ``None``).

        wrap (bool): Whether to compute q-grams across consecutive source-item-boundaries. 
            For example the 3-grams for the source ``["ACGT", "TTTT"]`` would be ``["ACG", "CGT", "TTT", "TTT"]`` (``wrap = False``),
            but with ``wrap = True`` the q-grams would be ``["ACG", "CGT", "GTT", "TTT", "TTT", "TTT"]``.
            (Default: ``False``)

    Yields:
        dtype: All q-grams of the source, either in the same dtype as the source or encoded using either 2bit or 4bit encoding.

    Raises:
        InvalidDtypeError: If an unsopported (or unrecognized) type is passed to dtype.
        InvalidEncodingError: If an unsopported (or unrecognized) type is passed to encoding.

    Examples:
        * Example 1::

            far = dinopy.FastaReader("files/testgenome_IUPAC.fasta")
            shp = dinopy.shape.Shape("#######")
            for qgram in dinopy.qgrams(far.reads(dtype=str), shp, dtype=str, encoding=None):
                pass

        * Example 2::

            far = dinopy.FastaReader("files/testgenome_IUPAC.fasta")
            shp = dinopy.shape.Shape(5)
            for qgram in dinopy.qgrams(far.reads(dtype=bytes), shp, dtype=bytes, encoding=dinopy.two_bit):
                pass

        * Example 3::

            far = dinopy.FastaReader("files/testgenome_IUPAC.fasta")
            shp = dinopy.shape.Shape("##_#_#")
            for qgram in dinopy.qgrams(far.lines(dtype=str), shp, dtype=str, encoding=None, wrap=True):
                pass

    """
    cdef:
        Shape shp = Shape(qgram_shape)
        int shape_length = len(shp)
        int item_length
        bint buffer_source = PyObject_CheckBuffer(source) == 1

    if dtype not in (valid_dtypes | {None,}):
        raise InvalidDtypeError("Unsupported dtype {}".format(dtype))

    if isinstance(source, (str, bytes)) or buffer_source:
        source = [source]
    if encoding is None:
        if not wrap:
            # pick the right low level function for the given dtype
            if dtype is None:
                for item in source:
                    yield from windows(item, shp)
            elif dtype == str:
                for item in source:
                    yield from _windows_unicode(item, shp)
            elif dtype in [bytes, basenumbers]:
                for item in source:
                    yield from _windows_bytes(item, shp)
            elif dtype == bytearray:
                for item in source:
                    yield from _windows_bytearray(item, shp)
            elif buffer_source:
                for item in source:
                    yield from _windows_unicode_view(item, shp)
            else:
                # None of the expected dtypes has been found.
                # Use (potentially slow) general window function.
                # This should be caught by the check against valid dtypes
                for item in source:
                    yield from windows(item, shp)
        else:  # wrap
            if dtype in [bytes, basenumbers]:
                yield from _qgrams_wrap_bytes(source, shp)
            elif dtype == bytearray:
                yield from _qgrams_wrap_bytearray(source, shp)
            elif dtype == str:
                yield from _qgrams_wrap_str(source, shp)
            elif dtype is None:  # try using '+' for 'automatic' type detection
                for item in _general_wrap(source, shape_length):
                    yield from windows(item, shp)
            elif buffer_source:
                for item in _wrap_memview(source, shape_length):
                    yield from _windows_unicode_view(item, shp)
            else:
                raise TypeError("Unsupported type: {}".format(str(type(source))))

    elif encoding is two_bit:
        if wrap: # use 2bit encoding, with wrap
            if dtype is None:
                for item in _general_wrap(source, shape_length):
                    if shp.is_solid():
                        yield from _2bit_qgrams(item, shp.length, sentinel)
                    else:
                        yield from _2bit_qgrams_with_shape(item, shp, sentinel)
            elif dtype == str:
                for item in _wrap_str(source, shape_length):
                    if shp.is_solid():
                        yield from _2bit_qgrams(item, shp.length, sentinel)
                    else:
                        yield from _2bit_qgrams_with_shape(item, shp, sentinel)
            elif dtype in [bytes, basenumbers]:
                for item in _wrap_bytes(source, shape_length):
                    if shp.is_solid():
                        yield from _2bit_qgrams(item, shp.length, sentinel)
                    else:
                        yield from _2bit_qgrams_with_shape(item, shp, sentinel)
            elif dtype == bytearray:
                for item in _wrap_bytearray(source, shape_length):
                    if shp.is_solid():
                        yield from _2bit_qgrams(item, shp.length, sentinel)
                    else:
                        yield from _2bit_qgrams_with_shape(item, shp, sentinel)
            elif buffer_source:
                for item in _wrap_memview(source, shape_length):
                    if shp.is_solid():
                        yield from _2bit_qgrams(item, shp.length, sentinel)
                    else:
                        yield from _2bit_qgrams_with_shape(item, shp, sentinel)
            else:
                try:
                    for item in _general_wrap(source, shape_length):
                        if shp.is_solid():
                            yield from _2bit_qgrams(item, shp.length, sentinel)
                        else:
                            yield from _2bit_qgrams_with_shape(item, shp, sentinel)
                except TypeError:
                    raise TypeError("Unsupported type {} of source.".format(str(type(source))))
        else: # use 2bit encoding, without wrap
            try:
                for item in source:
                    if shp.is_solid():
                        yield from _2bit_qgrams(item, shp.length, sentinel)
                    else:
                        yield from _2bit_qgrams_with_shape(item, shp, sentinel)
            except TypeError:
                raise TypeError("Unsupported type {} of source.".format(str(type(source))))

    elif encoding is four_bit:
        if wrap: # use 4bit encoding, with wrap
            if dtype is None:
                for item in _general_wrap(source, shape_length):
                    if shp.is_solid():
                        yield from _4bit_qgrams(item, shp.length, sentinel)
                    else:
                        yield from _4bit_qgrams_with_shape(item, shp, sentinel)
            elif dtype == str:
                for item in _wrap_str(source, shape_length):
                    if shp.is_solid():
                        yield from _4bit_qgrams(item, shp.length, sentinel)
                    else:
                        yield from _4bit_qgrams_with_shape(item, shp, sentinel)
            elif dtype in [bytes, basenumbers]:
                for item in _wrap_bytes(source, shape_length):
                    if shp.is_solid():
                        yield from _4bit_qgrams(item, shp.length, sentinel)
                    else:
                        yield from _4bit_qgrams_with_shape(item, shp, sentinel)
            elif dtype == bytearray:
                for item in _wrap_bytearray(source, shape_length):
                    if shp.is_solid():
                        yield from _4bit_qgrams(item, shp.length, sentinel)
                    else:
                        yield from _4bit_qgrams_with_shape(item, shp, sentinel)
            elif buffer_source:
                for item in _wrap_memview(source, shape_length):
                    if shp.is_solid():
                        yield from _4bit_qgrams(item, shp.length, sentinel)
                    else:
                        yield from _4bit_qgrams_with_shape(item, shp, sentinel)
            else:
                try:
                    for item in _general_wrap(source, shape_length):
                        for qgram in windows(item, shp):
                            yield encode(qgram, _4bit_from_any, sentinel)
                except TypeError:
                    raise TypeError("Unsupported type {} of source.".format(str(type(source))))
        else: # use 4bit encoding, without wrap
            try:
                for item in source:
                    if shp.is_solid():
                        yield from _4bit_qgrams(item, shp.length, sentinel)
                    else:
                        yield from _4bit_qgrams_with_shape(item, shp, sentinel)
            except TypeError:
                raise TypeError("Unsupported type {} of source.".format(str(type(source))))
    else:
        raise InvalidEncodingError("Unsupported or unrecognized encoding {}.".format(type(encoding)))

def _general_wrap(object source, int q, dtype=None):
    """Compute the overlap sequences between consecutive source items.

    Example:
        For the sequences ['AAAAA', 'CCCCC', 'TTTTT'] with 3-grams the resulting
        sequences would be ['AAAAA', 'AACC', 'CCCCC', 'CCTT', 'TTTTT'].
        From the overlap sequences all overlap 3-grams can be created.
        Hence all q-grams including the overlap can be computed using
        qgrams('AAAAA', 3) + qgrams('AACC', 3) + qgrams('CCCCC', 3) + qgrams('CCTT', 3) + qgrams('TTTTT', 3)
    
    Arguments:
        source (Iterable of Iterable): Sequences for which the overlap sequences
            will be computed.
        q (int): The size the overlap is computed for. Basically this is q.

    Returns:
        Iterable: An Iterable containing all input sequences interleaved with
        the overlap sequences between those sequences.
    """
    if dtype is None:
        # try to autodetect sequence type if None has been given.
        if isinstance(source, (collections.Sequence, collections.Iterable)):
            item = None
            if isinstance(source, collections.Sequence):  # subscriptable
                item = source[0]
            elif isinstance(source, collections.Iterable):
                for i in source:
                    item = i
                    break
                source = itertools.chain([i], source)
            if isinstance(item, bytes):
                dtype = bytes
            elif isinstance(item, bytearray):
                dtype = bytearray
            elif isinstance(item, str):
                dtype = str
            else:
                raise TypeError("Unsupported item type: {}.".format(str(type(item))))
        else:
            raise TypeError("Unsupported container type: {}.".format(str(type(source))))
    # call typed wrap function
    if dtype in (bytes, basenumbers):
        return _wrap_bytes(source, q=q)
    elif dtype == str:
        return _wrap_str(source, q=q)
    elif dtype == bytearray:
        return _wrap_bytearray(source, q=q)

def _wrap_bytes(object source, int q):
    """Compute the overlap sequences between bytes objects.

    Arguments:
        source(Iterable): Containing byte items.
        q(int): Length of the desired q-grams.

    Yields:
        All input sequences interleaved with the overlap sequences between
        those sequences.
    """
    cdef bytes overlap, item, last_item
    cdef int item_length, last_item_length
    last_item = None

    for item in source:
        if last_item is not None:
            item_length = len(item)
            overlap = last_item[last_item_length - q + 1:] + item[:q - 1]
            yield overlap
        yield item
        last_item = item
        last_item_length = len(last_item)

def _wrap_str(object source, int q):
    """Compute the overlap sequences between string items.

    Arguments:
        source(Iterable): Containing string items.
        q(int): Length of the desired q-grams.

    Yields:
        All input sequences interleaved with the overlap sequences between
        those sequences.
    """
    cdef str last_line, overlap, item
    cdef int item_length, last_line_length
    last_line = None

    for item in source:
        if last_line is not None:
            item_length = len(item)
            overlap = last_line[last_line_length - q + 1:] + item[:q - 1]
            yield overlap
        yield item
        last_line = item
        last_line_length = len(last_line)

def _wrap_bytearray(object source, int q):
    """Compute the overlap sequences between bytearray items.

    Arguments:
        source(Iterable): Containing bytearray items.
        q(int): Length of the desired q-grams.

    Yields:
        All input sequences interleaved with the overlap sequences between
        those sequences.
    """
    cdef bytearray last_line, overlap, item
    cdef int item_length, last_line_length
    last_line = None

    for item in source:
        if last_line is not None:
            item_length = len(item)
            overlap = last_line[last_line_length - q + 1:] + item[:q - 1]
            yield overlap
        yield item
        last_line = item
        last_line_length = len(last_line)

def _wrap_memview(object source, int q):
    """Compute the overlap sequences between memoryview items.

    Arguments:
        source(Iterable): Containing memoryview items.
        q(int): Length of the desired q-grams.

    Yields:
        All input sequences interleaved with the overlap sequences between
        those sequences.
    """
    cdef object last_line, overlap, item
    cdef int item_length, last_line_length
    last_line = None

    for item in source:
        if last_line is not None:
            item_length = len(item)
            overlap = np.concatenate([last_line[last_line_length - q + 1:], item[:q - 1]])
            yield overlap
        yield item
        last_line = item
        last_line_length = len(last_line)

def _qgrams_wrap_bytes(object source, Shape shp):
    """Create q-grams overlapping item boundaries from bytes.

    Arguments:
        source(Iterable): Containing bytes items.
        shp(Shape): A Shape object for the shape that will be used to shape
            the q-grams.

    Yields:
        All q-grams, including those overlapping item boundaries, created from the source.
    """
    cdef bytes last_line, overlap, item
    cdef int shape_length, item_length, last_line_length
    shape_length = len(shp)
    last_line = None

    for item in source:
        if last_line is not None:
            item_length = len(item)
            overlap = last_line[last_line_length - shape_length + 1:] + item[:shape_length - 1]
            for qgram in _windows_bytes(overlap, shp):
                yield qgram
        for qgram in _windows_bytes(item, shp):
            yield qgram
        last_line = item
        last_line_length = len(last_line)

def _qgrams_wrap_str(object source, Shape shp):
    """Create q-grams overlapping item boundaries from strings.

    Arguments:
        source(Iterable): Containing string items.
        shp(Shape): A Shape object for the shape that will be used to shape
            the q-grams.

    Yields:
        All q-grams, including those overlapping item boundaries, created from the source.
    """
    cdef str last_line, overlap, item
    cdef int shape_length, item_length, last_line_length
    shape_length = len(shp)
    last_line = None

    for item in source:
        if last_line is not None:
            item_length = len(item)
            overlap = last_line[last_line_length - shape_length + 1:] + item[:shape_length - 1]
            for qgram in _windows_unicode(overlap, shp):
                yield qgram
        for qgram in _windows_unicode(item, shp):
            yield qgram
        last_line = item
        last_line_length = len(last_line)

def _qgrams_wrap_bytearray(object source, Shape shp):
    """Create q-grams overlapping item boundaries from bytearrays.

    Arguments:
        source(Iterable): Containing bytearray items.
        shp(Shape): A Shape object for the shape that will be used to shape
            the qgrams.

    Yields:
        All q-grams, including those overlapping item boundaries, created from the source.
    """
    cdef bytearray last_line, overlap, item
    cdef int shape_length, item_length, last_line_length
    shape_length = len(shp)
    last_line = None

    for item in source:
        if last_line is not None:
            item_length = len(item)
            overlap = last_line[last_line_length - shape_length + 1:] + item[:shape_length - 1]
            for qgram in _windows_bytearray(overlap, shp):
                yield qgram
        for qgram in _windows_bytearray(item, shp):
            yield qgram
        last_line = item
        last_line_length = len(last_line)


cpdef uint64 _first_qgram_2bit(object seq, bint sentinel=False):
    """Encode the given sequence using 2bit encoding.

    Arguments:
        seq(object): Any dinopy sequence (see dtype).

    Returns:
        uint64: The 2bit encoded qgram.
    """
    cdef uint64 qgram = 0b11 if sentinel else 0  # initialize qgram with sentinel bits
    cdef int base
    for item in seq:
        base = _2bit_from_any_with_iupac_replacement[item]
        qgram = (qgram << 2) | base
    return qgram


def _2bit_qgrams(object seq, int q, bint sentinel=False):
    """Create 2bit encoded q-grams from a sequence.

    Warning:
        This only works for full shapes and q < 32.
        Also this can suffer greatly in performance on 32bit systems.

    Arguments:
        seq (Iterable): Any dinopy sequence.
        q (int): Length of the q-grams to be created.

    Yields:
        uint64: 2bit encoded q-grams generated from the sequence.
    """
    cdef uint64 sentinel_bits = <uint64>0b11 << (2*q) if sentinel else 0  # mask for the two sentinel bits
    cdef uint64 valid_bits_mask = (<uint64>1 << (2 * (q + 1))) - 1 if sentinel else (<uint64>1 << (2 * q)) - 1  # all valid bits for a q-gram
    cdef uint64 qgram = _first_qgram_2bit(seq[:q]) # create first q-gram
    cdef char base
    yield qgram # return first qrgam
    for item in seq[q:]:
        # shift the q-gram by two. Remove shifted sentinel by AND-ing with the valid bits mask
        # and add the sentinel back in by OR-ing with the sentinel mask overwriting the base
        # shifted out of the q-gram. 
        # Then query the dict for the the new base and OR it into the gram.
        # (overwriting the shifted in zeroes)
        base = _2bit_from_any_with_iupac_replacement[item]
        qgram = (((qgram << 2) & valid_bits_mask) | sentinel_bits) | base
        yield qgram

def _2bit_qgrams_with_shape(object seq, Shape shp, bint sentinel=False):
    """Create 2bit encoded q-grams from a sequence.

    Warning:
        This only works for q < 32.
        Also this can suffer greatly in performance on 32bit systems.

    Arguments:
        seq (Iterable): Any dinopy sequence.
        shp (Shape): Shape of the q-grams to be created.

    Yields:
        uint64: 2bit encoded q-grams generated from the sequence.
    """
    cdef int q = len(shp)
    cdef uint64 sentinel_bits = <uint64>3 << (2 * q) if sentinel else 0  # mask for the two sentinel bits
    cdef uint64 valid_bits_mask = (<uint64>1 << (2 * (q + 1))) - 1 if sentinel else (<uint64>1 << (2 * q)) - 1  # all valid bits for a q-gram
    cdef uint64 qgram = _first_qgram_2bit(seq[:q])  # initialize qgram with sentinel bits
    cdef char base
    # WIP: avoid calls to apply_shape by using "gapshift"
    # cdef list care_indices = shp.index_shape_care
    # cdef list runlengths = [b - a  - 1 for (a, b) in zip(care_indices[:len(care_indices) - 1], care_indices[1:])]
    yield _apply_shape_int(qgram, shp, 2)

    for item in seq[q:]:
        # shift the q-gram by two. Remove shifted sentinel by AND-ing with the valid bits mask
        # and add the sentinel back in by OR-ing with the sentinel mask overwriting the base
        # shifted out of the q-gram.
        # Then query the dict for the the new base and OR it into the gram.
        # (overwriting the shifted in zeroes)
        base = _2bit_from_any_with_iupac_replacement[item]
        qgram = (((qgram << 2) & valid_bits_mask) | sentinel_bits) | base
        yield _apply_shape_int(qgram, shp, 2, sentinel)

cpdef uint64 _first_qgram_4bit(object seq, bint sentinel=False):
    """Encode the given sequence using 4bit encoding.

    Arguments:
        seq(object): Any dinopy sequence (see dtype).

    Returns:
        uint64: The 4bit encoded q-gram.
    """
    cdef uint64 qgram = 0b1111 if sentinel else 0  # initialize q-gram with sentinel bits
    cdef int base
    for item in seq:
        base = _4bit_from_any[item]
        qgram = (qgram << 4) | base
    return qgram

def _4bit_qgrams(object seq, int q, bint sentinel=False):
    """Create 4bit encoded q-grams from a sequence.

    Warning:
        This only works for full shapes and q < 16.
        Also this can suffer greatly in performance on 32bit systems.

    Arguments:
        seq (Iterable): Any dinopy sequence.
        q (int): Length of the q-grams to be created.

    Yields:
        long: 4bit encoded q-grams generated from the sequence.
    """
    cdef long sentinel_bits = <uint64>0b1111 << (4*q) if sentinel else 0  # mask for the two sentinel bits
    cdef uint64 valid_bits_mask = (<uint64>1 << (4 * (q + 1))) - 1 if sentinel else (<uint64>1 << (4 * q)) - 1  # all valid bits for a q-gram
    cdef uint64 qgram = _first_qgram_4bit(seq[:q]) # create first q-gram
    cdef char base
    yield qgram # return first qrgam
    for item in seq[q:]:
        # shift the q-gram by four. remove shifted sentinel by XOR-ing shifted sentinel
        # add in sentinel by OR-ing in the mask, overwriting the base shifted out of
        # the q-gram. Then query the dict for the base for the new base and OR it into
        # the gram. (overwriting the shifted in zeroes)
        base = _4bit_from_any[item]
        qgram = (((qgram << 4) & valid_bits_mask) | sentinel_bits) | base
        yield qgram

def _4bit_qgrams_with_shape(object seq, Shape shp, bint sentinel=False):
    """Create 4bit encoded q-grams from a sequence.

    Warning:
        This only works for q < 16.
        Also this can suffer greatly in performance on 32bit systems.

    Arguments:
        seq (Iterable): Any dinopy sequence.
        shp (Shape): Shape of the q-grams to be created.

    Yields:
        long: 4bit encoded q-grams generated from the sequence.
    """
    cdef int q = len(shp)
    cdef long sentinel_bits = <uint64>0b1111 << (4*q) if sentinel else 0  # mask for the two sentinel bits
    cdef uint64 valid_bits_mask = (<uint64>1 << (4 * (q + 1))) - 1 if sentinel else (<uint64>1 << (4 * q)) - 1  # all valid bits for a q-gram
    cdef uint64 qgram = _first_qgram_4bit(seq[:q]) # create first q-gram
    cdef char base
    # cdef list care_indices = shp.index_shape_care
    # cdef list runlengths = [b - a  - 1 for (a, b) in zip(care_indices[:len(care_indices) - 1], care_indices[1:])]
    yield _apply_shape_int(qgram, shp, 4)

    for item in seq[q:]:
        # shift the q-gram by four. Remove shifted sentinel by AND-ing with the valid bits mask
        # and add the sentinel back in by OR-ing with the sentinel mask overwriting the base
        # shifted out of the q-gram.
        # Then query the dict for the the new base and OR it into the gram.
        # (overwriting the shifted in zeroes)
        base = _4bit_from_any[item]
        qgram = (((qgram << 4) & valid_bits_mask) | sentinel_bits) | base
        yield _apply_shape_int(qgram, shp, 4, sentinel)

def replace_ambiguities(object seq, object random_choice=choice):
    """Replace each occurence of a IUPAC code in ``seq`` randomly by one of its corresponding bases.
    For ``bytearrays``, this will happen in-place, while for ``str``, ``bytes`` or ``int``/``long`` a new copy
    (with all ambiguities resolved) will be created.

    Args:
        seq: The sequence in which each IUPAC code is to be replaced by one of the bases A, C, G or T.
        random_choice (Collection → Item): A function which for a given collection of bases selects exactly one
          of those bases. Defaults to `random.choice <https://docs.python.org/3/library/random.html#random.choice>`_ which will sample uniformly from the collection.

    Returns:
        (A copy of) the sequence in which all IUPAC codes have been randomly replaced with one of their corresponding bases.

    """
    if isinstance(seq, bytearray):  # inplace replacement
        for i, item in enumerate(seq):
            if item in _iupac_mapping:
                seq[i] = random_choice(_iupac_mapping[item])
        return seq  # Note that we actually modified seq inplace, so strictly speaking there's no need to return the reference again
    elif isinstance(seq, str):
        return "".join(random_choice(_iupac_mapping[item]) if item in _iupac_mapping else item for item in seq)
    elif isinstance(seq, bytes):
        return bytes([random_choice(_iupac_mapping[item]) if item in _iupac_mapping else item for item in seq])
    elif isinstance(seq, (int, long)):
        raise TypeError("Unsupported sequence type {}.".format(type(seq)))
    else:
        raise TypeError("Unsupported sequence type {}.".format(type(seq)))


# Complement functions
################################################################################

@cython.wraparound(False)
cpdef reverse_complement(object seq):
    """Compute the reverse complement of a sequence.

    Arguments:
        seq (Iterable): sequence of which the reverse complement is to be computed.

    Returns:
        The reverse complement of the sequence.
    """
    return _reverse_complement(seq)

@cython.wraparound(False)
cdef object _reverse_complement(object seq):
    """Return the reverse complement of a DNA sequence."""
    cdef object t = reversed(seq)
    cdef list rc = [_complement[x] for x in t]
    if isinstance(seq, (str, unicode)):
        return "".join(rc)  # join the elements into a string
    else:
        return bytes(rc)

# masks used for quick 2-bit wise reversal of a given uint64
# the nonexistent cmask1 has every other bit set (i.e. 0b101010101010...)
# while cmask2 looks like (0b11001100...) etc.
cdef uint64 cmask2 = 0x3333333333333333, cmask4 = 0x0F0F0F0F0F0F0F0F, cmask8 = 0x00FF00FF00FF00FF, cmask16 = 0x0000FFFF0000FFFF, cmask32 = 0x00000000FFFFFFFF
cdef inline uint64 word_reverse_complement(uint64 w, unsigned int seq_length):
    w = ((w >> 2)  & cmask2) | ((w & cmask2) << 2)
    w = ((w >> 4)  & cmask4) | ((w & cmask4) << 4)
    w = ((w >> 8)  & cmask8) | ((w & cmask8) << 8)
    w = ((w >> 16) & cmask16) | ((w & cmask16) << 16)
    w = ( w >> 32                   ) | ( w                    << 32)
    return (~w) >> (2 * (32 - seq_length))

cpdef uint64 reverse_complement_2bit(uint64 seq, unsigned int seq_length=0, bint sentinel=False):
    """Return the reverse complement of a 2bit encoded sequence"""""
    if seq_length == 0 and sentinel == False:
        raise ValueError("TODO: proper error message.")
    if not sentinel:
        return word_reverse_complement(seq, seq_length)
    cdef uint64 mask = 0b11, reverse = 0b11 if sentinel else 0
    cdef int length = seq_length if not sentinel else seq.bit_length() / 2 - 1
    for _ in range(length):
        reverse <<= 2
        reverse |= (~(seq & mask)) & 0b11
        seq >>= 2
    return reverse

cpdef uint64 reverse_complement_4bit(uint64 seq, unsigned int seq_length=0, bint sentinel=False):
    """Return the reverse complement of a 2bit encoded sequence.

    Arguments:
        seq (uint64): 2bit encoded sequence.

    Returns:
        uint64: The 2bit encoded complement of the input sequence.
    """
    if seq_length == 0 and sentinel == False:
        raise ValueError("TODO: proper error message.")
    cdef uint64 mask = 0b1111, reverse = 0b1111 if sentinel else 0
    cdef int length = seq_length if not sentinel else seq.bit_length() / 4 - 1
    for _ in range(length):
        reverse <<= 4
        reverse |= _iupac_complement[seq & mask]
        seq >>= 4
    return reverse


@cython.wraparound(False)
cpdef object complement(object seq):
    """Compute the complement of a sequence.

    Arguments:
        seq (Iterable): sequence of which the complement is to be computed.

    Returns:
        The complement of the sequence.
    """
    return _forward_complement(seq)

@cython.wraparound(False)
cdef object _forward_complement(object seq):
    """Return the complement of a DNA sequence."""
    cdef list complement = [_complement[base] for base in seq]
    if isinstance(seq, (str, unicode)):
        return "".join(complement)  # join the elements into a string
    else:
        return bytes(complement)

cdef uint64* BVAL = [0, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4]

cdef unsigned char msb64(uint64 x):  # taken from https://stackoverflow.com/questions/2589096/find-most-significant-bit-left-most-that-is-set-in-a-bit-array
    """Calculates the position of the most significant bit in given 64bit integer.
    Used instead of `int.bit_length`.

    Args:
        x:

    Returns:

    """
    cdef uint64 mask32 = 0xFFFFFFFF00000000, mask16 = 0x00000000FFFF0000  # defining these avoids python int ←→ unsigned long long calls
    cdef unsigned char r = 0
    if x & mask32:
        r += 32
        x >>= 32
    if x & mask16:
        r += 16
        x >>= 16
    if x & 0x000000000000FF00:
        r += 8
        x >>= 8
    if x & 0x00000000000000F0:
        r += 4
        x >>= 4
    return r + BVAL[x]

cpdef uint64 complement_2bit(uint64 seq, unsigned int seq_length=0, bint sentinel=False):
    """Return the complement of a 2bit encoded sequence.

    Arguments:
        seq (uint64): 2bit encoded sequence.

    Returns:
        uint64: The 2bit encoded complement of the input sequence.
    """
    if seq_length == 0 and sentinel == False:
        raise ValueError("TODO: proper error message.")
    cdef unsigned int length = msb64(seq)
    cdef uint64 mask = (0b1 << (length if sentinel else 2 * seq_length)) - 1
    cdef uint64 sentinel_bits = 0b11 << (length - 2)
    # invert all bits and cut off all bits higher than the target number
    # i.e. length of the input bitmask (-2 for sentinel bits, if any)
    cdef uint64 reverse = ~seq & mask
    if sentinel:  # add the sentinel bits back in
        reverse |= sentinel_bits
    return reverse

cpdef uint64 complement_4bit(uint64 seq, unsigned int seq_length=0, bint sentinel=False):
    """Return the reverse complement of a 4bit encoded sequence

    Arguments:
        seq (uint64): 4bit encoded sequence.

    Returns:
        uint64: The 4bit encoded complement of the input sequence.
    """
    if seq_length == 0 and sentinel == False:
        raise ValueError("TODO: proper error message.")
    cdef unsigned int length = msb64(seq)
    cdef uint64 mask = (0b1 << (length if sentinel else 4 * seq_length)) - 1
    cdef uint64 sentinel_bits = 0b1111 << (length - 4)
    # invert all bits and cut off all bits higher than the target number
    # i.e. length of the input bitmask (-2 for sentinel bits, if any)
    cdef uint64 reverse = ~seq & mask
    if sentinel:  # add the sentinel bits back in
        reverse |= sentinel_bits
    return reverse

cpdef np.uint64_t[:] suffix_array(object sequence):
    """Calculates the suffix array of given sequence using the induced sorting algorithm as specified
    in `this paper <https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/ge-nong/Two%20Efficient%20Algorithms%20for%20Linear%20Time%20Suffix%20Array%20Construction.pdf>`_.

    Arguments:
        sequence (str, bytes, bytearray): Currently only supports sequences whose values can be interpreted as
         integers in the range of 0-255. String arguments will be coerced to ``bytes`` using :code:`string.encode('ascii')`.
         **Important**: The sequence *must* be terminated with a so called *sentinel* (a unique value smaller than any
         other value of the sequence). If the sequence does not end with a nul-byte (i.e ``b'\\x00'``) it will be added *automatically*.
         That means your sequence's length is increased by one, which in turn means that the very first item of the resulting suffix array
         will be equal the number of items in the sequence + 1 (as ``b'\x00'`` always is the lexicographically smallest suffix).


    Returns:
        A typed memoryview of 64 bit integers resembling the suffix array for the given sequence.
        Note that this is 'overkill' for short sequences, as resulting values
        are in the range of (0, len(sequence) - 1).
    """
    cdef:
        bytes seq
        int* sa_ptr
        np.uint64_t[:] result = np.empty(len(sequence) + (1 if sequence[-1] != 0 else 0), dtype=np.uint64)
    if isinstance(sequence, str):
        seq = sequence.encode('ascii')
    elif isinstance(sequence, bytes):
        seq = sequence
    elif isinstance(sequence, bytearray):
        seq = bytes(sequence)
    else:
        try:
            seq = sequence
        except TypeError as te:
            raise te
    if seq[-1] != 0:
        seq += b'\x00'
    sa_ptr = wrap_sais.suffix_array(seq)
    for i in range(len(seq)):  # FIXME can we avoid creating a copy?
        result[i] = sa_ptr[i]

    PyMem_Free(sa_ptr)
    return result
