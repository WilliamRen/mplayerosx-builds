## outdated: please use the instructions at https://github.com/pigoz/mplayerosx-builds ##

This document is still work in progress.

**Note** when building I work into a directory into my home called dev, my tree looks like this:
```
~
|- dev
    |- libbs2b-3.1.0
    |- mplayer-build
    |- mplayerosx-builds
```

To make this document more readable I'll assume that you are using the same directory structure.

# Install GNU's autotools #

The autotools coming with Mac OSX gave me problems so I recompiled them using [MacPorts](http://www.macports.org/).

```
sudo port install autoconf automake libtool pkgconfig
```

# Compile the dependencies #

mplayerosx-builds uses [MacPorts](http://www.macports.org/) to build most of the dependencies. This is a list of the dependencies you need to install with [MacPorts](http://www.macports.org/) to have similar functionalities:

```
sudo port install bzip2 expat freetype fontconfig libdvdnav libdvdread libdvdcss libiconv libpng libtheora ncurses zlib lzo2
```

## Compile BS2B ##
BS2B is not available as a [MacPorts](http://www.macports.org/) package so you need to build manually. First you need to build libsndfile because BS2B depends on it, luckyly this is available on [MacPorts](http://www.macports.org/):

```
sudo port install libsndfile
```

Then you can get the BS2B source tarball and compile.

```
cd ~/dev
wget http://downloads.sourceforge.net/project/bs2b/bs2b/3.1.0/libbs2b-3.1.0.tar.gz?use_mirror=dfn
tar xvfz libbs2b-3.1.0.tar.gz
cd libbs2b-3.1.0/
mkdir build && cd build
export CFLAGS=-I/opt/local/include
export LDFLAGS=-L/opt/local/lib
export LIBTOOL=/opt/local/bin/glibtool
export LIBTOOLIZE=/opt/local/bin/glibtoolize
../configure
make
sudo make install
```

# Get the build scripts #

The compilation process uses the scripts provided by Uoti here: http://repo.or.cz/w/mplayer-build.git


# Edit the configuration files #

After cloning the mplayer-build repository you need to:

```
./init
./enable-mt
```

You can now proceed to edit the configuration files to add some options to the configures.

**common\_options**:
```
--cc=gcc-4.2
```

**ffmpeg\_options**:
```
--cpu=core2
--arch=x86_64
```

**mplayer\_options**:
```
--disable-x11
--disable-gl
--disable-mencoder
--enable-macosx-bundle
--enable-macosx-finder
--target=x86_64-Darwin
```


# Apply the patches #
I have developed some custom patches to improve the behavior of mplayer with MPlayer OSX Extended. To apply the patches use git apply into mplayer's source tree root (~/dev/mplayer-build/mplayer):

```
git apply ~/dev/mplayerosx-builds/mplayer-patches/${PATCHNAME}.diff
```


# Compile ffmpeg+libass+mplayer #
Run make in the mplayer-build directory. The build scripts will take care of everything from running configure to the actual building.