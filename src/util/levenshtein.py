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

'''
def levenshtein[ a, b ]:
    """Calculates the Levenshtein distance between a and b."""
    n, m = len[ a ], len[ b ]
    if n > m:
        # Make sure n <= m, to use O[ min [ n, m ] ] space
        a, b = b, a
        n, m = m, n

    current = range[ n + 1 ]
    for i in range[ 1, m + 1 ]:
        previous, current = current, [ i ] + [ 0 ] * n
        for j in range[ 1, n + 1 ]:
            add, delete = previous[ j ] + 1, current[ j - 1 ] + 1
            change = previous[ j -1 ]
            if a[ j - 1 ] != b[ i - 1 ]:
                change = change + 1
            current[ j ] = min[ add, delete, change ]

    return current[ n ]
'''
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

# PATTERNS: ------------------------------------------------------------------
def create_pattern_up():
    pattern = """
    043 041 029
    080 064 018
    088 066 011
    082 067 004
    062 049 239
    042 034 225
    017 024 208
    004 016 201
    003 011 211
    254 000 211
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
    014 011 233
    037 007 187
    041 029 227
    050 016 245
    053 019 239
    031 024 201
    036 030 200
    022 031 195
    026 019 189
    038 000 172
    """

    return string_to_pattern( pattern )

def create_pattern_left():
    pattern = """
    024 032 207
    023 051 210
    017 068 251
    016 043 213
    024 035 209
    012 003 203
    045 013 192
    027 020 195
    063 031 219
    044 032 219
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
    036 061 253
    050 074 236
    033 073 229
    041 075 221
    051 063 205
    033 042 192
    011 018 187
    241 005 206
    224 007 200
    246 244 212
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
    048 034 225
    063 035 220
    048 030 242
    047 029 217
    054 007 219
    023 017 203
    019 025 179
    043 030 204
    024 024 197
    030 053 213
    """

    return find_pattern( string_to_pattern( pattern ) )

def test_get_pattern_left():
    pattern = """
    039 053 219
    026 064 233
    015 040 221
    039 036 197
    041 025 202
    033 034 195
    055 039 193
    041 027 230
    049 040 211
    047 042 238
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
