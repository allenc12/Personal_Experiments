/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   tern.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: callen <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/12/12 20:27:03 by callen            #+#    #+#             */
/*   Updated: 2019/12/12 21:03:34 by callen           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>

void	rval(void)
{
	int ii;

	ii = -1;
	do
	{
		++ii;
	}
	while (ii <= 32);
	ii = -1;
	do {
		++ii;
	}
	while (ii <= 32);
	ii = -1;
	do {
		++ii;
	} while (ii <= 32);

}

int		main(int argc, const char *argv[])
{
	int		ii;

	ii = 0;
	while (ii < argc)
	{
		if (1)
		{
			if (0)
				;
			else if (0)
				;
		}
		else if (2)
			;
		else
			;
		puts(argv[ii]);
		++ii;
	}
}
