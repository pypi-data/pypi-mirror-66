from ldstore.parse import *

import numpy as np
import pandas as pd
import math
import sys

class bcor:
        
    ##-----------------------------------##
    ## Initialize BCOR instance          ##
    ##-----------------------------------##
    def __init__( self, fname, read_header = True ):
        self.__fname = fname
        try:
            self.__fh = open( self.__fname, 'rb' )
            self.__readHeader()
            if read_header:
                self.__readMeta()
        except IOError:
            raise
    
    ##-----------------------------------##
    ## Getters                           ##
    ##-----------------------------------##
    def getFname       ( self ): return self.__fname
    def getFsize       ( self ): return self.__fsize
    def getMeta        ( self ):
        if not hasattr( self, '__meta' ):
            self.__fh.seek( 0 )
            self.__readHeader()
            self.__readMeta  ()
        return self.__meta
    
    def getNumOfSNPs   ( self ): return self.__nSNPs
    def getNumOfSamples( self ): return self.__nSamples
    
    ##-----------------------------------##
    ## Get linear index for strictly     ##
    ## lower triangular matrix           ##
    ##-----------------------------------##
    def __getIndex( self, snp_x, snp_y ):
        if snp_x > snp_y:
            return self.__nSNPs * ( self.__nSNPs - 1 ) // 2 - ( self.__nSNPs - snp_y ) * ( ( self.__nSNPs - snp_y ) - 1 ) // 2 + snp_x - snp_y - 1
        else:
            return self.__nSNPs * ( self.__nSNPs - 1 ) // 2 - ( self.__nSNPs - snp_x ) * ( ( self.__nSNPs - snp_x ) - 1 ) // 2 + snp_y - snp_x - 1
    
    ##-----------------------------------##
    ## Read correlations for a pair      ##
    ## of SNPs                           ##
    ##-----------------------------------##
    def __readCorrPair( self, snp_x, snp_y, seek ):
        if self.__compression == 0:
            if seek:
                self.__fh.seek( np.uint64( self.__corr_block_offset + self.__getIndex( snp_x, snp_y ) * 2 ) )
            return convertIntToFloat( np.fromfile( self.__fh, np.uint16, 1 )[ 0 ], 2 ) - 1.0
        elif self.__compression == 1:
            if seek:
                self.__fh.seek( np.uint64( self.__corr_block_offset + self.__getIndex( snp_x, snp_y ) * 4 ) )
            return convertIntToFloat( np.fromfile( self.__fh, np.uint32, 1 )[ 0 ], 4 ) - 1.0
        elif self.__compression == 2:
            if seek:
                self.__fh.seek( np.uint64( self.__corr_block_offset + self.__getIndex( snp_x, snp_y ) * 8 ) )
            return convertIntToFloat( np.fromfile( self.__fh, np.uint64, 1 )[ 0 ], 8 ) - 1.0
        elif self.__compression == 3:
            if seek:
                self.__fh.seek( np.uint64( self.__corr_block_offset + self.__getIndex( snp_x, snp_y ) * 1 ) )
            return convertIntToFloat( np.fromfile( self.__fh, np.uint8, 1 )[ 0 ], 1 ) - 1.0
    
    ##-----------------------------------##
    ## Read correlations in a BCOR file  ##
    ##-----------------------------------##
    def readCorr( self, snps1, snps2 ):
        if len( snps2 ) == 0:
            return self.__readCorr( snps1 )
        else:
            return self.__readCorr2( snps1, snps2 )
    
    def __readCorr( self, snps ):
        if type( snps ) is not list:
            print( 'Need to input "snps" as a list!' )
            return
        
        if len( snps ) == 0:
            self.__fh.seek( self.__corr_block_offset )
            corr = np.identity( self.__nSNPs )
            for snp_x in range( self.__nSNPs - 1 ):
                for snp_y in range( snp_x + 1, self.__nSNPs ):
                    corr[ snp_y, snp_x ] = self.__readCorrPair( snp_x, snp_y, False )
            return np.tril( corr ) + np.triu( corr.T, 1 )
        else:
            areSNPsIncluded2( snps, self.__nSNPs, self.__fname )
            
            corr = np.zeros( [ self.__nSNPs, len( snps ) ] )
            for snp_x, index in zip( snps, range( len( snps ) ) ):
                for snp_y in range( self.__nSNPs ):
                    if snp_x == snp_y:
                        corr[ snp_y, index ] = 1.0
                    else:
                        corr[ snp_y, index ] = self.__readCorrPair( snp_x, snp_y, True )
            return corr
    
    def __readCorr2( self, snps1, snps2 ):
        if type( snps1 ) is not list:
            print( 'Need to input "snps1" as a list!' )
            return
        
        if type( snps2 ) is not list:
            print( 'Need to input "snps2" as a list!' )
            return
        
        if len( snps1 ) == 0:
            print( 'Need to input a list "snps1"!' )
            return
        
        if len( snps2 ) == 0:
            print( 'Need to input a list "snps2"!' )
            return
        
        areSNPsIncluded2( snps1, self.__nSNPs, self.__fname )
        areSNPsIncluded2( snps2, self.__nSNPs, self.__fname )
        
        corr = np.zeros( [ len( snps1 ), len( snps2 ) ] )
        for snp_x, index1 in zip( snps1, range( len( snps1 ) ) ):
            for snp_y, index2 in zip( snps2, range( len( snps2 ) ) ):
                if snp_x == snp_y:
                    corr[ index1, index2 ] = 1.0
                else:
                    corr[ index1, index2 ] = self.__readCorrPair( snp_x, snp_y, True )
        return corr
    
    ##-----------------------------------##
    ## Read header block                 ##
    ##-----------------------------------##
    def __readHeader( self ):
        magic = str( self.__fh.read( 7 ), 'utf-8' )
        if magic != 'bcor1.1':
            print( 'File "' + self.__fname + '" is not from LDStore!' )
            return
        
        self.__fsize             = np.fromfile ( self.__fh, np.uint64, 1  )[ 0 ]
        self.__nSamples          = np.fromfile ( self.__fh, np.uint32, 1  )[ 0 ]
        self.__nSNPs             = np.fromfile ( self.__fh, np.uint32, 1  )[ 0 ]
        self.__compression       = np.fromfile ( self.__fh, np.uint8,  1  )[ 0 ]
        self.__corr_block_offset = np.fromfile ( self.__fh, np.uint64, 1  )[ 0 ]
    
    ##-----------------------------------##
    ## Read meta information block       ##
    ##-----------------------------------##
    def __readMeta( self ):
        rsid       = []
        position   = np.zeros( self.__nSNPs, dtype = np.int )
        chromosome = []
        allele1    = []
        allele2    = []
        
        for snp in range( self.__nSNPs ):
            L_buffer          = np.fromfile( self.__fh, np.uint32, 1 )[ 0 ]
            index             = np.fromfile( self.__fh, np.uint32, 1 )[ 0 ]
            L_rsid            = np.fromfile( self.__fh, np.uint16, 1 )[ 0 ]
            rsid.append( str( self.__fh.read( L_rsid ), 'utf-8' ) )
            position[ snp ]   = np.fromfile( self.__fh, np.uint32, 1 )[ 0 ]
            L_chromosome      = np.fromfile( self.__fh, np.uint16, 1 )[ 0 ]
            chromosome.append( str( self.__fh.read( L_chromosome ), 'utf-8' ) )
            L_allele1         = np.fromfile( self.__fh, np.uint32, 1 )[ 0 ]
            allele1.append( str( self.__fh.read( L_allele1 ), 'utf-8' ) )
            L_allele2         = np.fromfile( self.__fh, np.uint32, 1 )[ 0 ]
            allele2.append( str( self.__fh.read( L_allele2 ), 'utf-8' ) )
            assert( L_buffer == ( 20 + L_rsid + L_chromosome + L_allele1 + L_allele2 ) )
        
        self.__meta = pd.concat( [
            pd.DataFrame( rsid,       columns = [ 'rsid'       ] ),
            pd.DataFrame( position,   columns = [ 'position'   ] ),
            pd.DataFrame( chromosome, columns = [ 'chromosome' ] ),
            pd.DataFrame( allele1,    columns = [ 'allele1'    ] ),
            pd.DataFrame( allele2,    columns = [ 'allele2'    ] )
        ], axis = 1 )
