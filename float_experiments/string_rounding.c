#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <float.h>
#include <limits.h>
#include <math.h>
#include <fcntl.h>
#include <stdio.h>

/*
 * Round up the given digit string.  If the digit string is fff...f,
 * this procedure sets it to 100...0 and returns 1 to indicate that
 * the exponent needs to be bumped.  Otherwise, 0 is returned.
 */
static int	roundup(char *s0, int ndigits)
{
	char *s;

	s = s0 + ndigits - 1;
	while (*s == 0xf)
	{
		if (s == s0)
		{
			*s = 1;
			return (1);
		}
		*s = 0;
		s--;
	}
	++*s;
	return (0);
}

/*
 * Round the given digit string to ndigits digits according to the
 * current rounding mode.  Note that this could produce a string whose
 * value is not representable in the corresponding floating-point
 * type.  The exponent pointed to by decpt is adjusted if necessary.
 */
static void	dorounding(char *s0, int ndigits, int sign, int *decpt)
{
	int adjust;		/* do we need to adjust the exponent? */

	adjust = 0;
	if (FLT_ROUNDS == 1)		/* to nearest, halfway rounds to even */
		if ((s0[ndigits] > 8) || (s0[ndigits] == 8 && s0[ndigits + 1] & 1))
			adjust = roundup(s0, ndigits);
	if (FLT_ROUNDS == 2)		/* toward +inf */
		if (sign == 0)
			adjust = roundup(s0, ndigits);
	if (FLT_ROUNDS == 3)		/* toward -inf */
		if (sign != 0)
			adjust = roundup(s0, ndigits);
		/* toward zero */
		/* implementation-defined */
	if (adjust)
		*decpt += 4;
}

int		main(void)
{
	// float f = 0.15625f;
	double d = DBL_MAX;
	char *res, *h;
	int decpt;
	// long double l = 0.15625L;

	decpt = 0;
	asprintf(&res, "%.0f", d);
	asprintf(&h, "%.0f", d);
	dorounding(res, 99, 0, &decpt);
	if (strcmp(res,h))
	printf("res{%s}\n", res);
	printf("  h{%s}\n", h);
	return (0);
}
