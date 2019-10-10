#!/usr/bin/python
#
# Orphanage
# A tool to foul an ACDsee DB with Orphans and useless meta data
# This is addressed to users, who plan to use ACDSee
# with lots of image files, lots of keywords or
# many categories and who need a stress test.
#
# Emil 2019-10-09
#
# minimum requirement: afaik python 3.6
# I used v 3.7.2
#
# v. 0.0.1
#

import configparser
import os
import sys
import io


def createfile(path):
    return io.open(path, "w", newline="\n", encoding="utf-16")


def header(outfile, cfg):
    version = cfg['version']
    outfile.write(f'<ACDDB Version="{version}">\n')


def footer(outfile):
    outfile.write(f'</ACDDB>')


# this one creates a master list with nested keywords
def keywordlist(outfile, cfg):

    def keyword(d, c):
        outfile.write(f'<Keyword>\n')
        outfile.write(f'<Name>keyword_{d:02d}_{c:06d}</Name>\n')
        outfile.write(f'<Attributes>0</Attributes>\n')

    count = int(cfg['count'])
    depth = int(cfg['depth'])
    if count > 0:
        outfile.write(f'<KeywordList>\n')
        numc = 0
        print()
        while numc < count:
            print(f'\rwriting keywordlist: {numc+1:06d}', end='')
            sys.stdout.flush()
            numd = 0
            while numd < depth-1:
                keyword(numd, numc)
                outfile.write(f'<KeywordList>\n')
                numd += 1
            keyword(numd, numc)
            numd = 0
            while numd < depth-1:
                outfile.write(f'</Keyword>\n')
                outfile.write(f'</KeywordList>\n')
                numd += 1
            outfile.write(f'</Keyword>\n')
            numc += 1
        outfile.write(f'</KeywordList>\n')


# this one creates nested categories
def categorylist(outfile, cfg):

    def category(d, c):
        # outfile.write(f'{d} - {c}')
        outfile.write(f'<Category>\n')
        outfile.write(f'<Name>category_{d:02d}_{c:06d}</Name>\n')
        outfile.write(f'<Attributes>0</Attributes>\n')
        outfile.write(f'<IconID>0</IconID>\n')

    count = int(cfg['count'])
    depth = int(cfg['depth'])
    if count > 0:
        outfile.write(f'<CategoryList>\n')
        print()
        numc = 0
        while numc < count:
            print(f'\rwriting categorylist: {numc+1:06d}', end='')
            sys.stdout.flush()
            numd = 0
            while numd < depth-1:
                category(numd, numc)
                outfile.write(f'<CategoryList>\n')
                numd += 1
            category(numd, numc)
            numd = 0
            while numd < depth-1:
                outfile.write(f'</Category>\n')
                outfile.write(f'</CategoryList>\n')
                numd += 1
            outfile.write(f'</Category>\n')
            numc += 1
        outfile.write(f'</CategoryList>\n')


# this one creates nested categories
def assetlist(outfile, cfg):

    def kslist(cfg):
        keys = int(cfg['assignedkeywords'])
        depth = int(cfg['keyworddepth'])
        if keys > 0:
            outfile.write(f'<AssetKeywordList>\n')
            numc = 0
            while numc < keys:
                kwd = f'<AssetKeyword>'
                numd = 0
                while numd < depth-1:
                    kwd = kwd + f'Keyword_{numd:03d}_{numc:03d}\\'
                    numd += 1
                kwd = kwd + f'Keyword_{numd:03d}_{numc:03d}'
                numc += 1
                kwd = kwd + f'</AssetKeyword>\n'
                outfile.write(kwd)
            outfile.write(f'</AssetKeywordList>\n')

    def cylist(cfg):
        cats = int(cfg['assignedcategories'])
        depth = int(cfg['categorydepth'])
        if cats > 0:
            outfile.write(f'<AssetCategoryList>\n')
            numc = 0
            while numc < cats:
                kwd = f'<AssetCategory>'
                numd = 0
                while numd < depth-1:
                    kwd = kwd + f'Category_{numd:03d}_{numc:03d}\\'
                    numd += 1
                kwd = kwd + f'Category_{numd:03d}_{numc:03d}'
                numc += 1
                kwd = kwd + f'</AssetCategory>\n'
                outfile.write(kwd)
            outfile.write(f'</AssetCategoryList>\n')

    def colist(cfg):
        cols = int(cfg['assignedcollections'])
        depth = int(cfg['collectiondepth'])
        if cols > 0:
            outfile.write(f'<AssetCollectionList>\n')
            numc = 0
            while numc < cols:
                kwd = f'<AssetCollection>'
                numd = 0
                while numd < depth-1:
                    kwd = kwd + f'Collection_{numd:03d}_{numc:03d}\\'
                    numd += 1
                kwd = kwd + f'Collection_{numd:03d}_{numc:03d}'
                numc += 1
                kwd = kwd + f'</AssetCollection>\n'
                outfile.write(kwd)
            outfile.write(f'</AssetCollectionList>\n')

    def asset(c, cfg):
        # outfile.write(f'{d} - {c}')
        outfile.write(f'<Asset>\n')
        outfile.write(f'<Name>item_{c:06d}</Name>\n')
        outfile.write(f'<Folder>&lt;Local\\12345678&gt;\\</Folder>\n')
        outfile.write(f'<FileType>Nikon RAW</FileType>\n')
        outfile.write(f'<ImageType>4605262</ImageType>\n')
        outfile.write(f'<DBDate>20190101 00:00:00.000</DBDate>\n')
        outfile.write(f'<Caption>Orphan_{c:06d}</Caption>\n')
        outfile.write(f'<Label>red</Label>\n')
        outfile.write(f'<Author>Orphanage</Author>\n')
        outfile.write(f'<Notes>Note_{c:06d}</Notes>\n')
        outfile.write(f'<Rating>1</Rating>\n')
        kslist(cfg)
        cylist(cfg)
        colist(cfg)
        outfile.write(f'</Asset>\n')

    def aslist(cfg):
        outfile.write(f'<AssetList>\n')
        print()
        numc = 0
        while numc < count:
            print(f'\rwriting assets: {numc+1:06d}', end='')
            sys.stdout.flush()
            asset(numc, cfg)
            numc += 1
        outfile.write(f'</AssetList>\n')

    def frlist():
        outfile.write(f'<FolderRootList>\n')
        outfile.write(f'<FolderRoot>\n')
        outfile.write(f'<Name>O:</Name>\n')
        outfile.write(f'<DiscID>12345678</DiscID>\n')
        outfile.write(f'<RootType>Local</RootType>\n')
        outfile.write(f'<SysPath>O:</SysPath>\n')
        outfile.write(f'<DBRootPath>Local\\12345678</DBRootPath>\n')
        outfile.write(f'<VolumeLabel>Volumelabel</VolumeLabel>\n')
        outfile.write(f'<FileSystemType>NTFS</FileSystemType>\n')
        outfile.write(f'</FolderRoot>\n')
        outfile.write(f'</FolderRootList>\n')

    count = int(cfg['count'])
    if count > 0:
        aslist(cfg)
        frlist()


def doit():
    config = configparser.ConfigParser()
    config.read(os.path.dirname(__file__) + os.sep + 'config.ini')
    outfilename = sys.argv[1]
    outfile = createfile(outfilename)
    header(outfile, config['main'])
    keywordlist(outfile, config['keywordlist'])
    categorylist(outfile, config['categorylist'])
    assetlist(outfile, config['assetlist'])
    footer(outfile)

    outfile.close()


if __name__ == "__main__":
    doit()




