/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bep.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: callen <callen@student.42.us.org>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/02/08 18:58:37 by callen            #+#    #+#             */
/*   Updated: 2019/02/20 11:48:32 by callen           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "bup.h"

static const uint8_t g_data[4] = {0xde, 0xad, 0xbe, 0xef};
static uint32_t g_gonk = 0x7fffffff;
const uint64_t g_highbits = 0x8080808080808080;

int		ret5(void)
{
	int lbl;

	lbl = 5;
	return (lbl);
}

void	aaaaaaaaaaaaa(int *a, int *b)
{
	*a ^= *b;
	*b ^= *a;
	*a ^= *b;
}

static inline

int		main(void)
{
	int c;

	printf("polipio\n");
	return (0);
}
