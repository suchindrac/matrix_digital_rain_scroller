# Matrix Digital Rain scroller

## Summary

Most of us would have watched Matrix film, where we notice that the computer screen with black background is shown, with green 
 characters scrolling on it. This script is an attempt to create the digital rain for displaying the output of system commands
 that are typed by a user

## Details:

As of now, 5lines are allocated for viewing the messages:
  * The first line shows (would show actually), the unread email messages in inbox (TBD)
  * The second line shows the output of previous command executed
  * The third line shows system details such as memory used, CPU used, disk space etc
  * The fourth and fifth lines (added recently) show subliminal messages

To be concise: Subliminal messages enter into your subconscious mind (which is in a higher dimension), when you create "patterns" of events and make those patterns miss conscious mind. This technique generates pattern of events through scrolling, as compared to flickering of messages on screen

## Execution:

NOTE: To ensure transparency can be enjoyed, you will have to enable transparency in your terminal as follows:

* Go to Preferences -> Profile "Default"
* Select "Use transparent background" and set the slider to full
* Then execute the following command:

```python
python3 matrix.py
```

This is followed by the curses screen being displayed as shown below:

![alt text](https://github.com/suchindrac/matrix_digital_rain_scroller/raw/main/matrix_screen.png "Initial Screen")

The first section at the top is the help window, and gives basic details such as width and height of the screen and some help messages
The second section is a set of lines, one below another, where messages (emails/outputs of commands/system details) are seen
The third section is the status section where error messages/exceptions are seen

### The commands:

Type in "c" (without the quotes), to enter command mode. Just after that, type a linux command that you want to see the output of, 
 followed by <RETURN> key. Notice that the output of linux command is seen in the second line

Type in "s" (without the quotes) and notice that system details are displayed in the third line as scrolling text

Type in "q" (without the quotes) to quit the application

Type in "b" (without the quotes) to display subliminal messages on line 4

Below is a video of the application:

https://github.com/suchindrac/matrix_digital_rain_scroller/raw/main/matrix_scroller.mp4
