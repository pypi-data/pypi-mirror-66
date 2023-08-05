# Factiva Country Code Mapping

This utility simplifies mapping between country names, DJII region codes, and ISO Alpha 2 country codes. There were two approaches explored in this implementation: the first was to create a list containing lists for each mapping of country name to DJII RC to ISO Alpha 2 code, and the second was to create three separate dictionaries with each of the various data type as keys. This was both a simple exercise to compare O(n) between searching the underlying data using lists vs dictionaries, as well as to actually transform data files being used with the Factiva search engine.

## Installation

To install this library, run the following commands.

    $ pip install -i factiva-country-code-mapping

## Usage

The utility can be run by adding csv files to the 'process' folder; the input files should contain a newline ('\n') delimited list of country codes, DJII region codes, or ISO Alpha 2 country codes that are to be mapped to either of the other two data types. I've included some sample inputs and outputs in the 'process' folder - both inputs should be uploaded there and outputs will be displayed there. This utlity will output the other two data types by running the following command.

    python -m country_code_mapping <input file> [method-options] [output-options]
    
*<*input file*>* - filename of input file located in the 'process/input' folder

*[method-options]* - method of parsing with the below values
l = list approach (slower)
d = dictionaries approach (faster)

*[output-options]* - preferred output format with the below values
1 = standard country names
2 = DJII region codes
3 = ISO Alpha 2 country codes
