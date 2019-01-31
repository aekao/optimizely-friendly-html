# Optimizely-friendly HTML

This script takes an .HTML file and outputs an Optimizely-friendly string, ready to be copy/pasted into your Optimizely experiment.

## Prerequisites

Please make sure you have installed Beautiful Soup: https://www.crummy.com/software/BeautifulSoup/

## What it does, specifically

It converts HTML like this:
```
    <div class="example" aria-label="Program information">
        <p class="revo-aware-title">This course is 1 of {totalCourses} in a series from {org}</p>
        <p> Want to keep learning after you finish this course? </p>
    </div>
```

into something you can directly copy/paste into Optimizely.

```
'<div aria-label="Program information" class="example">' +
    ' <p class="revo-aware-title">' +
    '  This course is 1 of ' + totalCourses + ' in a series from ' + org + 
    ' </p>' +
    ' <p>' +
    '  Want to keep learning after you finish this course?' +
    ' </p>' +
    '</div>';
```


## How to
 
```
python optimizely-friendly.py [ .HTML filename ] [ (optional) element class to format ] [ (optional) number of preceding spaces in each line ]
```

If you do not provide an element class, this script will reformat the entire .HTML file. The number of preceding spaces in each line is customizable so your code can look nicely tabbed over in the Optimizely editor.

In your .HTML file, you may want to use JS variables, like so:

```
'<a class="revo-aware-program-link" href="' + programUrl + '">Visit Program Page</a>'
```

This script will format it appropriately, if you enclose JS variables in curly braces with no spaces, like this: 

```
<a class="revo-aware-program-link" href="{programUrl}">Visit Program Page</a>
```

## Authors

* **Audrey Kao**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
