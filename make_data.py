# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 13:11:58 2024

@author: xfang13
"""

import pandas as pd

q1 = """Create a new Java class called Experiments with a main.
Be sure to include the appropriate comment blocks.
Create the following variables, initializing each of them to an initial value:
    A short named aShort with value 6
    A long named aLong with value 105
    Two ints named int1 and int2 with values 10 and 11
    A float named aFloat with value 1.5 (remember to use 1.5f)
    A double named aDouble with value 100.3"""
    
q2 = """Create a new Java class called Experiments with a main.
Be sure to include the appropriate comment blocks.
Create the following variables, initializing each of them to an initial value:
    A short named aShort with value 6
    A long named aLong with value 105
    Two ints named int1 and int2 with values 10 and 11
    A float named aFloat with value 1.5 (remember to use 1.5f)
    A double named aDouble with value 100.3

Add the following assignment statements to your program, along with a println statement that prints the variable that was assigned into along with a label after each assignment statement:
    aDouble = int2 / 2;
    aDouble = int2 / 2.0;
    aLong = int1 % 2;
    aLong = int1 % 4;
    int1 = int2 % 2;
    int1 = int2 % 3;
    int1 = int2 % 4;
    int1 = 2 + 3 * 4;
    int1 = (2 + 3) * 4

 ****  Example print statement to follow the first assignment statement:  ****
	System.out.println("aDouble = int2 / 2; results in: " + aDouble);
Each of the above variable equations should have an output statement."""    


q3 = """1.	Create a new class with a main method called StringExperiment
    a.	Remember to include required comment blocks
2.	Declare three String variables called:  firstName, middleName, and lastName
    a.	Initialize each with your names
3.	Do each of the following:
    a.	Print your full name with a space between each name. You should follow the format below:
        i.	Last First Middle 
    b.	Print your first name, middle initial followed by a period, and last name.
        i.	First M. Last
    c.	Print your last name in all uppercase letters and first name in all lowercase letters.
        i.	LAST first
    d.	Print the length of your middle name.  Be sure to give it a label.
        i.	Length of middle name = 6
    e.	Calculate the middle position in your middle name and print the letter that is there.  If your name has an even number of letters, it will be one to the right of the middle.

    f.	Print the last letter in your last name.

"""

d = {"topic":['arithmetic']*2+['string'], "question":[q1,q2,q3]}
pd.DataFrame(d).to_csv("data.csv")