# Matrix Digital Rain scroller

## Summary

Most of us would have watched Matrix film, where we notice that the computer screen with black background is shown, with green 
 characters scrolling on it. This script is an attempt to create the digital rain for displaying the output of system commands
 that are typed by a user

## Details:

As of now, 3 lines are allocated for viewing the messages. The first line shows (would show actually), the unread email messages in
 inbox. The second line shows the output of previous command executed. The third line shows system details such as memory used, CPU
 used, disk space etc

## Execution:

Just type the following command:

```python
python matrix.py
```

This is followed by the curses screen being displayed as shown below:

[image] https://github.com/suchindrac/matrix_digital_rain_scroller/raw/main/matrix_screen.png "Initial Screen"

The first section at the top is the help window, and gives basic details such as width and height of the screen and some help messages
The second section is a set of lines, one below another, where messages (emails/outputs of commands/system details) are seen
The third section is the status section where error messages/exceptions are seen

### The commands:

Type in "c" (without the quotes), to enter command mode. Just after that, type a linux command that you want to see the output of, 
 followed by <RETURN> key. Notice that the output of linux command is seen in the second line

Type in "s" (without the quotes) and notice that system details are displayed in the third line as scrolling text

Type in "q" (without the quotes) to quit the application

Below is a video of the application:
