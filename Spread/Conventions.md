# Coding Conventions

### Variables Names 
- They will start with a lowercase letter.  Phrases will be represented by using a capital letter for 
the start of each word in the phrase (except for the first word).

- Typing is faster than looking up variable names, especially with modern IDEs (Integrated Development
Environments) which dramatically reduce the cost of typing.  So care should be taken to make it easy
to learn and memorize the variable names, at least withing a collection of related code.

- Consistency and symmetry of variable names within a collection of related code makes the code much easier
to maintain.  It also makes it easier to spot some kinds of bugs when proofreading your code.

- Slightly longer variable names than is common in the wider community are to be encouraged, but very 
long variable names are undesirable.

- How long is too long depends on how hard it is to create a name that is descriptive.  But around 12
characters is around the transition to being too long.

- Variable names should be singular, not plural; e.g., *node* not *nodes*.  Using plural for lists and
singular for elements is occasionally useful.  But as a convention using plurals for all lists is a
little bit tedious.  More serious problem arise when the variable name is not the "name" of the element.
For example, *mapIdToList* is awkward as *mapIdToLists*, because the element type is a list not a list 
of list.

- When it is desirable to have the same name for a variable describing a list and an element of the list
there are two solutions:

  1) Use a shorter form of the list name for the element name.  For example ```for n in names```.  If 
  the scope of the short name is limited (e.g., less than about 10 lines) this is a good solution in
  spite of the fact that variable name would be too cryptic for more general uses.

  2) Append the suffix 'L' onto the name of the list.  For example ```for node in nodeL```.  This works
  for larger scopes.  It also avoids name conflicts that may occurs with very short variable name (e.g.
  *n* might be used elsewhere in the scope for the number of iterations)

### Function Names
- Will start with a capital letter, but otherwise be the same as variable names.

- Capitalization is done so that variable names and function names can be the same without conflicting.  
A common pattern is for a function to return a result that in the caller's context is most logically
associated with the function.  In this case using the function name for the result of the function is
convenient, but would not be allowed if the function names are lower case.

### Line Widths
Lines should be no widder than 120 characters.

Lines that are so long that they wrap on a normal screen are quite disruptive.  Not all developers have
super wide screens.

In addition reading the code becomes slower if the line is too long.  This is analogous the fixation
width when reading a book.  If the columns are too long it slows the reading processes.  In many cases
readability is maximised at between 60 and 80 characters.  Nevertheless 80 characters is a restrictive
as a limit

120 characters allows for landscape printing of the code.  Need to check that this works for portrait 
monitor.