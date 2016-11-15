# Updating Douglas County restaurant inspections
*Aidan Connolly, Nov. 2016*

## Table of Contents
1. [Retrieve updated data](#retrieve)
1. [Clean data](#clean)
	* [Converting PDF](#convert)
1. [Create a Fusion Table](#fusiontable)
1. [Update templates](#templates)

<a name="retrieve"></a>
## Retrieve updated data

You should be able to get a listing of restaurant inspections from Douglas County. At this time, a PDF is kept on the [Douglas County Health Department website](http://www.douglascountyhealth.com/food-a-drink/food-facility-ratings).  
Cody Winchester said he was able to get an Excel file from Phil Rooney (669-1602) at one point, but when I contacted him, he said no such file existed.

<a name="clean"></a>
## Clean data

This will depend on the format of the file you get. If you get a PDF, you'll first need to convert it into a manageable filetype. 

<a name="convert"></a>
### Converting PDF

There are different ways to try and convert a PDF. One method that has worked for me is [Cometdocs](http://www.cometdocs.com).   

1. Create an account or login to your account
1. Upload your PDF
1. Click on the "Convert" tab.
1. Drag the uploaded file down into the convert box.
1. Click on "to Excel (xlsx)"
1. Click "Convert"
1. Once the bar stops moving in the "XLS" button, you can click on it to download the converted file

Once you open the Excel file, you'll need to remove the headers and empty row that appear at the top of every page. 

Cometdocs tries to line up data based on its position in the PDF, but empty cells can cause it to put information in the wrong column. 

Make sure all of the cells that should be filled are filled with the correct information. If a cell is blank, the corresponding information may be in an adjacent cell. Just cut it and paste it in the proper location.

Also, with the way the county creates the PDF, some cells run into each other. This causes text to be cut off. Keep an eye out for this.

### Data smells

Before manipulating the data, it's important to make sure the data seems accurate and makes sense. 

From Nikolas Iubel:
>It is often said of data journalists that they interview data just like traditional reporters interview traditional sources. A corollary is that data must be subject to the same scrutiny traditional sources are. Not all sources can be readily trusted and neither can all data sets. But how do data journalists go about determining whether or not a data set demands closer inspection?

>Inspired by the idea of code smells, we take on the task of developing a list of "data smells", that is, red flags in data sets that may indicate data is not be reliable for journalistic purposes.

You should always be wary of blank cells. Find out if they're supposed to be blank and what they mean.

In the case of this data, there are a couple of specific things to look for.

#### Restaurant name

The restaurant names are not perfectly normalized. Some have store numbers. Some store numbers have a space between "#" and the number. 

If you are just using this column to show the name of the restaurant for each record, normalization isn't as important. If you want to analyze the data, normalization is more important. It depends on how much work you want to put in.

#### Address

At this time, only the street address is listed. However, there are multiple towns in Douglas County and the data even includes some Sarpy County locations.

Some records have a town at the end of the address, but not in a normalized way. Some records had a hyphen before the name and some just had a space. 

#### `SEARCH` and `ISNUMBER`

One way to check for the presence of a town name is with Excel's `SEARCH` function combined with `ISNUMBER`.

The `SEARCH` function searches a set of text for a substring and returns the number of the character at which the substring is first found.

The `ISNUMBER` function checks if a value is a number and returns a boolean value.

If used together, the cell will reflect whether the substring was found with a boolean value.

`=ISNUMBER(SEARCH("<substring>",<cell>))`

Replace `"<substring>"` with the town you want to search for and `<cell>` with the cell you're looking at. Then, you can copy down the formula and sort the column. That will place `TRUE` cells together and you can check for the name of a town.

#### `CONCATENATE`

Once you know where each restaurant is located, we need to add the town and state to each address. To do that, we'll use the `CONCATENATE` function.

The `CONCATENATE` function takes multiple strings and combines them into one.

In our case, we want to combine the street address of each restaurant with the town and state.

`=CONCATENATE(<streetcell>,", ",<towncell>,", Nebraska")`

This formula assumes you created a column of town names. If not, just replace `<towncell>` with the name of the town in quotes and copy the formula for all of the restaurants in that town.

Finally, just copy the values you just created and "Paste Special > Values."

#### Rating

The ratings of the restaurants are normalized for the most part, but in the October 2016 data, there were some inconsistencies.

The four ratings the department gives are:

* Superior
* Excellent
* Standard
* Fair

In the October 2016 data, two restaurants had a rating of "Medium," and two had a rating "BMS." Make sure to check for inconsistent data.

#### Current

This column lists the date of the most recent inspection. There may be incorrect data here.  In the October 2016 data, the "Current" value for Cabana Coffee was July 26, 2017. Make sure dates are realistic.

#### Insp# #

I'll be honest. I have no idea what this column means.

#### Risk

The risk of a restaurant is assigned according to the type of food, how it is prepared and the chance of cross-contaminating the food. The three values the department assigns are

* High
* Medium
* Low

Make sure only these three values are present.

### Creating a secondary rating column

When we import our data into a Fusion Table, we'll want to change the color of the points based on the rating of the restaurant. 

To do this, we need a numerical range of ratings.

Text Rating | Numerical Rating
----------- | ----------------
Superior    | 4
Excellent   | 3
Standard    | 2
Fair        | 1

### `VLOOKUP`

The way to add these values to our data is using `VLOOKUP` in Excel.

First, we need a column for new data. Here is how my header row and first entry look.

Name        | Address                         | Text Rating | Numerical Rating | Current  | Insp# | Risk
----------- | ------------------------------- | ----------- | ---------------- | -------- | ----- | ------
Dairy Queen | 5302 S 72 ST, Ralston, Nebraska | Excellent   |                  | 11/12/15 | 88    | MEDIUM

Then, we need a group of reference values for our function. It should look like the corresponding ratings table above. For this example, we'll call the top left cell, "Text Rating," I1 and the bottom right cell, "1," J4.

The `VLOOKUP` function looks for a value in the left column and returns a corresponding value in a different column. In our case, we want to look for the value in the Text Rating column and have it return the corresponding value.

`=VLOOKUP(C2,I$1:J$4,2,FALSE)`

The first value is the cell with the lookup value, in our case that's the text rating. 

The second input is the range of cells with the referece values. You want to give `<TopLeftCell>:<BottomRightCell>`. The dollar signs lock those values so they don't shift when you copy down the formula. 

The third input is the column number in the range of cells with the corresponding value, with 1 being the leftmost column. 

The fourth input tells Excel how specific to be when searching for values. TRUE = find closest match. FALSE = find exact match.

Then, just copy the values and "Paste Special > Values" and delete the reference cells.

### Preparing for export

After you are convinced the data is correct and clean, save it as a CSV file.

## Create a Fusion Table
