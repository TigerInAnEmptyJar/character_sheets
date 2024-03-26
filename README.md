Character sheet generation
============================

Hi folks!

The scripts contained in this repository found their way into our world, because I was 
pretty annoyed by some of the fillable PDFs out there for both Dungeons&Dragons as well
as GURPS Dungeon Fantasy.

And, sure it is possible, but it is not that much fun to version-control a PDF. That's 
much easier with a text file.

However smart these scripts may be, they are not meant to be a fully fledged character
generation tool. They take whatever you have defined as character and put that into a
nicely formatted PDF.

## Prerequisites

For the scripts to work, you'll need:
* Python version 3.10 or later
* pdflatex

I tested the scripts on (Manjaro) Linux, but they are untested for other systems.

## Setting up a character sheet

Both script directories contain a template for a character `json` file, which you can use
to define your own character. They contain all tags required by the scripts and some 
example entries. 

Note: Races add boni to ability scores, like strength. These will be added automatically
by the script. The adjusted values are visible then in the PDF.

## Running the script

Both scripts work rather similarly. They take a character definition sheet in `json` format
and an output pattern as input (pattern can be a filename stem, then it will be expanded 
to `$(pwd)/outfile.pdf` or an absolute path like `/path/to/folder/base`, which will create
this file `/path/to/folder/base.pdf`). 

Since the scripts are using pdflatex to generate the PDF, intermediate files, like the `tex`
file will be created in a folder `build` in the output folder. They are not cleaned 
automatically, so feel free to inspect them.

### Dungeons and Dragons

```
python /path/to/repo/DnD/dnd2tex.py myCharacter.json --outfile myCharacter 
```

### GURPS

```
python /path/to/repo/GURPS/gurps2tex.py myCharacter.json --outfile myCharacter 
```

## Internals

### Dungeons & Dragons

Properties of professions and races are defined in `json` files in the sub-folder `tables`.
The respective classes in `professions.py` and `races.py`, instantiated via the main 
script, read these table files and adjust values accordingly.  

All calculated values are added to the respective latex template (in folder `templates`) and
written to file, before pdflatex is invoked.

### GURPS

Admittedly, this system has a lot more to calculate, than D&D, having more secondary and
dependent properties. We do calculations for `advantages`, `attributes`, `skills`, `spells` 
and `equipment` in the respective python files. Each of them have a `json` table with the
needed data in the `tables` folder.

Skill levels are calculated and - where applicable and, most important, implemented - 
adjusted for dis/-advantages the character took.

All calculated values are added to the latex template and written to file, before pdflatex 
is invoked.
