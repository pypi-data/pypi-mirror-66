#!/usr/bin/env python
#
# test_processing_core.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

import string
import random
import datetime
import itertools as it

import pytest

import numpy  as np
import pandas as pd


import funpack.util                      as util
import funpack.processing_functions_core as core


def test_isSparse_minpres():

    size = 100
    actual_present    = [0,  0.01, 0.1, 0.5, 1]
    minpres_threshold = [0,  0.01, 0.1, 0.5, 1]

    for present, threshold in it.product(actual_present, minpres_threshold):

        data     = np.random.random(size)
        expected = present < threshold

        missing = int(round(size - present * size))
        missing = np.random.choice(range(size), missing, replace=False)
        data[missing] = np.nan

        data = pd.Series(data)

        absres  = core.isSparse(
            data, util.CTYPES.continuous, minpres=threshold * size)
        propres = core.isSparse(
            data, util.CTYPES.continuous, minpres=threshold, abspres=False)

        if expected:
            expcause = 'minpres'
            expval   =  size - len(missing)
        else:
            expcause = None
            expval   = None

        assert absres  == (expected, expcause, expval)
        assert propres == (expected, expcause, expval)

    # minpres should be ignored if
    # number of points in data is
    # less than or equal to it
    data = np.random.random(10)
    data[:2] = np.nan

    res = core.isSparse(pd.Series(data),
                         util.CTYPES.continuous,
                         minpres=9)
    assert res == (True, 'minpres', 8)

    res = core.isSparse(pd.Series(data),
                        util.CTYPES.continuous,
                        minpres=10)
    assert res == (True, 'minpres', 8)

    res = core.isSparse(pd.Series(data),
                        util.CTYPES.continuous,
                        minpres=11)
    assert res == (False, None, None)

    res = core.isSparse(pd.Series(data),
                        util.CTYPES.continuous,
                        minpres=100)
    assert res == (False, None, None)


def test_isSparse_minstd():

    actualstds = np.linspace(0, 2, 10)
    minstds    = np.linspace(0, 2, 10)

    size = 500

    for actualstd, minstd in it.product(actualstds, minstds):

        data      = np.random.randn(size) * actualstd
        data      = pd.Series(data)
        actualstd = data.std()
        expected  = actualstd <= minstd

        result = core.isSparse(data, util.CTYPES.continuous,
                               minstd=minstd)
        if expected:
            assert result[:2] == (expected, 'minstd')
            assert np.isclose(result[2], actualstd)


def test_isSparse_maxcat():

    size          = 20
    actualmaxcats = np.arange(1, 21, 2)
    maxcats       = np.arange(1, 21, 2)

    dtypes = [util.CTYPES.integer,
              util.CTYPES.categorical_single,
              util.CTYPES.categorical_multiple]

    # test should only be applied
    # for integer/categoricals
    data = pd.Series(np.arange(size))
    result = core.isSparse(data, util.CTYPES.continuous, maxcat=1)
    assert result == (False, None, None)

    # threshold should be ignored if
    # bigger than size of data set
    data[:] = 123
    result = core.isSparse(data, util.CTYPES.integer, maxcat=25)
    assert result == (False, None, None)

    for actualmaxcat, maxcat in it.product(actualmaxcats, maxcats):

        data = np.arange(size)
        data[:actualmaxcat] = size + 1

        data = pd.Series(data)

        expected = actualmaxcat >= maxcat

        if expected:
            expected = (expected, 'maxcat', actualmaxcat)
        else:
            expected = (expected, None, None)

        for dt in dtypes:

            maxcatprop = maxcat / len(data)

            resultabs  = core.isSparse(data, dt, maxcat=maxcat)
            resultprop = core.isSparse(data, dt, maxcat=maxcatprop,
                                       abscat=False)

            assert resultabs  == expected
            assert resultprop == expected

    # when maxcat is a proportion, test should ignore nans
    data        = np.zeros(100, dtype=np.float)
    data[:40]   = np.nan
    data[40:80] = 1
    data        = pd.Series(data)
    assert core.isSparse(data, None, maxcat=0.5, abscat=False) == \
        (True, 'maxcat', 40)
    assert core.isSparse(data, None, maxcat=0.6, abscat=False) == \
        (True, 'maxcat', 40)
    assert core.isSparse(data, None, maxcat=0.7, abscat=False) == \
        (False, None, None)


