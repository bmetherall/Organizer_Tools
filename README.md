# Overview
1. `Grouper.py`: Pulls competition info from the WCA, then creates groups and writes LaTeX code for the `scorecard` class.
2. `scorecard.cls`: The scorecard class contains the LaTeX code for drawing (with TikZ) name tags, groups for the back of name tags, and scorecards for WCA competitions.

## Usage
The code can be run with `python3 Grouper.py` from a terminal. This will create (some of) the following files:

1. `compId.tex`: Main TeX file for compiling name tags, group tables, and scorecards.
2. `compId-Cards.tex`: Contains LaTeX code for generating scorecards.
3. `compId-Groups.csv`: Contains competitors and their groups.
4. `compId-Groups.tex`: Contains LaTeX code for generating individual group tables for name tags.
5. `compId-Tags.tex`: Contains LaTeX code for generating name tags.
6. `compId-WCA.md`: Contains competitors and their groups for uploading to the WCA competition page.

The name tags and scorecards can then be generated with `pdflatex compId.tex` from the terminal.

### Scorecard Class
The scorecard class is loaded with `\documentclass{scorecard}`, and provides the commands `\nametag`, `\groups`, and `\scorecard`.

Additonally, the `scorecard` class provides some optional arguments:

* `fast` Uses predrawn scorecards saved in `./Backgrounds` to greatly speed up compilation time.

* `a4paper` Uses A4 paper instead of US letter paper. The alignment will be slightly off, and will not work well with the argument `fast`.

* Any other argument that the `article` class accepts will be passed through.
