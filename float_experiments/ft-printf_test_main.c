#include <stdio.h>
#include <float.h>
#include <limits.h>
#include <locale.h>
#include "libft.h"

#define PI100	3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067
#define LMAXD	9223372036854775807.0
#define BINGUS	9223372036854775295.0
#define ULMAXD	18446744073709551615.0
#define CROGUS	18446744073709550592.0
#define FLUBNIB	47778931862957161709568.0
#define BINBLUF	(long double)3475880078629571617095689999.0
#define STEST	"s[%s]\n", "blabbo\0wumdingers"
#define WSTEST	"S[%.4S]\n", L"\x1f44c\x1f44c\x1f44c"
#define CTEST	"c[%c]\n", 'H'
#define WCTEST	"C[%C ]\n", L'\x1f44c'
#define PTEST	"p[%p]\n", &ptr
#define ITEST	"i[%+56.13i]\n", -0x7FFFFFFF
#define DTEST	"d[%+56.13d]\n", -0x7FFFFFFF
#define LDTEST	"D[%+56.13D]\n", -1
#define OTEST	"o[%#48.10zo]\n", 360038650UL
#define LOTEST	"O[%O]\n", -1
#define UTEST	"u[%u]\n", -1
#define LUTEST	"U[%U]\n", -1
#define HTEST	"x[%x]\n", -1
#define LHTEST	"X[%X]\n", -1
#define NTEST	"n[hej%n]\t", &ptr
#define NVAL	"n[%d]\n", ptr
#define ATEST	"a[%a]\n", BINGUS
#define LATEST	"A[%A]\n", BINGUS
#define ETEST	"e[%e]\n", BINGUS
#define LETEST	"E[%E]\n", BINGUS
#define FTEST	"f[%f]\n", DBL_MAX
// [ERROR] diff on output for format "^.^/%49.22lf^.^/" and arg: -9223372036854775808.000000 {this test is wrong}
#define LFTEST	"F[%F]\n", FLT_MAX
#define GTEST	"g[%g]\n", BINGUS
#define LGTEST	"G[%G]\n", BINGUS
#define ASTTEST	"*[%*.sbigfunny]\n", 12, "flippino"

int		main(void)
{
	int ft = 0;
	int pf = 0;
	setlocale(LC_ALL, "en_US.UTF-8");
	int ptr = 0;
	/* pf += printf(STEST);ft += ft_printf(STEST);		//? */
	/* pf += printf(WSTEST);ft += ft_printf(WSTEST);	//? */
	/* pf += printf(CTEST);ft += ft_printf(CTEST);		//? */
	/* pf += printf(WCTEST);ft += ft_printf(WCTEST);	//? */
	/* pf += printf(PTEST);ft += ft_printf(PTEST);		//? */
	/* pf += printf(DTEST);ft += ft_printf(DTEST);		//? */
	/* pf += printf(ITEST);ft += ft_printf(ITEST);		//? */
	/* pf += printf(LDTEST);ft += ft_printf(LDTEST);	//? */
	/* pf += printf(OTEST);ft += ft_printf(OTEST);		//? */
	/* pf += printf(LOTEST);ft += ft_printf(LOTEST);	//? */
	/* pf += printf(UTEST);ft += ft_printf(UTEST);		//? */
	/* pf += printf(LUTEST);ft += ft_printf(LUTEST);	//? */
	/* pf += printf(HTEST);ft += ft_printf(HTEST);		//? */
	/* pf += printf(LHTEST);ft += ft_printf(LHTEST);	//? */
	/* pf+=printf(NTEST);pf+=printf(NVAL);ptr=0;		//: */
	/* ft+=ft_printf(NTEST);ft+=ft_printf(NVAL);ptr=0;	//G */
	/* pf += printf(FTEST);ft += ft_printf(FTEST);		//? */
	/* pf += printf(LFTEST);ft += ft_printf(LFTEST);	//? */
	/* pf += printf(ATEST);ft += ft_printf(ATEST);		//? */
	/* pf += printf(LATEST);ft += ft_printf(LATEST);	//? */
	/* pf += printf(GTEST);ft += ft_printf(GTEST);		//? */
	/* pf += printf(LGTEST);ft += ft_printf(LGTEST);	//? */
	/* pf += printf(ETEST);ft += ft_printf(ETEST);		//? */
	/* pf += printf(LETEST);ft += ft_printf(LETEST);	//? */
	/* pf += printf(ASTTEST);ft += ft_printf(ASTTEST);	//? */
	/* pf += printf("%d\n", ULLONG_MAX);ft += ft_printf("%d\n", ULLONG_MAX); */
	/* (void)ptr; */
	pf += fprintf(stdout, "puscetti\n");ft += ft_fprintf(stdout, "puscetti\n");
	printf("ft[%d] pf[%d]\n",ft,pf);
}