def test_isSparse_mincat():

    size          = 100
    actualmincats = np.arange(1, 21, 2)
    mincats       = np.arange(1, 21, 2)

    dtypes = [util.CTYPES.integer,
              util.CTYPES.categorical_single,
              util.CTYPES.categorical_multiple]

    # test should only be applied
    # for integer/categoricals
    data     = np.zeros(size)
    data[:5] = size + 1
    data     = pd.Series(data)
    result   = core.isSparse(data, util.CTYPES.continuous,
                             mincat=2)
    assert result == (False, None, None)

    # threshold should be ignored if
    # bigger than size of data set
    data[:] = size + 1
    result = core.isSparse(data, util.CTYPES.integer, mincat=size + 5)
    assert result == (False, None, None)

    for actualmincat, mincat in it.product(actualmincats, mincats):

        data = np.zeros(size)
        data[:actualmincat] = size + 1

        data = pd.Series(data)

        if actualmincat < mincat:
            expected = (True, 'mincat', actualmincat)
        else:
            expected = (False, None, None)

        for dt in dtypes:

            mincatprop = mincat / len(data)

            resultabs  = core.isSparse(data, dt, mincat=mincat)
            resultprop = core.isSparse(data, dt, mincat=mincatprop,
                                       abscat=False)

            assert resultabs  == expected
            assert resultprop == expected

    # when mincat is a proportion, test should ignore nans
    data        = np.zeros(100, dtype=np.float)
    data[:40]   = np.nan
    data[40:60] = 1
    data        = pd.Series(data)
    assert core.isSparse(data, None, mincat=0.1, abscat=False) == \
        (False, None, None)
    assert core.isSparse(data, None, mincat=0.2, abscat=False) == \
        (False, None, None)
    assert core.isSparse(data, None, mincat=0.3, abscat=False) == \
        (False, None, None)
    assert core.isSparse(data, None, mincat=0.4, abscat=False) == \
        (True, 'mincat', 20)


def test_isSparse_non_numeric():


    data     = list(np.random.randint(1, 10, 100))
    data[50] = 'abcde'
    data[51] = np.nan
    data     = pd.Series(data)
    assert core.isSparse(data, minstd=10) == (False, None, None)

    data = pd.Series(['a', 'a', 'b', 'b', 'b', np.nan, np.nan])
    assert core.isSparse(data, mincat=1) == (False, None, None)
    assert core.isSparse(data, mincat=2) == (False, None, None)
    assert core.isSparse(data, mincat=3) == (True, 'mincat', 2)
    assert core.isSparse(data, maxcat=4) == (False, None, None)
    assert core.isSparse(data, maxcat=3) == (True, 'maxcat', 3)


def test_isSparse_naval():

    data = np.random.randint(1, 10, 100)
    data = pd.Series(data)

    data.iloc[:10] = -1
    assert core.isSparse(data, minpres=89, naval=-1) == (False, None,      None)
    assert core.isSparse(data, minpres=90, naval=-1) == (False, None,      None)
    assert core.isSparse(data, minpres=91, naval=-1) == (True,  'minpres', 90)

    # nan is not missing
    data.iloc[:10] = np.nan
    assert core.isSparse(data, minpres=91, naval=-1) == (False, None, None)

    # non-numeric
    data = random.choices(string.ascii_lowercase, k=100)
    data = pd.Series(data)

    data.iloc[:10] = 'A'
    assert core.isSparse(data, minpres=89, naval='A') == (False, None,      None)
    assert core.isSparse(data, minpres=90, naval='A') == (False, None,      None)
    assert core.isSparse(data, minpres=91, naval='A') == (True,  'minpres', 90)
    data.iloc[:10] = np.nan
    assert core.isSparse(data, minpres=91, naval='A') == (False, None, None)

    # mixed type
    data.iloc[:10] = 0
    assert core.isSparse(data, minpres=91, naval=0) == (True,  'minpres', 90)


