---
layout: page
title: Learn \LaTeX
permalink: /latex/
---

---
## Table of Content
1. ["Who Is LaTeX" Stage](#who-is-latex-stage)
    - [Typing](#typing)
    - [How To Learn](#how-to-learn)
    - [Where To Tex](#where-to-tex)
        - [GUI / Text Editor for LaTeX](#gui--text-editor-for-latex) 
1. [Life Hacks](#life-hacks)
1. [Typical Mistakes](#typical-mistakes)
1. [Useful Links](#useful-links)

---
<p>&nbsp;</p>

## "Who Is LaTeX" Stage
### Typing
It is a requirement for [any](https://www.ratatype.com) programming activity. Open any trainer for blind printing with ten fingers — and go ahead!

### How To Learn
For a quick start in LaTeX take [a free course from the HSE](https://www.coursera.org/learn/latex). The basics could be learned in 4-5 hours, and two days off are enough for the entire course. Video lessons are better than thick books in the beginning.

### Where To TeX
There are two ways.
1. Online compiler like overleaf.
    - Very simple.
    - Real-time online teamwork.
2. Set up your environment.
    - ***So much faster compiling!*** 
    - Takes time.  
    - Easier to integrate Git.
    
#### GUI / Text Editor for LaTeX
**The best** option, in my opinion, is `LaTeX` in `Vim`. There are [**gold**](https://castel.dev) 
articles in which Gilles Castel shows his `Vim` + `LaTeX` setup and how it works.

Otherwise — you can try `TexStudio`, but it looks like an ancient artifact. 
Also, there is the `texpad` app for macOS, but I had some issues with buggy behavior (in 2020).

PS: The `Vim` + `LaTeX` setup can easily take 20+ hours to make it work if you are new.

<p>&nbsp;</p>
---
## Life Hacks
1. Use `\newcommand{command_name}{script_of_command}` for commands you use **very often**.
   Compare `f: \mathbb{R} \to \mathbb{R}` and `f: \R\to\R`.
   <img src="https://i.upmath.me/svg/f%3A%20%5Cmathbb%7BR%7D%20%5Cto%20%5Cmathbb%7BR%7D" alt="f: \mathbb{R} \to \mathbb{R}" />
1. Learn how to tex in `Vim` =)
   
## Typical Mistakes
1. Please, God, don't do 500+ lines main.tex ... 
    - It will be an unmaintainable mess.
    - You don’t have a universal preamble.

    Instead --- use `input{anotherFile.tex}` or `include{anotherFile.tex}` to structure code.

1. Not using or defining `LaTeX` environments. 
    For every theorem, proof, note, etc. you can set special environment (`\begin{theorem}`, `\begin{proof}`).
    - Now you can change the style of your theorems by changing one line.

1. Not using `multiline` or `align` environments for long formulas.
    <img src="https://i.upmath.me/svg/%5Cbegin%7Balign*%7D%0Aa%20%26%3D%20%20b%20%2B%20c%20%2B%20d%20-%20d%20%5C%5C%0A%26%3D%20b%20%2B%20c%0A%5Cend%7Balign*%7D" alt="\begin{align*}
    a &amp;=  b + c + d - d \\
    &amp;= b + c
    \end{align*}" />
```
\begin{align*}
    a &=  b + c + d - d \\
      &= b + c
\end{align*}
``` 
1. Not using `\cfrac` or `\displaystyle` when necessary.
    - Otherwise, the formula may get hard to read.  
    <img src="https://i.upmath.me/svg/%5Cfrac%7B2%20%2B%20%5Cfrac%7B8%7D%7B4%7D%7D%7B6%7D" alt="\frac{2 + \frac{8}{4}}{6}" /> (`\frac{2 + \frac{8}{4}}{6}`)  
    <img src="https://i.upmath.me/svg/%5Cfrac%7B%5Cdisplaystyle%202%20%2B%20%5Cfrac%7B8%7D%7B4%7D%7D%7B6%7D" alt="\frac{\displaystyle 2 + \frac{8}{4}}{6}" /> (`\cfrac{2 + \frac{8}{4}}{6}`)  


1. Not using `\text` inside formulas.  
    <img align="center" src="//i.upmath.me/svg/" alt="" />
<img align="center" src="//i.upmath.me/svg/%5Cbegin%7Balign*%7D%0Aa%20%26%3D%20a%20%2B%20b%20%2B%20c%20%2B%20d%20%2C%20when%5C%3B%20sun%5C%3B%20is%5C%3B%20red%20%20%5C%5C%0Aa%20%26%3D%20b%20%2B%20c%2C%20%5Ctext%7Bwhen%20sun%20is%20white%7D%0A%5Cend%7Balign*%7D" alt="\begin{align*}
a &amp;= a + b + c + d , when\; sun\; is\; red  \\
a &amp;= b + c, \text{when sun is white}
\end{align*}" />
    ```
$$\begin{align*}
a &= a + b + c + d , when\; sun\; is\; red  \\
a &= b + c, \text{when sun is white}
\end{align*}$$
    ```
1. All variables inside text should be math mode.  
    -a or <img src="https://i.upmath.me/svg/-a" alt="-a" />
1. Avoid making new lines in text with `\\`.
    - Using empty lines instead makes code much more readable.
1. Not using `\ldots` for ...
  
1. Ignoring warnings and errors.
    - You **must not**  ignore errrs.
    - Warnings help you deepen your knowledge and improve code.
1. Not using `Git` for big projects.
    - Best of luck...
1. Using tutorials from ancient times.
    - You can meet outdated and deprecated practices.

    
## Useful Links

- [Get LaTeX code from formula screenshot](https://mathpix.com) --- super ultra-useful
- [Draw symbol and get latex command](http://detexify.kirelabs.org/classify.html) --- ultra-useful
- [Latex table constructor](https://www.tablesgenerator.com)
- [LaTeX Cheatsheet](http://wch.github.io/latexsheet/latexsheet.pdf)
