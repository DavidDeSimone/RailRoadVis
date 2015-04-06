RailRoadVis is a railroad visualization based in the broswer, rendered with d3.js

The tool used to visualize the data is a web page (called view.html). This page accepts graphs seralized
in JSON format, and accepts them via AJAX requests.

The project is broken into two modules, /src and /web

/src contains all of the scripts used to generate the JSON graphs used by the web view, and the statistic spreadsheets
     One script handles the graph formation, and the spreadsheet export (single_graph_form.py).
     You can generate a JSON file for a crossing by invoking python single_graph_form.py <Crossing id>
     You can generate ALL JSON files (with multi-core optimizations) by invoking python single_graph_form.py <multi_all>
     You can generate the spreadsheet for ALL crossing with python single_graph_form.py <multi_export>
     All JSON files will be placed in the /src/crossings folder

/web contains all of the materials needed for the webpage view

/web/html contains the static HTML files used for viewing, and the JSON files needed for viewing. The view page
will perform an AJAX request to the local directory (/web/html) for the JSON graph files.

/web/css contains the CSS files used by the html view.

/web/js contains the javascript libraries used by the html view

/web/server contains the python server used in automated screenshot export. NOTE: This server NEEDS to be running in order to support automated screenshot export. To run the server, run python ss_server.py