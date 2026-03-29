# LaTeX Kurzueberblick fuer die Presentation

Diese Datei erklaert ein paar haeufige LaTeX-Bausteine, die du in `Presentation.tex` nutzen kannst.

## 1) Listen mit `itemize`

Fuer Aufzaehlungen ohne Nummern:

```latex
\begin{itemize}
  \item Erster Punkt
  \item Zweiter Punkt
  \item Dritter Punkt
\end{itemize}
```

Wenn du Nummern willst, nutze stattdessen `enumerate`.

## 2) Tabellen mit `tabular`

Ein einfaches Beispiel mit 3 Spalten:

```latex
\begin{tabular}{|l|c|r|}
  \hline
  Name & Jahr & Ort \\
  \hline
  Daguerre & 1839 & Paris \\
  Talbot & 1841 & London \\
  \hline
\end{tabular}
```

Erklaerung der Spaltenangabe `{|l|c|r|}`:

- `l` = linksbuendig
- `c` = zentriert
- `r` = rechtsbuendig
- `|` = vertikale Linie

## 3) Bilder mit `includegraphics`

Dafuer brauchst du das Paket `graphicx` (bei Beamer oft schon aktiv, sonst manuell laden):

```latex
\usepackage{graphicx}
```

Bild in einer Folie:

```latex
\begin{frame}{Beispielbild}
  \centering
  \includegraphics[width=0.7\textwidth]{bilder/foto.jpg}
\end{frame}
```

Nutzliche Optionen:

- `width=...` Breite setzen
- `height=...` Hoehe setzen
- `scale=...` Skalierung
- `keepaspectratio` Seitenverhaeltnis beibehalten

## 4) Mini-Beispiel: Alles zusammen

```latex
\begin{frame}{Ueberblick}
  \begin{itemize}
    \item Fotografie ab 1839
    \item Wichtige Pioniere
  \end{itemize}

  \vspace{0.5cm}

  \begin{tabular}{lc}
    Person & Jahr \\
    Daguerre & 1839 \\
    Talbot & 1841
  \end{tabular}
\end{frame}
```

## 5) Typische Fehler

- Bildpfad falsch geschrieben (`includegraphics` findet Datei nicht).
- Paket vergessen (`graphicx` fehlt).
- Bei Tabellen ein `\\` oder `&` vergessen.
- Zu breite Inhalte auf einer Folie (lieber kuerzen oder auf mehrere Folien aufteilen).

## 6) Basics von LaTeX Beamer

### Minimaler Start

```latex
\documentclass{beamer}

	itle{Geschichte der Fotografie}
\author{Dein Name}
\date{\today}

\begin{document}

\frame{\titlepage}

\begin{frame}{Agenda}
  	ableofcontents
\end{frame}

\section{Anfaenge}
\begin{frame}{Erste Schritte}
  Inhalt der Folie
\end{frame}

\end{document}
```

### Wichtige Beamer-Bausteine

- Jede Folie ist ein `frame`.
- Mit `\section{...}` strukturierst du die Praesentation.
- `\frame{\titlepage}` erzeugt das Titelblatt.
- `\tableofcontents` erstellt eine Inhaltsuebersicht.

### Overlays (schrittweiser Inhalt)

```latex
\begin{frame}{Punkte nacheinander}
  \begin{itemize}
    \item<1-> Erster Punkt
    \item<2-> Zweiter Punkt
    \item<3-> Dritter Punkt
  \end{itemize}
\end{frame}
```

Alternative:

```latex
\begin{frame}{Schrittweise mit Pause}
  Erster Satz.\pause
  Zweiter Satz.\pause
  Dritter Satz.
\end{frame}
```

### Bloecke fuer Hervorhebungen

```latex
\begin{frame}{Block-Beispiele}
  \begin{block}{Info}
    Neutraler Hinweis.
  \end{block}

  \begin{alertblock}{Wichtig}
    Dieser Punkt ist besonders wichtig.
  \end{alertblock}

  \begin{exampleblock}{Beispiel}
    Konkretes Beispiel.
  \end{exampleblock}
\end{frame}
```

### Zwei Spalten auf einer Folie

```latex
\begin{frame}{Bild und Text}
  \begin{columns}
    \begin{column}{0.55\textwidth}
      \begin{itemize}
        \item Kurzer Punkt
        \item Noch ein Punkt
      \end{itemize}
    \end{column}
    \begin{column}{0.45\textwidth}
      \includegraphics[width=\textwidth]{bilder/foto.jpg}
    \end{column}
  \end{columns}
\end{frame}
```

### Theme und Aussehen

Ein Theme kannst du im Vorspann setzen:

```latex
\usetheme{Madrid}
```

Oft genutzte Themes: `Madrid`, `Berlin`, `CambridgeUS`, `Boadilla`.

### Typische Beamer-Fehler

- Zu viel Text pro Folie (besser Stichpunkte).
- Overlays (`<1->`) falsch nummeriert.
- Bilder ohne `\centering` oder mit zu grosser Breite.
- Fehlende `\end{frame}` oder nicht geschlossene Umgebungen.
