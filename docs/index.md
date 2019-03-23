# Welcome to SVL

SVL is a declarative, SQL-like language for data visualizations.
It's designed to make it very easy to build simple or complex dashboard-like collections of plots for data in flat tabular files.
Like SQL, there are no variables, loops, if/else statements or data structures.
You declare your datasets, describe the charts you want built and how they're arranged, and SVL will produce an HTML file with your plots.

## Installation

To install SVL, you need Python 3.5+ and pip.
If you've got that ready, install with

```
pip install -U svl
```

After that, you're all set.

## Quickstart

***TODO***

If you'd like to read more about what's in SVL and why I created it, read on!

Or maybe you want to go deeper and head into the [tutorials](tutorials/basic_svl.md).

## SVL is...

* **Simple** - no variables, control flow statements, or data structures. Just like SQL.
* **Easy** - syntax _feels_ like SQL, with actual SQL support for in-script data manipulation.
* **Small** - the entire [grammar](https://github.com/timothyrenner/svl/blob/master/resources/svl.lark) is under 150 lines long.

## Alpha Features

✅ **Easy to learn**: The entire grammar is under 150 lines.

🖐 **Five chart types**: Line, bar, scatter, histogram and pie. I plan on adding more, so if I'm missing your favorite one let me know.

📈 **Complex layouts**: SVL scripts can support any number of plots and makes it straightforward to arrange them so that the most important plots get the most real estate.

📊 **Interactive HTML output**: SVL uses [Plotly](https://plot.ly/javascript/) to draw the visualizations, and produces an easily shareable but still interactive HTML file.

📂 **CSV and Parquet files**: Currently the data is limited to files, and SVL has support for CSV and (if [pyarrow](https://arrow.apache.org/docs/python/) is installed) parquet files.

## Not Alpha Features, but Possible

**Other plot backends** The compiler isn't married to Plotly.
SVL can have future support for other backends like Vega, Bokeh, or even Matplotlib (probably).

**Other data sources** For simplicity SVL operates on files, but like the plot renderer the compiler isn't coupled to flat files.
In fact, most of the data processing is done under the hood by [SQLite](https://sqlite.org/index.html), so adding support for other data processors like Postgres or MySQL is definitely possible.

**Other plot types** I picked those five for the alpha release because they're the most common, but obviously more support can be added. Let me know what other chart types you'd like to see!

## Why SVL

I do data science and machine learning for a living, so I make a lot of plots.
Some of those plots are for exploratory purposes inside a notebook environment, and usually I use [Seaborn](https://seaborn.pydata.org/) or, more recently, [Chartify](https://github.com/spotify/chartify).
If I'm in R (which isn't too often these days), obviously [ggplot](https://ggplot2.tidyverse.org/) is the way to go.
All of these libraries are great and offer a nice balance of customizability and conciseness when building individual plots.
There are two things I notice while I'm working with these tools.

1. I can never remember enough commands to make a plot without consulting documentation. Never. Maybe I just don't do it enough, but these libraries have complicated APIs and I can't keep them in my head.
2. I tend to make the same kinds of plots over and over again. Yes there are all sorts of powerful things you can do with these libraries to make publication-quality charts, but honestly I pretty much just make scatter plots and histograms and like one bar chart per project.

There's another scenario I use plots for - operational metrics.
When I execute a training / offline prediction run for a machine learning model, I want to visualize a whole bunch of stuff all at once to get a "feel" for what the model's doing with the features, and what kind of impacts we'll expect to put onto our downstream consumers.
These are basically operational dashboards (like what you'd make with Splunk or Datadog), but for machine learning models.
For these plots I don't want super customized stuff, I just want simple visualizations to give me a feel for what's going on in one place.
Now I could just have a notebook that does this for me - in fact the [Lore](https://github.com/instacart/lore) framework from Instacart takes this approach, but there are a number of issues with using a notebook for operational stuff:

- difficult to automate (some progress has been made in this area recently)
- difficult to version (hey, another repo that's 99.8% "Jupyter Notebook"!)
- difficult to share (maybe nobody wants to see bad notebook code?)

I do often write scripts for operational plots for these ML pipelines, but it's a lot of work.
There's the verbosity of the plots themselves, plus I have to read the data myself, then I have to write the code for laying the plots out so they're visually coherent.
I found myself wishing there was some way for me to just write a plot like this:

```
SCATTER dataset
    X field1
    Y field2
```

If `dataset` were a table or file with `field1` and `field2` this would be really easy to remember.
Better still, if I could put multiple plots like this in one script file, I could control which plots appear together to make it easier to get a feel for the data.
Like if I wanted histograms of `field1` and `field2` underneath my scatter plot I could write:

```
SCATTER dataset
    X field1 Y field2

CONCAT(
    HISTOGRAM dataset X field1
    HISTOGRAM dataset X field2
)
```

and the scatter plot would be on top, and the histograms would be next to each other underneath it.

After thinking about it a bit, I realized what I wanted was SQL for plots.
SQL doesn't have variables, objects or control structures.
There are some things that it's not well suited for, but for a huge amount of tabular data processing and manipulation it's easily the simplest tool for the job.
SQL sits squarely between "spreadsheet" and "pandas/dplyr" on the simplicity<->flexibility spectrum for data processing.

***TODO Diagram***

SVL sits between "GUI program" and "seaborn/ggplot" for data visualization.

***TODO Diagram***

My goal in creating SVL isn't to replace my usual set of plotting tools, it's to get me making _more plots, faster_.
Hopefully you will find SVL as useful as I do.