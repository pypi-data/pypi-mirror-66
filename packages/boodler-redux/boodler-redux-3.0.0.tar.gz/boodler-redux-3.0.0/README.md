Boodler Redux: A programmable soundscape tool

Designed by Andrew Plotkin <erkyrath@eblong.com>
   <http://boodler.org/>

Recent work (3.0.0 and above) by Beau Gunderson <beau@beaugunderson.com>
   <https://beaugunderson.com/>

Copyright 2001-2011 by Andrew Plotkin
   This program is distributed under the LGPL.
   See the LGPL document, or the above URL, for details.

## WHAT IT IS

Boodler is a tool for creating soundscapes -- continuous, infinitely
varying streams of sound. Boodler is designed to run in the background
on a computer, maintaining whatever sound environment you desire.

Boodler is extensible, customizable, and modular. Each soundscape is a
small piece of Python code -- typically less than a page. A soundscape
can incorporate other soundscapes; it can combine other soundscapes,
switch between them, fade them in and out. This package comes with
many example soundscapes. You can use these, modify them, combine them
to arbitrary levels of complexity, or write your own.

Boodler is written in Python, with the driver module (cboodle_stdout)
written in C. It was developed under Python 3.

Boodler can generate audio output to one destination:

- stdout: write raw sample output to stdout

Boodler does not come with any warranty of any sort whatsoever.

## GETTING STARTED

Boodler is now distributed as a standard Python setuptools package.
If you have downloaded the source code, you need only type:

```python
python setup.py build
python setup.py install
```

For more information, point your web browser at the contents of the
documentation folder (doc/index.html in this package) and follow the
"Installation" link.

Note that the Boodler is not distributed with any soundscapes. You
must download those separately. See the "Running Boodler" link in the
documentation folder.

## LICENSING FOR USERS

(Running Boodler)

Boodler is free software, and you may run it freely. (Portions of the
Boodler source code are copyrighted and licensed under the LGPL or the
GPL, and other portions are public domain. Neither of these restrict
you in any way from running the program.)

However, there is another legal issue. Boodler operates by executing
soundscape code, which combines sound-sample files into a ongoing
stream of sound. Legally speaking, when you run Boodler, you are
creating a derivative work based on those code fragments and sound
files.

The soundscapes and sound files in the Boodler package library are
*not* all in the public domain. Many are licensed "for non-commercial
use only". Some of the sound files were found by random searching
around the web, and appear without any copyright statement at all.

It is my opinion (*not* backed by any legal advice) that if you run
Boodler for your own private use, using packages downloaded from the
Boodler library, then you are within the scope of fair use and the
"non-commercial use" licenses of those sounds.

However, if you play the sound output of Boodler (based on the Boodler
package library) as a commercial performance, or include it in a
recording sold for profit, you may not be complying with the copyright
restrictions on those sounds. You will have to look at the license
terms of the packages you use, and decide whether your performance is
legal.

Note that this legal issue is a problem of playing sounds and
soundscapes from the Boodler package library. It is not a restriction
of the Boodler software itself. If you create your own Boodler
soundscape, based solely on *your own* sound-sample files and code,
then that stream of sound is entirely your own work; you may do with
it as you wish.

## LICENSING FOR SOUNDSCAPE DESIGNERS

(Creating new soundscapes)

The sound and soundscape packages in the org.boodler section of the
package library (excluding org.boodler.old) are in the public domain.
They are intended to be used as code samples as well as soundscapes.
You may modify, extend, combine, and pervert them as you wish.

The sound packages in the org.boodler.old section of the package
library are copyrighted, but free for non-commercial use. They are not
free for commercial use.

Sound packages elsewhere in the library (not under org.boodler) are
free for non-commercial use. They may or may not be free for
commercial use, modification, and other forms of derivative work. See
the terms of each package for details.

If you create sound files or soundscape code for use with Boodler, you
may license them as you wish -- GPL, LGPL, Creative Commons, some
other license. Or you might choose to not release them at all; you are
not obligated to do so.

## LICENSING FOR SOUNDSCAPE CONTRIBUTORS

(Putting your work in the Boodler library)

You are welcome to contribute your sounds and soundscapes to the
Boodler project. Any properly-formatted package file will be accepted
into the Boodler package library, as long as it is free for users to
enjoy.

You are also welcome to repackage and contribute other people's
sounds, as long as their licenses permit you to do so.

To be accepted, a package must be, at minimum, free for non-commercial
use. The Boodler project strongly encourages contributions to be either
placed in the public domain, or licensed under an open-source or
Creative Commons license.

## LICENSING FOR PROGRAMMERS

(Modifying Boodler and incorporating it into other software)

I consider Boodler to be more like a software component than a
stand-alone program. Accordingly, I have released it under the GNU
Library General Public License (the LGPL). To be precise, the
workhorse parts of Boodler -- the boodle and boopak Python packages --
form a library, which is licensed under the LGPL.

The Python program boodler is simply a shell that starts up the
Boodler library. I have released this program into the public domain.
You may do with it as you like. However, understand that if you write
a program that is intended to link in the Boodler library (regardless
of whether you use the boodler script), then your program is a work that
uses the library, and must behave appropriately. See the LGPL document
for details.

One detail: the C source code of the cboodle extensions is
dual-licensed. You may use it under the terms of the LGPL or the GPL,
whichever you like.
