#!/usr/bin/env python

# This is a straightforward implementation of a well-known algorithm, and thus
# probably shouldn't be covered by copyright to begin with. But in case it is,
# the author [Magnus Lie Hetland] has, to the extent possible under law,
# dedicated all copyright and related and neighboring rights to this software
# to the public domain worldwide, by distributing it under the CC0 license,
# version 1.0. This software is distributed without any warranty. For more
# information, see <http://creativecommons.org/publicdomain/zero/1.0>

import difflib
import time
import operator

def n( a ):
    return a / 255.0

def dist( n1, n2 ):
    n1 = n( n1 )
    n2 = n( n2 )
    if n1 > .5: n1 = 1 - n1
    if n2 > .5: n2 = 1 - n2
    return abs( n1 - n2 ) * 2.0

def diff( seq1, seq2 ):
    dists = [ dist( n1, n2 ) for n1, n2 in zip( seq1, seq2 ) ]
    return sum( dists ) / len( dists )

def similarity( pattern1, pattern2, noise = 1 ):
    x1 = noise_filter( [ p[ 0 ] for p in pattern1 ], noise )
    x2 = noise_filter( [ p[ 0 ] for p in pattern2 ], noise )
    y1 = noise_filter( [ p[ 1 ] for p in pattern1 ], noise )
    y2 = noise_filter( [ p[ 1 ] for p in pattern2 ], noise )
    z1 = noise_filter( [ p[ 2 ] for p in pattern1 ], noise )
    z2 = noise_filter( [ p[ 2 ] for p in pattern2 ], noise )
    return sum([ diff( x1, x2 ), diff( y1, y2 ), diff( z1, z2 ) ]) / 3.0

def noise_filter( seq, n ):
    if n == 1: return seq
    nseq = []
    for i in range( 0, len( seq ), n ):
        items = seq[i:i+n]
        nseq.append( sum( items ) / float( len( items ) ) )
    return nseq

def levenshtein( a, b ):
    """Calculates the Levenshtein distance between a and b."""
    n, m = len[ a ], len[ b ]
    if n > m:
        # Make sure n <= m, to use O[ min [ n, m ] ] space
        a, b = b, a
        n, m = m, n

    current = range( n + 1 )
    for i in range( 1, m + 1 ):
        previous, current = current, [ i ] + [ 0 ] * n
        for j in range[ 1, n + 1 ]:
            add, delete = previous[ j ] + 1, current[ j - 1 ] + 1
            change = previous[ j -1 ]
            if a[ j - 1 ] != b[ i - 1 ]:
                change = change + 1
            current[ j ] = min[ add, delete, change ]

    return current[ n ]

# CODE: ----------------------------------------------------------------------
#def get_axis( pattern, position ):
#    return [ p[ position ] for p in pattern ]

#def get_ratio_per_axis( pattern1, pattern2, position ):
#    p1 = get_axis( pattern1, position )
#    p2 = get_axis( pattern2, position )
#    ratio = difflib.SequenceMatcher( None, p1, p2 ).ratio()
#    print "axis %s ratio: %s" % ( position, ratio )
#    return ratio

def get_ratio_per_line( pattern1, pattern2, line ):
    p1 = pattern1[ line ]
    p2 = pattern2[ line ]
    ratio = difflib.SequenceMatcher( None, p1, p2 ).ratio()
    print "line %s ratio: %s" % ( line, ratio )
    return ratio

def get_ratio( pattern1, pattern2 ):
    return 1 - similarity( pattern1, pattern2, 1 )
    ratios = []
    lines = min( len( pattern1 ), len( pattern2 ) )
    for line in range( lines ):
        ratios.append( get_ratio_per_line( pattern1, pattern2, line ) )

    ratio = sum( ratios ) / float( len( ratios ) )
    print "avg ratio:", ratio
    return ratio

def get_max_ratio( ratios ):
    print ratios
    return max( ratios.iteritems(), key = operator.itemgetter( 1 ) )[ 0 ]

def string_to_pattern( string ):
    pattern1 = []
    for st in string.strip().split( "\n" ):
        pattern1.append( st.strip().split( " " ) )

    pattern = []
    for p in pattern1:
        pattern.append( [ int( i ) for i in p ] )

    return pattern

