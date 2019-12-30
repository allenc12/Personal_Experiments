/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   butts.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: callen <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/12/17 14:44:09 by callen            #+#    #+#             */
/*   Updated: 2019/12/17 19:54:08 by callen           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stddef.h>
#include <sys/cdefs.h>

#define MACRO "H1\xc9H\xf7\xe1\x04;H\xbb/bin//shRST_RWT^\x0f\x05"

static inline int __attribute__((__always_inline__))
	ret_if(int cond, int retv)
{
	if (cond)
		return (retv);
	return (0);
}

int
	tst_macro(int arg)
{
	RET_IF(arg == 3, 9);
	return (0);
}

int
	tst_inline(int arg)
{
	ret_if(arg == 3, 9);
	return (0);
}

int
	main(void)
{
	int r1;
	int r2;

	r1 = tst_macro(3);
	r2 = tst_inline(3);
	printf("r1(%d) r2(%d)\n", r1, r2);
}
