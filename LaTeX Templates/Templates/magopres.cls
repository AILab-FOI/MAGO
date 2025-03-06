\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{magopres}[2025/03/06 Custom Presentation Class]

\LoadClass[11pt, aspectratio=169]{beamer}

\RequirePackage{fontspec}
\RequirePackage{fontawesome}
\RequirePackage{FiraSans}
\RequirePackage{booktabs}
\RequirePackage[scale=1]{ccicons}
\RequirePackage{pgfplots}
\pgfplotsset{compat=1.18}
\RequirePackage{appendixnumberbeamer}
\RequirePackage{subcaption}
\RequirePackage{graphicx}
\RequirePackage{qrcode}
\RequirePackage{tabularx}
\RequirePackage{hyperref}
\RequirePackage{multicol}
\RequirePackage{pifont}
\RequirePackage{setspace}


\input{LaTeX Templates/Preambles/Tikz}
\input{LaTeX Templates/Preambles/Custom Commands}
\input{LaTeX Templates/Preambles/Acronyms}
\input{LaTeX Templates/Preambles/Itemize}
\input{LaTeX Templates/Preambles/Listings}
\input{LaTeX Templates/Preambles/Cleveref}
\input{LaTeX Templates/Preambles/BibLaTeX}
\renewcommand*{\bibfont}{\tiny}
\input{LaTeX Templates/Preambles/Custom Sequence Items}
\input{LaTeX Templates/Preambles/Chart Donut}
\input{LaTeX Templates/Preambles/Colours}

\setmainfont{Fira Sans Light}
\setsansfont[
  ItalicFont={Fira Sans Light Italic},
  BoldFont={Fira Sans},
  BoldItalicFont={Fira Sans Italic}
]{Fira Sans Light}
\setmonofont[BoldFont={Fira Mono Medium}]{Fira Mono}

\AtBeginEnvironment{tabular}{%
  \addfontfeature{Numbers={Monospaced}}
}


\mode<presentation>
{
    \usetheme[
        progressbar=frametitle,
        numbering=fraction,
        subsectionpage=simple,
        sectionpage=progressbar,
        block=fill
    ]{moloch}
}

\setbeamercolor{block title}{bg=blockcolour, fg=maincolour}
\setbeamercolor{block body}{bg=blockcolour!10!maincolour, fg=frontcolour}

\setbeamercolor{block title example}{bg=examplecolour, fg=maincolour}
\setbeamercolor{block body example}{bg=examplecolour!10!maincolour, fg=frontcolour}

\input{LaTeX Templates/Preambles/Beamer Settings}

\newcommand{\makePreface}[1]{%
    #1
    \begin{document}
}

\newcommand{\makeTableOfContents}{
    \setbeamertemplate{footline}{%
        \leavevmode%
        \vspace{2pt}
        \hbox{%
            \begin{beamercolorbox}[wd=\paperwidth,ht=3ex,dp=1.125ex]{palette quaternary}%
                \begin{columns}[T,onlytextwidth]
                    \column{0.33\paperwidth}
                    
                    \column{0.33\paperwidth}
                    \centering
                    \textcolor{footertext}{\insertshortauthor~@~\insertshortsubtitle}
                    
                    \column{0.33\paperwidth}
                \end{columns}
            \end{beamercolorbox}%
        }
    }
    
    \begin{frame}{\prijevod{Sadržaj}{Contents}}
        \setbeamertemplate{section in toc}[sections numbered]
        \tableofcontents[hideallsubsections]
    \end{frame}
    
    \setbeamertemplate{footline}{%
        \leavevmode%
        \vspace{2pt}
        \hbox{%
            \begin{beamercolorbox}[wd=\paperwidth,ht=3ex,dp=1.125ex]{palette quaternary}%
                \begin{columns}[T,onlytextwidth]
                    \column{0.33\paperwidth}
                    \hspace{1pt}
                    \textcolor{footertext}{\insertshorttitle~>~\insertsectionhead}
                    
                    \column{0.33\paperwidth}
                    \centering
                    \textcolor{footertext}{\insertshortauthor~@~\insertshortsubtitle}
                    
                    \column{0.33\paperwidth}
                    \textcolor{footertext}{\hfill\insertframenumber{}~/~\inserttotalframenumber\hspace{0.2cm}}
                \end{columns}
            \end{beamercolorbox}%
        }
    }
    \setcounter{framenumber}{0}
}

\newcommand{\makeBibliography}{
    \section*{\prijevod{Popis literature}{Bibliography}}
    
    \begin{frame}[allowframebreaks]{\insertsection}
        \printbibliography[heading=none]
    \end{frame}
}

\newcommand{\makeBack}{
    \section*{Acknowledgement}

    \begin{frame}{\insertsection}
        \begin{multicols}{2}
            \null\vfill
            \prijevod{
                \textbf{MOBODL-2023-08-5618}
                Ovaj projekt financirale su Europska unija i Hrvatska zaklada za znanost.
            }{
                \textbf{MOBODL-2023-08-5618}
                This project was funded by the European Union and the Croatian Science Foundation.
            }
            \columnbreak
            \centering
            \prijevod{
                \includegraphics[width=4cm]{LaTeX Templates/Common Figures/EU logo HR.pdf}
                \includegraphics[width=4cm]{LaTeX Templates/Common Figures/HRZZ logo HR.pdf}
            }{
                \includegraphics[width=4cm]{LaTeX Templates/Common Figures/EU logo EN.pdf}
                \includegraphics[width=4cm]{LaTeX Templates/Common Figures/HRZZ logo EN.pdf}
            }
        \end{multicols}
    \end{frame}

    \begin{frame}[standout]    
        \centering
        \large{\insertauthor}
        dokresa@foi.unizg.hr
        \begin{multicols}{3}
            \includegraphics[width=4cm]{LaTeX Templates/Common Figures/QR Contact Signal.pdf}
            \includegraphics[width=4cm]{LaTeX Templates/Common Figures/QR Contact All.pdf}
            \includegraphics[width=4cm]{LaTeX Templates/Common Figures/QR Contact Telegram.pdf}
        \end{multicols}
        \scriptsize \insertinstitute
        \large \url{ai.foi.hr}
    \end{frame}
    \end{document}
}