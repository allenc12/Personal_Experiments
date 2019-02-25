/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_float_rounding.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: evjohnst <evjohnst@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/01/09 13:41:47 by evjohnst          #+#    #+#             */
/*   Updated: 2019/01/31 16:00:21 by callen           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <math.h>
#include <limits.h>
#include <float.h>
#include <string.h>
#include <stdint.h>
#include <stdio.h> //TODO: remove

union	ldshape {
	long double	f;
	struct {
		uint16_t se;
		uint64_t m;
	} i;
};

long double ft_fmodl(long double x, long double y)
{
	union ldshape ux = {x}, uy = {y};
	int ex = ux.i.se & 0x7fff;
	int ey = uy.i.se & 0x7fff;
	int sx = ux.i.se & 0x8000;

	if (y == 0 || isnan(y) || ex == 0x7fff)
		return (x*y)/(x*y);
	ux.i.se = ex;
	uy.i.se = ey;
	if (ux.f <= uy.f) {
		if (ux.f == uy.f)
			return 0*x;
		return x;
	}
	/* normalize x and y */
	if (!ex) {
		ux.f *= 0x1p120f;
		ex = ux.i.se - 120;
	}
	if (!ey) {
		uy.f *= 0x1p120f;
		ey = uy.i.se - 120;
	}
	/* x mod y */
	uint64_t i, mx, my;
	mx = ux.i.m;
	my = uy.i.m;
	for (; ex > ey; ex--) {
		i = mx - my;
		if (mx >= my) {
			if (i == 0)
				return 0*x;
			mx = 2*i;
		} else if (2*mx < mx) {
			mx = 2*mx - my;
		} else {
			mx = 2*mx;
		}
	}
	i = mx - my;
	if (mx >= my) {
		if (i == 0)
			return 0*x;
		mx = i;
	}
	for (; mx >> 63 == 0; mx *= 2, ex--);
	ux.i.m = mx;
	/* scale result */
	if (ex <= 0) {
		ux.i.se = (ex+120)|sx;
		ux.f *= 0x1p-120f;
	} else
		ux.i.se = ex|sx;
	return ux.f;
}


int		fill_ipart_ld(long double n, char *str, int i)
{
	long double	div;
	long double	tmp;
	int			digit;

	div = 1;
	tmp = n / 10;
	while (div <= tmp)
		div *= 10;
	while (div >= 1)
	{
		digit = (int)(n / div);
		str[++i] = digit + '0';
		n -= div * digit;
		div /= 10;
	}
	return (i);
}

/* long double	ft_powl(long double x, long double y) */
/* { */
/* 	long double	m; */

/* 	if (y == 0.0L) */
/* 		return (1.0L); */
/* 	if (fmodl(y,2.0L) == 0.0L) */
/* 	{ */
/* 		m = ft_powl(x, y / 2.0L); */
/* 		return (m * m); */
/* 	} */
/* 	else */
/* 		return (x * ft_powl(x, y - 1.0L)); */
/* } */
long double	ft_powl(long double x, long double y);

char	*ft_dtoa(long double n, unsigned int prec)
{
	char		str[1076];
	int			i;

	//catch infinities?
	i = -1;
	if (n < 0)
	{
		str[++i] = '-';
		n = -n;
	}
	n += 5.0L * 10.0L * (int)(-prec - 1);
	i = fill_ipart_ld(n, str, i);
	if (prec)
	{
		str[++i] = '.';
		while (prec)
		{
			n = 10 * (n - (long)n);
			str[++i] = (long)n + '0';
			--prec;
		}
	}
	str[++i] = '\0';
	return (strdup(str));
}

#include <stdlib.h>
int		main(int ac, char **av)
{
	char *res,*stdlc,*libft;
	long double x;
	int prec;

	if (ac >= 2)
		prec = atoi(av[1]);
	else
		prec = 6;
	x = (long double)FLT_MAX;
	res = ft_dtoa(x, prec);
	asprintf(&libft, "%s", res);
	asprintf(&stdlc, "%.*Lf", prec, x);
	// if (strcmp(libft, stdlc)) {
		// printf("ft_dtoa output differs from Libc\'s dtoa:\n");
	// }
	printf("  stdlc [%s]\nevlibft [%s]\n", stdlc, libft);
	free(stdlc);
	free(libft);
	free(res);
	return (0);
}
