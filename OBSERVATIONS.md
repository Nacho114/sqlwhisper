# Prompting observations

## Toy data

## Stock data

TODO 

## Artist data

Here we only get 1/5.

```
Enter query: What are all the albums that Kendrick has in this db?
Validating user query:

 What are all the albums that Kendrick has in this db?...

Query valid, converting to sql...

SQL query:

SELECT album FROM artist_data WHERE name = 'Kendrick' ORDER BY created_at;

   album
0  DAMN.
```

Here we only get 3/5, by specifying that there might be an alias.

```
Enter query: What are all the albums that Kendrick has in this db? Note that he might have other alises!
Validating user query:

 What are all the albums that Kendrick has in this db? Note that he might have other alises!...

Query valid, converting to sql...

SQL query:

SELECT album FROM artist_data WHERE name ILIKE '%Kendrick%'

                           album
0                          DAMN.
1         good kid, m.A.A.d city
2  Mr. Morale & the Big Steppers
```
