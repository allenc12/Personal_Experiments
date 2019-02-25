/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_modf.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: callen <callen@student.42.us.org>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/01/21 10:54:51 by callen            #+#    #+#             */
/*   Updated: 2019/01/21 10:59:01 by callen           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
#define MAXPOW2		4.503599627370496000E+15

double	ft_modf(double val, register double *iptr)
{
	register double	abs;

	if ((abs = (val >= 0.0) ? val : -val) >= MAXPOW2)
		*iptr = value;
	else
	{
		*iptr = abs + MAXPOW2;
		*iptr -= MAXPOW2;
		while (*iptr > abs)
			*iptr -= 1.0;
		if (val < 0.0)
			*iptr = -*iptr;
	}
	return (val - *iptr);
}
