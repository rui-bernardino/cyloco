# Cyloco
Concatenate and date-sort multiple logs files in parallel

# Description
You're investigating some incident and you need to look a bunch of different logs files, each with different date formats and what not, switching back and forth between a bunch of text editors in order to establish a timeline of events...
This "my first python script" handles just that by sorting the files into cronological order and making it a little easier to cope.

# Install
Just copy it to whatever you have a path to and set execute permissions. BAT file included in case you want to use this in Windows.

# Usage
Just pass it whatever you want to concatenate. If you specify nothing, it will open "\*.txt" and "\*.log" in local directory.
## Unix
```
cyloco.py [<file>|<directory>]
```
## Windows
If you use the provided .BAT file (I don't know of another way)
```
cyloco [<file>|<directory>]
```
