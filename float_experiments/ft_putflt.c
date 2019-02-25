/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putflt.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: callen <callen@student.42.us.org>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/01/21 17:32:42 by callen            #+#    #+#             */
/*   Updated: 2019/01/31 20:00:47 by callen           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <float.h>
#include <math.h>
#include <x86intrin.h>
/*
                                                | | exponent|---| | fraction                                         |-----------|
                                                0 10000001000   | 0000000001000001100010010011011101001011110001101010           |	512.512
0000000000000000000000000000000000000000000000000 100000000001000 1000000000100000110001001001101110100101111000110101000000000000	512.512
|127                                                         64|

/sign bit
|  /--exponent---\
|  |  15 bits    |  /-fraction-(64 bits)-------------------------------------------\
|  |             |  |                                                              |
0  100000000001000  1000000000100000110001001001101110100101111000110101000000000000



0 11111111110 1111111111111111111111111111111111111111111111111111					DBL_MAX
0 111111111111110 1111111111111111111111111111111111111111111111111111111111111111	LDBL_MAX
*/

union	u_flt {
	float		f;
	uint32_t	i;
};

union	u_dbl {
	double		f;
	uint64_t	i;
};

union	u_ldbl {
	long double	f;
	struct {
		uint64_t m;
		uint16_t se;
	} i;
};

void	ft_putc(int c)
{
	write(1, &c, 1);
}

void	ft_putldbl_int(long double nbr)
{
	long double	div;
	int			sub;

	if ((sub = (nbr < 0.0)))
		nbr = -nbr;
	div = 1;
	while (div <= nbr / 10.0)
		div *= 10.0;
	if (sub)
		ft_putc('-');
	while (div >= 1.0)
	{
		ft_putc((long)(nbr / div) + '0');
		while (nbr >= div)
			nbr -= div;
		div /= 10.0;
	}
}

void	ft_putldbl_frac(long double nbr, int prec)
{
	int i;

	i = 1;
	ft_putc('.');
	while (i < prec + 1)
	{
		nbr = (nbr - (uint64_t)nbr) * 10 * (-2 * (nbr < 0) + 1);
		ft_putc((uint64_t)(nbr) + '0');
		i++;
	}
}

void	ft_putldbl(long double nbr, int prec)
{
	ft_putldbl_int(nbr);
	ft_putldbl_frac(nbr, prec);
}

void	ft_putldbl_bin(long double n)
{
	union u_ldbl	x = {.f = n};
	uint64_t i = (1ULL << 63ULL);

	while (i >>= 1)
		((uint64_t)n & i) ? printf("1") : printf("0");
	/* (x.i.se & 0x8000) ? printf("1") : printf("0"); */
	/* printf(" "); */
	/* for (i = 0x8000LLU; i >>= 1;) */
	/* 	(x.i.se & i) ? printf("1") : printf("0"); */
	/* printf(" "); */
	/* for (i = 0x8000000000000000LLU; i >>= 1;) */
	/* 	(x.i.m & i) ? printf("1") : printf("0"); */
	printf("\n");
}

union bep {
	double f;
	struct {
		unsigned int manl :32;
		unsigned int manh :20;
		unsigned int exp :11;
		unsigned int sign :1;
	} bits;
};

union bop {
	double f;
	struct {
		unsigned long m :52;
		unsigned int exp :11;
		unsigned int sign :1;
	} bits;
};

void	ft_putstr(const char *s)
{
	write(1, s, strlen(s));
}

int		main(int ac, char **av)
{
	int prec;
	if (ac >= 2)
		prec = atoi(av[1]);
	else
		prec = 6;
	double f = M_PI;
	union bep gonk = {.f = 23.0};
	union bop bonk = {.f = 23.0};
	ft_putstr("calibft [");
	ft_putldbl(f, prec);
	ft_putstr("]\n");
	ft_putldbl_bin(0.0L);
	// printf("  stdlc [%.*f]\n",prec,f);
	return (0);
}
