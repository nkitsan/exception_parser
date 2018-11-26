# Exeption parser for python exeptions

## Steps of solution:

1. Find the difference between python3 and python2 
	Result: no difference was found.

2. How user is going to pass params to the library functions
	Result: User can add a path to a log folder (absolute or relative)
	or with a path define a file. In the first case all files from folders
	and subfolders will be parsed.

3. Think about the format of files with exeption
	Result: file-log examples represented in logs folder 
	(regular traceback format).

4. Consider all ways of parsing strings
	Result: parse each string of a file with the help of regexp
	At first step undestand which line of a traceback it is
	Then parse all params to dict.

5. Problem with the defining place of an exeption: a line of code is not enought to find a problem
	Result: added param 'file' which defines file where exeption was raised.


6. Print result with json indent
	Result: json module function was used