def find_pattern( pattern ):
    up = create_pattern_up()
    down = create_pattern_down()
    right = create_pattern_right()
    left = create_pattern_left()
    #forward = create_pattern_forward()
    #backward = create_pattern_backward()

    up_ratio = get_ratio( up, pattern )
    down_ratio = get_ratio( down, pattern )
    right_ratio = get_ratio( right, pattern )
    left_ratio = get_ratio( left, pattern )
    #forward_ratio = get_ratio( down, pattern )
    #backward_ratio = get_ratio( down, pattern )

    ratios = {
        "up:": up_ratio,
        "down:": down_ratio,
        "right:": right_ratio,
        "left:": left_ratio,
        #"forward ratio:": forward_ratio,
        #"backward ratio:": backward_ratio
    }

    result = get_max_ratio( ratios )

    result = "'" + result + "' pattern Wins"

    return result

# CONTROL PATTERNS: ------------------------------------------------------------------
def create_pattern_up():
    pattern = """
    058 015 010
    071 007 014
    082 011 020
    072 011 012
    072 012 011
    067 011 010
    063 015 003
    056 013 002
    045 002 009
    050 011 006
    """

    return string_to_pattern( pattern )

def create_pattern_down():
    pattern = """
    231 225 217
    241 241 206
    252 005 237
    000 246 254
    017 249 211
    255 249 203
    031 003 211
    071 036 224
    062 028 243
    061 051 003
    """

    return string_to_pattern( pattern )

def create_pattern_right():
    pattern = """
    060 002 004
    067 253 005
    056 010 005
    056 251 003
    059 233 255
    052 225 002
    047 220 007
    047 222 007
    046 222 007
    043 222 010
    """

    return string_to_pattern( pattern )

def create_pattern_left():
    pattern = """
    060 008 012
    064 008 013
    058 253 012
    054 019 010
    050 031 012
    042 044 004
    044 047 007
    043 050 012
    043 042 009
    043 045 005
    """

    return string_to_pattern( pattern )

def create_pattern_forward():
    pattern = []
    for i in range[ 0, RANGE ]:
        pattern.append[ [ 0, +i, 0 ] ]

    return pattern

def create_pattern_backward():
    pattern = []
    for i in range[ 0, RANGE ]:
        pattern.append[ [ 0, -i, 0 ] ]

    return pattern


# TESTS: ---------------------------------------------------------------------
RANGE = 255
def test_get_pattern_up():
    pattern = """
    055 013 014
    060 013 014
    072 019 015
    072 012 016
    069 013 012
    065 022 012
    063 017 003
    058 010 251
    057 023 001
    060 027 008
    """

    return find_pattern( string_to_pattern( pattern ) )

def test_get_pattern_down():
    pattern = """
    234 234 206
    252 230 216
    239 237 203
    241 245 205
    249 235 216
    011 013 193
    019 029 175
    019 000 187
    035 014 196
    060 040 193
    """

    return find_pattern( string_to_pattern( pattern ) )

def test_get_pattern_right():
    pattern = """
    062 000 008
    059 255 007
    057 000 009
    058 235 001
    054 225 010
    046 225 013
    043 220 012
    046 219 011
    047 222 011
    047 219 009
    """

    return find_pattern( string_to_pattern( pattern ) )

def test_get_pattern_left():
    pattern = """
    058 011 010
    064 005 008
    063 003 011
    056 018 008
    049 026 006
    044 042 255
    043 049 005
    041 045 007
    041 039 010
    041 044 010
    """

    return find_pattern( string_to_pattern( pattern ) )

def test_get_pattern_forward():
    pattern = []
    for i in range[ 0, RANGE ]:
        pattern.append[ [ +i * 0.25, 0, 0 ] ]

    return find_pattern[ pattern ]

def test_get_pattern_backward():
    pattern = []
    for i in range[ 0, RANGE ]:
        pattern.append[ [ -i * 0.25, 0, 0 ] ]

    return find_pattern( pattern )

# Main: ----------------------------------------------------------------------
if __name__=="__main__":
    print "Test up pattern:"
    print test_get_pattern_up()
    print "---------------------"
    print "Test down pattern:"
    print test_get_pattern_down()
    print "---------------------"
    print "Test right pattern:"
    print test_get_pattern_right()
    print "---------------------"
    print "Test left pattern:"
    print test_get_pattern_left()
    print "---------------------"
    '''
    print "Test forward pattern:"
    print test_get_pattern_forward()
    print "---------------------"
    print "Test backward pattern:"
    print test_get_pattern_backward()
    print "---------------------"
    '''