def test_isSparse_date():

    data = []
    for i in range(100):
        data.append(datetime.date(2020,
                                  np.random.randint(1, 13),
                                  np.random.randint(1, 29)))

    data = pd.Series(data)

    data.iloc[:10] = np.nan
    assert core.isSparse(data, minpres=89) == (False, None,      None)
    assert core.isSparse(data, minpres=90) == (False, None,      None)
    assert core.isSparse(data, minpres=91) == (True,  'minpres', 90)



def test_redundantColumns():

    size    = 50
    series1 = np.sin(np.linspace(0, np.pi * 6, size))
    series2 = series1 + np.random.random(size)
    corr = pd.Series(series1).corr(pd.Series(series2))

    data = pd.DataFrame({0 : pd.Series(series1), 1 : pd.Series(series2)})
    cols = [(0, 1)]

    assert core.redundantColumns(data, cols, corr * 1.01) == []
    assert core.redundantColumns(data, cols, corr * 0.99) == [1]

    # insert some missing values, making
    # sure there are more missing values
    # in series2, and the missingness will
    # be positively correlated
    s1miss = np.random.choice(
        np.arange(size, dtype=np.int), 10, replace=False)
    s2miss = list(s1miss)
    while len(s2miss) < 13:
        idx = np.random.randint(0, size, 1)
        if idx not in s1miss:
            s2miss.append(idx)
    s2miss = np.array(s2miss, dtype=np.int)

    series1[s1miss] = np.nan
    series2[s2miss] = np.nan

    corr   = pd.Series(series1).corr(pd.Series(series2))
    nacorr = np.corrcoef(np.isnan(series1), np.isnan(series2))[0, 1]

    data = pd.DataFrame({0 : pd.Series(series1), 1 : pd.Series(series2)})

    assert core.redundantColumns(data, cols, corr * 1.01) == []
    assert core.redundantColumns(data, cols, corr * 0.99) == [1]

    # both present and missing values must
    # be above the threshold for the column
    # to be considered redundant
    assert core.redundantColumns(data, cols, corr * 0.99, nacorr * 0.99) == [1]
    assert core.redundantColumns(data, cols, corr * 1.01, nacorr * 0.99) == []
    assert core.redundantColumns(data, cols, corr * 0.99, nacorr * 1.01) == []
    assert core.redundantColumns(data, cols, corr * 1.01, nacorr * 1.01) == []

    # the column with more missing values
    # should be the one flagged as redundant
    data = pd.DataFrame({0 : pd.Series(series2), 1 : pd.Series(series1)})
    assert core.redundantColumns(data, cols, corr * 1.01)                == []
    assert core.redundantColumns(data, cols, corr * 0.99)                == [0]
    assert core.redundantColumns(data, cols, corr * 0.99, nacorr * 0.99) == [0]
    assert core.redundantColumns(data, cols, corr * 1.01, nacorr * 0.99) == []
    assert core.redundantColumns(data, cols, corr * 0.99, nacorr * 1.01) == []
    assert core.redundantColumns(data, cols, corr * 1.01, nacorr * 1.01) == []


def test_redundantColumns_associative():
    a        = np.random.randint(1, 100, 100).astype(np.float32)
    b        = np.copy(a)
    c        = np.copy(a)

    # assuminng that this is enough to guarantee
    # corr(a,b) > corr(a,c) < corr(b,c)
    b[::25]  = np.random.randint(1, 100, 4)
    c[::4]   = np.random.randint(1, 100, 25)

    # make sure that a is always selected over b
    # and b is always selected over c
    b[-1]    = np.nan
    c[-2:]   = np.nan
    df       = pd.DataFrame({'a' : a, 'b' : b, 'c' : c})

    corrmat  = df.corr()
    abthres  = corrmat.loc['a', 'b']
    bcthres  = corrmat.loc['b', 'c']

    # result should be the same regardless of column order
    for colorder in it.permutations('abc', 3):
        df = df[list(colorder)]
        colpairs = list(it.combinations(df.columns, 2))

        assert        core.redundantColumns(df, colpairs,  abthres * 1.05)         == []
        assert        core.redundantColumns(df, colpairs, (abthres + bcthres) / 2) == ['b']
        assert sorted(core.redundantColumns(df, colpairs,  bcthres * 0.95))        == ['b', 'c']


