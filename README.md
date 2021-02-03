# Multiprocessing/Multithreading with pytesseract

Another one of my personal projects,I have been writing this from last two days.

---

## What it can do for now:-
- Passing an image, program decides whether to enlarge it or not, enlarging factor that could be changed by default it is 2,that means if the image needs to be enlarged then it would be by the factor of 2.
- Enlarge function also converts the image into Black and white for better readibility simply by using PIL `image.convert()`.
- Without introducing any multithreading or multiprocessing ,the program is around 28% slower,which for smaller files doesn't seems much.
---
### TO RUN:-
- You would need `pytesseract`,`PIL` and *maybe* `numpy` too,if you want to translate text from one non-English to another you would also need `tessdata`.
- You could install all of them with `pip`.

### What I implemented:-
1. An pixel enlarger.
2. Converting an RGB image to Bi-level image, It is better to use PIL's convert function than this one.
3. Multiprocessing using standard module multiprocessing ,further explained below.
4. There are some other helper functions too, not much useful though.
5. Multi-threading using standard module threading.

---
#### How I implemented multiprocessing:-
At first I wanted to split the image into four quadrants and make one process to work upon each.
The problem with this method was collecting text together, for example let's say we have first and second quadrant of the image file. 
For the text reading to make sense you would have to read one line from the quadrant two(left side one) and then read one from quadrant 
one(right side one) and append one behind second, same with third and fourth.

This turns more complex furhter.All the threads would have to interact with each other and 
would have to work according to their intervals.This add stuffs like:-

---
*How would they order themselves ? Would they work in pair ? What if one thread does it jobs before second one would it have to wait ? How thread locking would need to be interacted with global variables ?* and so on.

---
So to keep things simple I split the image into the half horizontally not vertically(*why not ?* -> *It also has it's own complex story*) if it passes the *certain* critertia then given both of the split image file to two cores and make them store the data in a global variable which is a list.

---

#### Some Tests I done:-
- Multithreading was 61% faster than single threading program and 51% faster than multiprocessing program.
- Multiprocessing was 28% faster than single threading program.

---

*29th Jan 2021*
