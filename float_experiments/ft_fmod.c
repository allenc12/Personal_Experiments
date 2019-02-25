/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_fmod.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: callen <callen@student.42.us.org>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/01/21 11:00:08 by callen            #+#    #+#             */
/*   Updated: 2019/01/21 16:27:21 by callen           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <math.h>

union	u_dbl
{
	double		f;
	uint64_t	i;
};

double	ft_fabs(double x)
{
	union u_dbl u;

	u.f = x;
	u.i &= -1ULL/2;
	return (u.f);
}

double	ft_frexp(double v, int *e)
{
	*e = ((uint64_t)(v) >> 52 & 0x7ff);
	return (v);
}

double	ft_fmod(double x, double y)
{
	union u_dbl	ux;
	union u_dbl	uy;
	int			ex;
	int			ey;
	int			sx;
	uint64_t	i;
	uint64_t	uxi;

	ux.f = x;
	uy.f = y;
	ex = ux.i >> 52 & 0x7ff;
	ey = uy.i >> 52 & 0x7ff;
	sx = ux.i >> 63;
	uxi = ux.i;
	if (uy.i << 1 == 0 || isnan(y) || ex == 0x7ff)
		return ((x * y) / (x * y));
	if (uxi << 1 <= uy.i << 1)
	{
		if (uxi << 1 == uy.i << 1)
			return (0 * x);
		return (x);
	}
	if (!ex)
	{
		i = uxi << 12;
		while (i >> 63 == 0)
		{
			ex--;
			i <<= 1;
		}
		uxi <<= -ex + 1;
	}
	else
	{
		uxi &= -1ULL >> 12;
		uxi |= 1ULL << 52;
	}
	if (!ey)
	{
		i = uy.i << 12;
		while (i >> 63 == 0)
		{
			ey--;
			i <<= 1;
		}
		uy.i <<= -ey + 1;
	}
	else
	{
		uy.i &= -1ULL >> 12;
		uy.i |= 1ULL << 52;
	}
	while ( ex > ey)
	{
		i = uxi - uy.i;
		if (i >> 63 == 0)
		{
			if (i == 0)
				return (0 * x);
			uxi = i;
		}
		uxi <<= 1;
		ex--;
	}
	i = uxi - uy.i;
	if (i >> 63 == 0)
	{
		if (i == 0)
			return (0 * x);
		uxi = i;
	}
	while (uxi >> 52 == 0)
	{
		uxi <<= 1;
		ex--;
	}
	if (ex > 0)
	{
		uxi -= 1ULL << 52;
		uxi |= (uint64_t)ex << 52;
	}
	else
		uxi >>= -ex + 1;
	uxi |= (uint64_t)sx << 63;
	ux.i = uxi;
	return (ux.f);
}
#include <stdio.h>
#include <float.h>
void	print_dbin(double x)
{
	union {double f; uint64_t i;} ux = {x};
	int i = 0,j;
	char out[67] = {0};
	out[i++] = ((1L << 63) & ux.i ? '1' : '0');
	out[i++] = ' ';
	for (j = 62; j > 51; j--)
		out[i++] = (1 << j) & ux.i ? '1' : '0';
	out[i++] = ' ';
	for (j = 51; j >= 0; j--)
		out[i++] = (1 << j) & ux.i ? '1' : '0';
	printf("/sign (1 bit)\n");
	printf("| /exponent (8 bit)\n");
	printf("| |           /fraction (23 bit)\n");
	printf("| |---------| ");
	printf("|--------------------------------------------------|\n%s",out);
}

void	print_fbin(float x)
{
	union {float f; uint32_t i;} ux = {x};
	printf("/sign (1 bit)\n");
	printf("| /exponent (8 bit)\n");
	printf("| |        /fraction (23 bit)\n");
	printf("| |------| |---------------------|\n");
	(1 << 31) & ux.i ? printf("1 ") : printf("0 ");
	for (int i = 30; i > 22; i--)
		(1 << i) & ux.i ? printf("1") : printf("0");
	printf(" ");
	for (int i = 22; i >= 0; i--)
		(1 << i) & ux.i ? printf("1") : printf("0");
}

union	ldshape
{
	long double f;
	struct
	{
		uint64_t m;
		uint16_t se;
	} i;
};

void	print_ldbin(long double x)
{
	union ldshape ux = {x};
	int j;
	printf("/sign (1 bit)\n");
	printf("| /exponent (14 bit)\n");
	printf("| |              /integer part (1 bit)\n");
	printf("| |              | /fraction (63 bit)\n");
	printf("| |------------| | |");
	printf("--------------------------------------------------------------|\n");
	(1 << 15) & ux.i.se ? printf("1 ") : printf("0 ");
	for (j = 14; j > 0; j--)
		(1 << j) & ux.i.se ? printf("1") : printf("0");
	(1 << 0) & ux.i.se ? printf(" 1 ") : printf(" 0 ");
	for (j = 63; j >= 0; j--)
		(1 << j) & ux.i.m ? printf("1") : printf("0");
}

int		main(void)
{
	float x = 0.15625;
	float y = 10.0;
	printf("ft_fmod(%.5f, %.1f) = %f\n", x, y, ft_fmod(x, y));
	printf("   fmod(%.5f, %.1f) = %f\n", x, y, fmod(x, y));
	print_fbin(x);
	printf("\n");
	return (0);
}
