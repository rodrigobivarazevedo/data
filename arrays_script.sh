#!/bin/bash
#csv_file="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-LX0117EN-SkillsNetwork/labs/M3/L2/arrays_table.csv"
#wget csv_file

csv_file="./arrays_table.csv"

# parse table columns into 3 arrays
column_0=($(cut -d "," -f 1 $csv_file))
column_1=($(cut -d "," -f 2 $csv_file))
column_2=($(cut -d "," -f 3 $csv_file))

# print first array
echo "Displaying the first column:"
echo "${column_0[@]}"

## Create a new array as the difference of columns 1 and 2
# initialize array with header
column_3=("column_3")
# get the number of lines in each column
nlines=$(cat $csv_file | wc -l)
echo "There are $nlines lines in the file"
# populate the array
for ((i=1; i<$nlines; i++)); do
  column_3[$i]=$((column_2[$i] - column_1[$i]))
done
echo "${column_3[@]}"

: "
In Bash scripting, the dollar sign ($) has different meanings depending on its context:

Variable Expansion: When used in front of a variable name, it is used for variable expansion. For example, $var would be replaced by the value of the variable named "var."

Command Substitution: You can use $(command) or `command` to substitute the output of a command. For example, $(date) would be replaced by the current date when the command is executed.

Arithmetic Expansion: Inside double parentheses (( ... )), the dollar sign $ is used for arithmetic expansion. For example, $(($x + 5)) would perform the arithmetic operation and replace it with the result.

Special Variables: Some special variables in Bash also use the dollar sign as a prefix, such as $0 (script name), $1, $2, ... (command line arguments), and $# (number of arguments).

Escape Character: In double-quoted strings, a backslash \ is used as an escape character to prevent special treatment of the following character. For example, \$ would be treated as a literal dollar sign within double quotes.

Here's a breakdown of some common uses:

$var: Expands the value of the variable named var.
$(command): Substitutes the output of the given command.
$((expression)): Performs arithmetic expansion.
$0: Represents the script name.
$1, $2, ...: Represent command line arguments.
$$: Represents the process ID of the current script or process.
\$: Escapes the dollar sign character itself within double-quoted strings.
In essence, the dollar sign has various roles in Bash, primarily related to variable handling, command substitution, and special variables.
"