\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{scorecard}[2019/09/15]

\DeclareOption{fast}{\def\@fast{}}
\DeclareOption*{%
	\PassOptionsToClass{\CurrentOption}{article}%
}
\ProcessOptions\relax
\LoadClass[12pt]{article}

% Load packages
\RequirePackage{geometry}
\RequirePackage{tikz}
\RequirePackage{array}

% Get info from main tex document
\newcommand{\tagwidth}[1]{\def\@tagwidth{#1}}
\newcommand{\tagheight}[1]{\def\@tagheight{#1}}
\newcommand*{\crosssize}[1]{\def\@crosssize{#1}}
\newcommand*{\comp}[1]{\def\@comp{#1}}
\newcommand*{\url}[1]{\def\@url{#1}}
\newcommand*{\events}[1]{\def\@events{#1}}

% Default parameters
\tagwidth{85.7mm}
\tagheight{60.3mm}
\crosssize{1.5mm}

% Internal properties
\newcounter{tagnum} % Counter for left/right position
\def\pagereset{\newpage\setcounter{tagnum}{0}}
\newgeometry{margin=0.5in}
\setlength\parindent{0pt}
\newcolumntype{P}[1]{>{\centering\arraybackslash}p{#1}} % Used for centring table
\pagenumbering{gobble} % Suppress page numbers
\gdef\cardheight{\paperheight/2-0.1mm} % Scorecard height
\gdef\cardwidth{\paperwidth/2} % Scorecard width
\def\top{\cardheight-52.5mm} % Placement of results table
\tikzstyle{centre}=[anchor=south west,minimum height=10mm,minimum width=10mm,yshift=-0.5ex]

%% PDF metadata
%\AtBeginDocument{
%	\hypersetup{
%		pdftitle=\@comp
%	}
%}

% Define functions

% Define command for event images
\newcommand*{\img}[1]{%
	\includegraphics[
	height=12mm,
	width=12mm,
	keepaspectratio,
	]{#1}%
}

% Draw boxes for results
\newcommand\resultsbox[1]{%
	\draw (17mm,#1) rectangle +(80mm,10mm); % Rectangle
	\draw (27mm,#1) -- +(0mm,10mm); % Left divider
	\draw (77mm,#1) -- +(0mm,10mm); % Mid divider
	\draw (87mm,#1) -- +(0mm,10mm); % Right divider
}

% Draw cross marks for cutting
\newcommand\crossmarks[1]{%
	\draw (#1,0) -- (0,0) -- (0,#1);
	\draw (\@tagwidth-#1,0) -- (\@tagwidth,0) -- (\@tagwidth,#1);
	\draw (0,\@tagheight-#1) -- (0,\@tagheight) -- (#1,\@tagheight);
	\draw (\@tagwidth-#1,\@tagheight) -- (\@tagwidth,\@tagheight) -- (\@tagwidth,\@tagheight-#1);
}

% Draw name tags
\newcommand\nametag[3]{%
	% Arguments: Name, Role, WCAID
	\begin{tikzpicture}
		\draw [white] (0,0) rectangle (\@tagwidth,\@tagheight); % Define size
		\crossmarks{\@crosssize} % Draw cross marks

		% Place details
		\node at (\@tagwidth/2,50mm) {\bfseries \Large \@comp}; % Competition name
		\node at (\@tagwidth/2,36mm) {\@events}; % Event images
		\node at (\@tagwidth/2,22mm) {\bfseries \Large #1}; % Competitor's name
		\node at (\@tagwidth/2,14mm) {\large #2}; % Role
		\node at (\@tagwidth/2,6mm) {\small #3}; % WCAID
	\end{tikzpicture}%
	\stepcounter{tagnum}%
	\ifodd\value{tagnum} {\hspace{-2.9mm}} \else {\\ \vspace{-0.5mm}} \fi
}

% Draw groups
\newcommand\groups[2]{%
	%Arguments: Name, Groups (formatted to populate the table)
	\begin{tikzpicture}
		\draw [white] (0,0) rectangle (\@tagwidth,\@tagheight); % Define size
		\crossmarks{\@crosssize} % Draw cross marks

		% Place details
		\node[anchor=east] at (\@tagwidth-5mm,\@tagheight-5mm) {\footnotesize \@comp}; % Competition name
		\node at (\@tagwidth/2,5mm) {\footnotesize \@url}; % Live results
		\node[anchor=west] at (5mm,\@tagheight-5mm) {\footnotesize #1}; % Competitor's name
		% Table of groups
		\node at (\@tagwidth/2,\@tagheight/2) {\makebox[0mm]{
			\begin{tabular}{P{4cm}P{2cm}}
			\bfseries \large Event & \bfseries \large Group \\ \hline
			#2
			\hline
			\end{tabular}
		}};
	\end{tikzpicture}%
	\stepcounter{tagnum}%
	\ifodd\value{tagnum} {\hspace{-2.9mm}} \else {\\ \vspace{-0.5mm}} \fi
}

% Draw scorecards
\newcommand\scorecard[7][]{%
	% Optional Argument: Defines type of scorecard (empty: 5 attempts. not empty: 3 attempts)
	% Arguments: Name, Cubecomps ID, Event, Cutoff, Round, Group
	\begin{tikzpicture}

		\ifdefined\@fast
			\ifx&#1& % If normal event
				\ifx&#5& % If no cutoff
					\node[anchor=south west,inner sep=0] at (0,0) {\includegraphics[width=4.25in, height=5.48in]{./Backgrounds/Default}};
				\else % If cutoff
					\node[anchor=south west,inner sep=0] at (0,0) {\includegraphics[width=4.25in, height=5.48in]{./Backgrounds/Default_Cutoff}};
				\fi
			\else % If three attempt event
				\ifx&#5& % If no cutoff
					\node[anchor=south west,inner sep=0] at (0,0) {\includegraphics[width=4.25in, height=5.48in]{./Backgrounds/Short}};
				\else % If cutoff
					\node[anchor=south west,inner sep=0] at (0,0) {\includegraphics[width=4.25in, height=5.48in]{./Backgrounds/Short_Cutoff}};
				\fi
			\fi
		\else {
			\draw [white] (0,0) rectangle (\cardwidth,\cardheight); % Define size
			\draw [rounded corners=7.5mm,thick] (3mm,3mm) rectangle (\cardwidth-3mm,\cardheight-3mm); % Draw outline
		} \fi

		\crossmarks{\@crosssize} % Draw cross marks

		% Define variables based on type of scorecard
		\ifx&#1& \gdef\maxnum{5} \gdef\cutoffnum{2} \gdef\cutoffshift{12.5mm} \else \gdef\maxnum{3} \gdef\cutoffnum{1} \gdef\cutoffshift{0mm} \fi

		\ifdefined\@fast
			\def\word
		\else {
			% Results table
			\foreach \i in {1,...,\maxnum}{
				\ifx&#5& \gdef\shift{0mm} \else \ifnum\i>\cutoffnum \gdef\shift{3mm} \else\gdef\shift{0mm} \fi \fi
				\resultsbox{\top-\i*12.5mm-\shift} % Boxes
				\node at (12mm,\top-\i*12.5mm+5mm-\shift) {\bfseries \Large \i}; % Solve num
			}
			% Extra result
			\resultsbox{\top-\maxnum*12.5mm-16.5mm-\shift} % Box
			\node[anchor=north] at (12mm,\top-\maxnum*12.5mm-12.5mm-\shift) {\bfseries \Large \underline{\hspace{6mm}}}; % Attempt num
			\draw[dashed] (7mm,\top-\maxnum*12.5mm-3.25mm-\shift) -- +(94mm,0mm) node[pos=0.5,fill=white] {\footnotesize Extra Attempt---Delegate: \underline{\hspace{6mm}}}; % Label
		}
		\fi

		%Cutoff label
		\ifx&#5& \else%
			\draw[dashed] (7mm,\top-14mm-1.25mm-\cutoffshift) -- +(94mm,0mm) node[pos=0.5,fill=white] {\footnotesize Cutoff: #5};
		\fi

		\ifdefined\@fast
			\def\word
		\else {
			% Header
			\draw (17mm,\top+5mm) rectangle +(80mm,10mm); % Top box
			\draw (17mm,\top+22.5mm) rectangle +(80mm,10mm); % Lower box
			\draw (27mm,\top+22.5mm) -- +(0mm,10mm); % Left divider
			\draw (77mm,\top+5mm) -- +(0mm,10mm); % Mid divider
			\draw (87mm,\top+5mm) -- +(0mm,10mm); % Right divider
			% Labels
			\node at (22mm,\top) {\strut\footnotesize Scr.}; % Scrambler signature
			\node at (52mm,\top) {\strut\footnotesize Result}; % Result
			\node at (82mm,\top) {\strut\footnotesize Judge}; % Judge signature
			\node at (92mm,\top) {\strut\footnotesize Comp.}; % Competitor signature
			\node at (22mm,\top+17.5mm) {\strut\footnotesize Event}; % Event name
			\node at (92mm,\top+17.5mm) {\strut\footnotesize Group}; % Group number
			\node at (82mm,\top+17.5mm) {\strut\footnotesize Round}; % Round number
			\node at (22mm,\top+35mm) {\strut\footnotesize ID}; % Cubecomps ID
			\node at (34.5mm,\top+35mm) {\strut\footnotesize Name}; % Competitor name
		}
		\fi

		% Populate data
		\node[centre] at (27mm,\top+22.5mm) {\strut\Large #2}; % Competitor name
		\node[centre, anchor=south] at (22mm,\top+22.5mm) {\strut\Large #3}; % Cubecomps ID
		\node[centre] at (17mm,\top+5mm) {\strut\Large #4}; % Event name
		\node[centre] at (77mm,\top+5mm) {\strut\Large #6}; % Round number
		\node[centre] at (87mm,\top+5mm) {\strut\Large #7}; % Group number
		\node at (\cardwidth/2,\cardheight-10mm) {\bfseries \Large \@comp}; % Competition name

	\end{tikzpicture}%
	\stepcounter{tagnum}%
	\ifodd\value{tagnum} {\hspace{-2.9mm}} \else {\\ \vspace{-0.5mm}} \fi
}
