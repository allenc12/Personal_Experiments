/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   controlstruct.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: callen <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/12/17 00:17:10 by callen            #+#    #+#             */
/*   Updated: 2019/12/17 00:17:12 by callen           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>

int		main(int argc, const char *argv[])
{
	int		ii;
	int		jj;

	ii = 0;
	while (ii < argc) ++ii;
	if (ii > argc) return (-1);
	else if (ii == 0) return (0);
	else	return (1);
}
