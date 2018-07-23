.. strcmp:

strcmp - Character string compare
-----------------------------------------
.. index:: strcmp
.. index:: character string compare

**INDEX:**

	strcmp



**SYNOPSIS:**

.. code-block:: c

	#include <string.h>
	int strcmp(const char *<[a]>, const char *<[b]>);



**DESCRIPTION:**

	<<strcmp>> compares the string at <[a]> to
	the string at <[b]>.



**RETURNS:**

	If <<*<[a]>>> sorts lexicographically after <<*<[b]>>>,
	<<strcmp>> returns a number greater than zero.  If the two
	strings match, <<strcmp>> returns zero.  If <<*<[a]>>>
	sorts lexicographically before <<*<[b]>>>, <<strcmp>> returns a
	number less than zero.



**PORTABILITY:**

<<strcmp>> is ANSI C.

<<strcmp>> requires no supporting OS subroutines.