def test_binariseCategorical():

    data = np.random.randint(1, 10, (100, 10))
    cols = {str(i + 1) : data[:, i] for i in range(10)}
    df   = pd.DataFrame(cols)

    bindata, uniq = core.binariseCategorical(df)

    assert sorted(uniq) == sorted(np.unique(data))

    for i, v in enumerate(uniq):
        exp = np.any(data == v, axis=1)
        assert np.all(bindata[:, i] == exp)

    data[data == 5] = 6
    data[:10, 0] = 5
    cols = {str(i + 1) : data[:, i] for i in range(10)}
    df   = pd.DataFrame(cols)

    bindata, uniq = core.binariseCategorical(df, minpres=11)

    assert sorted(uniq) == [1, 2, 3, 4, 6, 7, 8, 9]

    for i, v in enumerate(uniq):
        exp = np.any(data == v, axis=1)
        assert np.all(bindata[:, i] == exp)


def test_binariseCategorical_missing():

    data = np.full((50, 5), np.nan)

    for i in range(data.shape[1]):
        namask = np.random.random(data.shape[0]) < 0.1
        data[~namask, i] = np.random.randint(1, 10, (~namask).sum())

    expuniq = list(sorted(np.unique(data[~np.isnan(data)])))

    expdata = np.zeros((data.shape[0], len(expuniq)))

    for i, v in enumerate(expuniq):
        expdata[:, i] = np.any(data == v, axis=1)

    cols = {str(i + 1) : data[:, i] for i in range(data.shape[1])}
    df   = pd.DataFrame(cols)

    gotdata, gotuniq = core.binariseCategorical(df)
    assert np.all(gotuniq == expuniq)
    assert np.all(gotdata == expdata)


def test_binariseCategorical_take():
    data = np.full((10, 5), np.nan)
    aux  = np.full((10, 5), np.nan)

    for i in range(data.shape[1]):
        namask = np.random.random(data.shape[0]) < 0.7
        data[~namask, i] = np.random.randint(1, 10, (~namask).sum())

    mask      = np.isfinite(data)
    aux[mask] = np.random.randint(1, 100, data.shape)[mask]

    expuniq = list(sorted(np.unique(data[~np.isnan(data)])))

    expdata = np.full((data.shape[0], len(expuniq)), np.nan)

    for i, v in enumerate(expuniq):
        rows, cols = np.where(data == v)
        for r in range(data.shape[0]):
            if r not in rows:
                continue
            c = cols[np.where(rows == r)[0][0]]
            expdata[r, i] = aux[r, c]

    cols = {str(i + 1) : data[:, i] for i in range(data.shape[1])}
    df   = pd.DataFrame(cols)

    cols = {str(i + 1) : aux[:, i] for i in range(aux.shape[1])}
    adf  = pd.DataFrame(cols)

    gotdata, gotuniq = core.binariseCategorical(df, take=adf)

    gotna = pd.isnull(gotdata)
    expna = pd.isnull(expdata)

    assert np.all(gotuniq         == expuniq)
    assert np.all(gotna           == expna)
    assert np.all(gotdata[~gotna] == expdata[~expna])



def test_binariseCategorical_take_error():

    data = pd.DataFrame(np.random.randint(1, 10, (100, 10)))
    take = pd.DataFrame(np.random.randint(1, 10, (100, 9)))

    with pytest.raises(ValueError):
        core.binariseCategorical(data, take=take)


def test_expandCompound():

    data = []

    for i in range(20):
        rlen = np.random.randint(1, 20)
        row = np.random.randint(1, 100, rlen)
        data.append(row)

    exp = np.full((20, max(map(len, data))), np.nan)

    for i in range(20):
        exp[i, :len(data[i])] = data[i]

    series = pd.Series(data)

    got = core.expandCompound(series)

    expna = np.isnan(exp)
    gotna = np.isnan(got)

    assert np.all(     expna  ==      gotna)
    assert np.all(exp[~expna] == got[~gotna])
