#!/usr/bin/env python

# This is a straightforward implementation of a well-known algorithm, and thus
# probably shouldn't be covered by copyright to begin with. But in case it is,
# the author [Magnus Lie Hetland] has, to the extent possible under law,
# dedicated all copyright and related and neighboring rights to this software
# to the public domain worldwide, by distributing it under the CC0 license,
# version 1.0. This software is distributed without any warranty. For more
# information, see <http://creativecommons.org/publicdomain/zero/1.0>

import difflib
import operator

# CODE: ----------------------------------------------------------------------
class MuscleOps( object ):

    def gesture( self, pattern ):
        return self.find_pattern( self.string_to_int( pattern ) )

    def n( self, a ):
        return a / 255.0

    def dist( self, n1, n2 ):
        n1 = self.n( n1 )
        n2 = self.n( n2 )
        if n1 > .5: n1 = 1 - n1
        if n2 > .5: n2 = 1 - n2
        return abs( n1 - n2 ) * 2.0

    def diff( self, seq1, seq2 ):
        dists = [ self.dist( n1, n2 ) for n1, n2 in zip( seq1, seq2 ) ]
        return sum( dists ) / len( dists )

    def similarity( self, pattern1, pattern2, noise = 1 ):
        x1 = self.noise_filter( [ p[ 0 ] for p in pattern1 ], noise )
        x2 = self.noise_filter( [ p[ 0 ] for p in pattern2 ], noise )
        y1 = self.noise_filter( [ p[ 1 ] for p in pattern1 ], noise )
        y2 = self.noise_filter( [ p[ 1 ] for p in pattern2 ], noise )
        z1 = self.noise_filter( [ p[ 2 ] for p in pattern1 ], noise )
        z2 = self.noise_filter( [ p[ 2 ] for p in pattern2 ], noise )
        return sum([ self.diff( x1, x2 ), self.diff( y1, y2 ), self.diff( z1, z2 ) ]) / 3.0

    def noise_filter( self, seq, n ):
        if n == 1: return seq
        nseq = []
        for i in range( 0, len( seq ), n ):
            items = seq[i:i+n]
            nseq.append( sum( items ) / float( len( items ) ) )
        return nseq

    def levenshtein( self, a, b ):
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

    def get_ratio_per_line( self, pattern1, pattern2, line ):
        p1 = pattern1[ line ]
        p2 = pattern2[ line ]
        ratio = difflib.SequenceMatcher( None, p1, p2 ).ratio()
        #print "line %s ratio: %s" % ( line, ratio )
        return ratio

    def get_ratio( self, pattern1, pattern2 ):
        return 1 - self.similarity( pattern1, pattern2, 1 )
        ratios = []
        lines = min( len( pattern1 ), len( pattern2 ) )
        for line in range( lines ):
            ratios.append( self.get_ratio_per_line( pattern1, pattern2, line ) )

        ratio = sum( ratios ) / float( len( ratios ) )
        #print "avg ratio:", ratio
        return ratio

    def get_max_ratio( self, ratios ):
        #print ratios
        return max( ratios.iteritems(), key = operator.itemgetter( 1 ) )[ 0 ]

    def string_to_pattern( self, string ):
        pattern1 = []
        for st in string.strip().split( "\n" ):
            pattern1.append( st.strip().split( " " ) )

        return self.string_to_int( pattern1 )

    def string_to_int( self, pattern1 ):
        pattern = []
        for p in pattern1:
            pattern.append( [ int( i ) for i in p ] )

        return pattern

    def find_pattern( self, pattern ):
        up = self.create_pattern_up()
        down = self.create_pattern_down()
        right = self.create_pattern_right()
        left = self.create_pattern_left()

        up_ratio = self.get_ratio( up, pattern )
        down_ratio = self.get_ratio( down, pattern )
        right_ratio = self.get_ratio( right, pattern )
        left_ratio = self.get_ratio( left, pattern )

        ratios = {
            "up": up_ratio,
            "down": down_ratio,
            "right": right_ratio,
            "left": left_ratio
        }

        result = self.get_max_ratio( ratios )

        return result

    # CONTROL PATTERNS: ------------------------------------------------------------------
    def create_pattern_up( self ):
        pattern = """
	059 016 008
	093 011 022
	075 015 024
	060 011 027
	036 013 028
	033 013 035
	030 019 041
	025 013 044
	009 012 038
	017 015 049
        """

        return self.string_to_pattern( pattern )

    def create_pattern_down( self ):
        pattern = """
        063 011 019
        044 020 010
        048 017 006
        043 015 249
        053 016 235
        054 015 225
        055 009 215
        058 011 205
        046 005 205
        035 000 206
        """

        return self.string_to_pattern( pattern )

    def create_pattern_right( self ):
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

        return self.string_to_pattern( pattern )

    def create_pattern_left( self ):
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

        return self.string_to_pattern( pattern )

    # TESTS: ---------------------------------------------------------------------
    RANGE = 255
    def test_get_pattern_up( self ):
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

        return self.find_pattern( self.string_to_pattern( pattern ) )

    def test_get_pattern_down( self ):
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

        return self.find_pattern( self.string_to_pattern( pattern ) )

    def test_get_pattern_right( self ):
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

        return self.find_pattern( self.string_to_pattern( pattern ) )

    def test_get_pattern_left( self ):
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

        return self.find_pattern( self.string_to_pattern( pattern ) )


# # Main: ----------------------------------------------------------------------
if __name__== "__main__":
    lev = MuscleOps()
    print "Test up pattern:"
    print lev.test_get_pattern_up()
    print "---------------------"
    print "Test down pattern:"
    print lev.test_get_pattern_down()
    print "---------------------"
    print "Test right pattern:"
    print lev.test_get_pattern_right()
    print "---------------------"
    print "Test left pattern:"
    print lev.test_get_pattern_left()
    print "---------------------"
