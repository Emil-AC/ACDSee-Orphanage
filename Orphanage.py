#!/usr/bin/python
#
# Orphanage
# A tool to fill an ACDsee databse with orphans and some meta data
# This is addressed to users, who plan to use ACDSee
# with lots of image files, keywords, categories or collections,
# and who to do some stress tests.
#
# Emil 2019-10-09
#
# minimum requirement: afaik python 3.6
# I used v 3.7.2
#
# v. 0.0.1
#   initial release
# v. 0.0.2
#   reduced some similar functions
#   comments added
#   clearer naming for functions an vars

import configparser
import os
import sys
import io


# create and open a new textfile for writing
# there's currently no error handling
def createfile(path):
    return io.open(path, "w", newline="\n", encoding="utf-16")


# write the header of the text file with database version number
def header(outfile, cfg):
    version = cfg['version']
    outfile.write(f'<ACDDB Version="{version}">\n')


# finally append the footer
def footer(outfile):
    outfile.write(f'</ACDDB>')


# this one creates nested masterlist of keywords or categories
# the masterlist of collection is not supported
def masterlist(outfile, prefix, cfg):

    def item(outfile, prefix, d, c):
        outfile.write(f'<{prefix}>\n')
        outfile.write(f'<Name>{prefix}_{d:03d}_{c:06d}</Name>\n')
        outfile.write(f'<Attributes>0</Attributes>\n')  # I've never seen a different value here

    count = int(cfg['count'])
    depth = int(cfg['depth'])
    if count > 0:
        outfile.write(f'<{prefix}List>\n')
        print()
        numc = 0
        while numc < count:
            print(f'\rwriting {prefix} masterlist: {numc+1:06d}', end='')
            sys.stdout.flush()
            numd = 0
            while numd < depth-1:
                item(outfile, prefix, numd, numc)
                outfile.write(f'<{prefix}List>\n')
                numd += 1
            item(outfile, prefix, numd, numc)
            numd = 0
            while numd < depth-1:
                outfile.write(f'</{prefix}>\n')
                outfile.write(f'</{prefix}List>\n')
                numd += 1
            outfile.write(f'</{prefix}>\n')
            numc += 1
        outfile.write(f'</{prefix}List>\n')


# creates the assetlist with the folderrootlist
def assetlist(outfile, cfg):

    # add a nested keyword/categorie/collection to the catalogued item
    def list(outfile, prefix, num, depth):
        if num > 0:
            outfile.write(f'<Asset{prefix}List>\n')
            numc = 0
            while numc < num:
                kwd = f'<Asset{prefix}>'
                numd = 0
                while numd < depth-1:
                    kwd = kwd + f'{prefix}_{numd:03d}_{numc:06d}\\'
                    numd += 1
                kwd = kwd + f'{prefix}_{numd:03d}_{numc:06d}'
                numc += 1
                kwd = kwd + f'</Asset{prefix}>\n'
                outfile.write(kwd)
            outfile.write(f'</Asset{prefix}List>\n')

    # create a single catalogued item
    def item(outfile, c, cfg):
        outfile.write(f'<Asset>\n')
        outfile.write(f'<Name>item_{c:06d}</Name>\n')
        outfile.write(f'<Folder>&lt;Local\\12345678&gt;\\</Folder>\n')  # same volume label as in folderrootlist
        outfile.write(f'<FileType>Nikon RAW</FileType>\n')
        outfile.write(f'<ImageType>4605262</ImageType>\n')  # taken from a NEF raw file
        outfile.write(f'<DBDate>20190101 00:00:00.000</DBDate>\n')
        outfile.write(f'<Caption>Orphan_{c:06d}</Caption>\n')
        outfile.write(f'<Label>red</Label>\n')
        outfile.write(f'<Author>Orphanage</Author>\n')
        outfile.write(f'<Notes>Note_{c:06d}</Notes>\n')
        outfile.write(f'<Rating>1</Rating>\n')
        list(outfile, 'Keyword', int(cfg['keywords']), int(cfg['keyworddepth']))
        list(outfile, 'Category', int(cfg['categories']), int(cfg['categorydepth']))
        list(outfile, 'Collection', int(cfg['collections']), int(cfg['collectiondepth']))
        outfile.write(f'</Asset>\n')

    # create the list of catalogued items
    def itemlist(outfile, cfg):
        outfile.write(f'<AssetList>\n')
        print()
        numc = 0
        while numc < count:
            print(f'\rwriting assets: {numc+1:06d}', end='')
            sys.stdout.flush()
            item(outfile, numc, cfg)
            numc += 1
        outfile.write(f'</AssetList>\n')

    # create the folderrootlist
    def folderrootlist(outfile):
        outfile.write(f'<FolderRootList>\n')
        outfile.write(f'<FolderRoot>\n')
        outfile.write(f'<Name>O:</Name>\n')  # Drive letter O: for all Orphans
        outfile.write(f'<DiscID>12345678</DiscID>\n')
        outfile.write(f'<RootType>Local</RootType>\n')
        outfile.write(f'<SysPath>O:</SysPath>\n')
        outfile.write(f'<DBRootPath>Local\\12345678</DBRootPath>\n')
        outfile.write(f'<VolumeLabel>Volumelabel</VolumeLabel>\n')
        outfile.write(f'<FileSystemType>NTFS</FileSystemType>\n')
        outfile.write(f'</FolderRoot>\n')
        outfile.write(f'</FolderRootList>\n')

    count = int(cfg['count'])  # number of assets (catalogued items)
    if count > 0:
        itemlist(outfile, cfg)
        folderrootlist(outfile)


def doit():
    config = configparser.ConfigParser()
    config.read(os.path.dirname(__file__) + os.sep + 'config.ini')
    outfilename = sys.argv[1]
    outfile = createfile(outfilename)
    header(outfile, config['main'])
    masterlist(outfile, 'Keyword', config['keywordlist'])
    masterlist(outfile, 'Category', config['categorylist'])
    assetlist(outfile, config['assetlist'])
    footer(outfile)
    outfile.close()


if __name__ == "__main__":
    doit()
