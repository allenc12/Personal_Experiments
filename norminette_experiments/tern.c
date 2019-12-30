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
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <errno.h>

void	rval(int a, int b, int c, int d)
{
	int e;

	errno ? exit(0) : 0;
	stdin ? 0 : exit(0);
	a ? b ? c : d : e;
	a ? b : c ? d : e;
	a ? b
	: c ? d
	: e;
	e = b?c:d;
}

int		main(int argc, const char *argv[])
{
	struct stat st;

	(st.st_dev && !st.st_nlink) ? ft_printf(" ? \" : %s ? \" : \n", argv[0]) :
		ft_putchar('?');
	(st.st_dev && !st.st_nlink && st.st_atimespec.tv_nsec) ?
		ft_printf(" ? \" : %s ? \" : \n", argv[0]) : ft_putchar('?');
	(st.st_dev && !st.st_nlink && st.st_birthtimespec.tv_nsec && st.st_blksize)
		? ft_printf(" ? \" : %s ? \" : \n", argv[0]) : ft_putchar('?');
	return (argc > 1 ? !argc : argc);
}
