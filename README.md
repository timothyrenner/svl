# SVL: Declarative Data Visualizations

[![Build Status](https://travis-ci.org/timothyrenner/svl.svg?branch=master)](https://travis-ci.org/timothyrenner/svl)

[![Coverage Status](https://coveralls.io/repos/github/timothyrenner/svl/badge.svg?branch=master)](https://coveralls.io/github/timothyrenner/svl?branch=master)

SVL is a declarative, SQL-like language for simple data visualizations.

Initially I made this project to learn and experiment with [EBNF](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form) context-free grammars, but pretty quickly realized this was something I could actually use for my job.
Maybe you will find it useful too.

## Quickstart

Installation is done with pip:

**TODO - figure out install**


Then, create a file called "plots.svl" and paste this into it:

```
DATASETS 
    bigfoot "sample_data/bigfoot_sightings.csv"
LINE bigfoot 
    X date BY YEAR 
    Y report_number COUNT
```

That's an SVL program that creates a single line chart.
To compile it to a visualization, run

```
svl plots.svl
```

## Alpha Features

**Easy to learn**: The entire grammar is under 150 lines.

**Five chart types**: Line, bar, scatter, histogram and pie. I plan on adding more, so if I'm missing your favorite one let me know.

**Complex layouts**: SVL scripts can support any number of plots and makes it straightforward to arrange them so that the most important plots get the most real estate.
The screenshot below was built with just **XXX** lines of SVL.

**TODO screenshot of something cool**

**Interactive HTML output**: SVL uses Plotly (**TODO link**) to draw the visualizations, and produces an easily shareable but still interactive HTML file.

**CSV and Parquet files**: Currently the data is limited to files, and SVL has support for CSV and (if pyarrow (**TODO link**) is installed) parquet files.

## Not Alpha Features, but Possible

**Other plot backends** The compiler isn't married to Plotly.
SVL can have future support for other backends like Vega, Bokeh, or even Matplotlib (probably).

**Other data sources** For simplicity SVL operates on files, but like the plot renderer the compiler isn't coupled to flat files.
In fact, most of the data processing is done under the hood by SQLite (**TODO Link**), so adding support for other data processors like Postgres or MySQL is definitely possible.

**Other plot types** I picked those five for the alpha release because they're the most common, but obviously more support can be added. Let me know what other chart types you'd like to see!

## Motivation

If I have a CSV and want to plot a bunch of stuff in it, what's the first step?
Either load it into a spreadsheet or Tableau, or write a Python / R / insert-other-language-with-plot-stuff here.
These are two totally different paradigms - one with no real versioning and high dependence on tools that don't script well, and the other a fully fledged programming language.
The former can be easy to get started (provided you have the software), but doesn't version or share well.
The latter provides you with all the customization you could want, but is usually really verbose, especially in cases where you've got _multiple_ plots you want laid out in a specific way.

There's a similar thread here for data exploration.
I can load my data into a spreadsheet (easy-to-use, inflexible), or I can load it into pandas / dplyr (not-easy-to-use, flexible).
But data analysis has a third option: SQL.
SQL is versionable, scriptable, and straightforward.
It doesn't have the full power of a programming language like R or Python, but it's much better than a spreadsheet.

SVL aims to be the "in-between" language for data visualization: better than a GUI based language, but easier and less flexible than Python and R.

With SVL you get -

* a straightforward declarative syntax,
* scripts that are easily versioned, and
* complex multi-plot layouts that are simple to build.

What you pay - 

* yet another tool in the stack and
* yet another language to learn.

But SVL is pretty simple to install.
If you use the PyData stack you've probably already got nearly every dependency you need.
It's also easy to learn.
The [grammar itself](https://github.com/timothyrenner/svl/blob/master/resources/svl.lark) is less than 150 lines long.
It's smaller and simpler than SQL, and will probably take only hours (if that) to learn.

I built SVL because there were a few scenarios where I wished something like it would exist:

* what's _really_ in this file?
* how did this ML training run go? What results can I expect?
* holy cow why didn't I think to plot X (where X is something I should have plotted, but forgot to) ?