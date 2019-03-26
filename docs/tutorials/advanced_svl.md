# Advanced SVL

The [basic SVL](basic_svl.md) tutorial covered how to make, customize and arrange plots.
SVL also has advanced SQL-powered data processing capabilities that make it easy to adjust your datasets without writing a bunch of additional code.

Before getting in to the SQL parts, there are a couple of things to cover first.
This tutorial uses the same dataset as the basic tutorial.
I'll go ahead and use the `basic_tutorial.svl` script from the basic SVL tutorial as a starting point.

```
cp basic_tutorial.svl advanced_tutorial.svl
```

## Sorting Data

Suppose I want to see which states have the most bigfoot sightings.
That's pretty easy.
Add this underneath the line chart.

```
BAR bigfoot
    TITLE "Bigfoot Sightings by State"
    X state LABEL "State"
    Y state COUNT LABEL "Number of Sightings"
```

It looks like this:

![](../images/advanced_tutorial_sort_bar_1.png)

Notice that it's unsorted.
SVL supports sorting an axis as a modifier.

```
BAR bigfoot
    TITLE "Bigfoot Sightings by State"
    X state LABEL "State"
    Y state COUNT LABEL "Number of Sightings" SORT DESC
```

Now our bar chart looks like this:

![](../images/advanced_tutorial_sort_bar_2.png)

`SORT` must be followed by `ASC` or `DESC`.

Here's the full script.

```
DATASETS
    bigfoot "bigfoot_sightings.csv"

LINE bigfoot
    TITLE "Bigfoot Sightings by Year"
    X date BY YEAR LABEL "Year of Sighting"
    Y number COUNT LABEL "Number of Sightings"
    SPLIT BY classification

BAR bigfoot
    TITLE "Bigfoot Sightings by State"
    X state LABEL "State"
    Y state COUNT LABEL "Number of Sightings" SORT DESC

CONCAT(
    HISTOGRAM bigfoot
        TITLE "Bigfoot Sighting Moon Phases"
        X moon_phase LABEL "Moon Phase"
        STEP 0.1

    (
        BAR bigfoot
            TITLE "Number of Bigfoot Sightings by Classification"
            X classification LABEL "Sighting Classification"
            Y number COUNT LABEL "Number of Sightings"

        PIE bigfoot
            TITLE "Number of Bigfoot Sightings by Classification"
            AXIS classification
            HOLE 0.3
    )
)

SCATTER bigfoot
    TITLE "Bigfoot Sighting Temperature by Latitude"
    X latitude LABEL "Latitude"
    Y temperature_mid LABEL "Temperature (F)"
    COLOR BY moon_phase "YlOrRd" LABEL "Moon Phase"
```

![](../images/basic_tutorial_additional_axes_1.png)
![](../images/advanced_tutorial_sort_bar_2.png)
![](../images/basic_tutorial_additional_axes_2.png)
![](../images/basic_tutorial_additional_axes_3.png)

Interactive version [here](../sample_visualizations/advanced_tutorial_sort.html)

## Datasets at the Command Line

Sometimes it might be convenient not to have the name of the file hard coded into the SVL script.
For example, suppose you've got a pipeline that produces files with dates in the name.
It would be nice if you could create the same visualizations and treat the file as a parameter.
SVL supports passing in dataset file definitions from the command line.
In fact, the `DATASETS` declaration is optional.

```
-- No DATASETS!

LINE bigfoot
    TITLE "Bigfoot Sightings by Year"
    X date BY YEAR LABEL "Year of Sighting"
    Y number COUNT LABEL "Number of Sightings"
    SPLIT BY classification

BAR bigfoot
    TITLE "Bigfoot Sightings by State"
    X state LABEL "State"
    Y state COUNT LABEL "Number of Sightings" SORT DESC

CONCAT(
    HISTOGRAM bigfoot
        TITLE "Bigfoot Sighting Moon Phases"
        X moon_phase LABEL "Moon Phase"
        STEP 0.1

    (
        BAR bigfoot
            TITLE "Number of Bigfoot Sightings by Classification"
            X classification LABEL "Sighting Classification"
            Y number COUNT LABEL "Number of Sightings"

        PIE bigfoot
            TITLE "Number of Bigfoot Sightings by Classification"
            AXIS classification
            HOLE 0.3
    )
)

SCATTER bigfoot
    TITLE "Bigfoot Sighting Temperature by Latitude"
    X latitude LABEL "Latitude"
    Y temperature_mid LABEL "Temperature (F)"
    COLOR BY moon_phase "YlOrRd" LABEL "Moon Phase"
```

is what our Bigfoot SVL script looks like without a `DATASETS` declaration.
It won't compile without one additional command line argument.

```
svl advanced_tutorial.svl --dataset bigfoot=bigfoot_sightings.csv
```

You can pass multiple files with different labels by repeating `--dataset label=path` for each file.

## Filtering Data

## Transforming Data

## Custom Datasets

## Conclusion
