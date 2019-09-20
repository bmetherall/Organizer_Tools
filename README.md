# Overview
Currently this repository has two programs for two purposes.

1. `Convert.py`: Reads the registration file, then create groups and write LaTeX code for the `scorecard` class.
2. `scorecard.cls`: The scorecard class contains the LaTeX code for drawing (with TikZ) name tags, groups for the back of name tags, and scorecards for WCA competitions.

## Usage

Download the registration file from the WCA website and move it to this directory. Running `python Convert.py CompetitionNameYear` will create the following files:

1. `NameTags.tex`: Contains LaTeX code for generating name tags with the `scorecard` class.
2. `Groups.tex`: Contains LaTeX code for generating a table of groups for the back of name tags with the `scorecard` class.
3. `Cards.tex`: Contains LaTeX code for generating scorecards for the competition with the `scorecard` class.
4. `Groups.md`: Contains a table of groups for all competitors in markdown for posting online.
5. `Groups.csv`: Contains a table of groups for all competitors in csv format for the organizers.

### Scorecard Class

Once the three `.tex` files have been generated, compiling `Main.tex` will produce all the name tags, group tables, and scorecards in `Main.pdf`.

The scorecard class is loaded with `\documentclass{scorecard}`, and provides the commands `\nametag`, `\groups`, and `\scorecard`.

Additonally, the `scorecard` class provides some optional arguments:

* `fast` Uses predrawn scorecards saved in `.\Backgrounds` to greatly speed up compilation time.

* `a4paper` Uses A4 paper instead of US letter paper. The alignment will be slightly off, and will not work with the argument `fast`.

* Any other argument that the `article` class accepts will be passed through.


