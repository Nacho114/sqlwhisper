# The problem

The goal is to go from a query written in English into an sql query.

To get a sense of some of the edge cases we might face, we'll look at a couple
of examples.

For each problem:

1. Write an llm that converts text to and sql query
2. Test it out with the queries found in X
3. Next, you are now allowed to inject extra context in the prompt.
4. Hard: you are allowed to query GPT, to look into it's own data
to create context for itself. 

## A tale of three problems

### Different naming convention: Stock data

In the first example we are looking at the futures prices of gold, silver and copper.
The symbols used for these are GC=F, SI=F, CL=F.

The issue is that the user might as for the latest gold price, without knowing that
the symbol for gold is GC=F

 symbol | open_price
--------+------------
 GC=F   |  2818.2000
 SI=F   |  2827.6001
 CL=F   |   105.6400

### Duplicate names: Artist data

Here we look at an example where we might have several names for the same artist.

The problem here is that if a user asks for all the albums of Tupac, we might miss
some of the albums using his alias!

                 album                 |      name      | downloads
---------------------------------------+----------------+-----------
 All Eyez on Me                        | Tupac          |   9800000
 Me Against the World                  | 2Pac           |   5400000
 The Don Killuminati: The 7 Day Theory | Makaveli       |   4000000

### Hidden rules: Toy data

In this last example we combine the previous two problems with an added twist.

let X = a...a be some string of a's

Then "dark" = X is even
Then "light" = X is odd

So when a user asks for something like, 

"Give me the value of dark"

The SQL query should be something like

"SELECT SUM(value) FROM toy_data WHERE LENGTH(name) % 2 = 0"

However, without any extra context, the llm will surely fail!

  name  | value
--------+-------
 aaaa   |  6015
 a      |  6583
 aa     |  3250
 aaa    |  1140

## Bonus points

How well do the solutions scale to db size?
