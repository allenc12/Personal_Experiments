/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bep.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: callen <callen@student.42.us.org>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/02/08 18:58:37 by callen            #+#    #+#             */
/*   Updated: 2019/03/03 14:31:48 by callen           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "bup.h"
union u_int32 {
	uint32_t	i;
	struct {
		uint8_t	d[4];
	} b;
};
static union u_int32 g_data;
static const uint32_t g_gonk = 0x7fffffff;
const uint64_t g_highbits = 0x8080808080808080;

int		ret5(void)
{
	int lbl;

	lbl = 5;
	return (lbl);
}

void	swap8(uint8_t *a, uint8_t *b)
{
	*a ^= *b;
	*b ^= *a;
	*a ^= *b;
}

void	swap32(int32_t *a, int32_t *b)
{
	*a ^= *b;
	*b ^= *a;
	*a ^= *b;
}

void	swap64(uint64_t *a, uint64_t *b)
{
	*a ^= *b;
	*b ^= *a;
	*a ^= *b;
}

int		main(void)
{
	int a;
	int b;

	a = 0b1111111011101101;
	b = 0175316;
	g_data.b.d[0] = 0xDe;
	g_data.b.d[1] = 0xAd;
	g_data.b.d[2] = 0xbE;
	g_data.b.d[3] = 0xeF;
	printf("(int) a = 0x%X, (int) b = 0x%X\n", a, b);
	swap32(&a, &b);
	printf("(int) a = 0x%X, (int) b = 0x%X\n", a, b);
	printf("polipio %d\n", ret5());
	fprintf(stdout, "(uint8_t[4]) g_data = {0x%hhX, 0x%hhX, 0x%hhX, 0x%hhX}\n",
			g_data.b.d[0], g_data.b.d[1], g_data.b.d[2], g_data.b.d[3]);
	fprintf(stdout, "(uint32_t) g_data = 0x%X\n", g_data.i);
	swap8(&g_data.b.d[0], &g_data.b.d[1]);
	swap8(&g_data.b.d[2], &g_data.b.d[3]);
	printf("(uint8_t[4]) g_data = {0x%hhX, 0x%hhX, 0x%hhX, 0x%hhX}\n",
			g_data.b.d[0], g_data.b.d[1], g_data.b.d[2], g_data.b.d[3]);
	fprintf(stdout, "(uint32_t) g_data = 0x%X\n", g_data.i);
	fprintf(stdout, "(uint32_t) g_gonk = 0x%X\n", g_gonk);
	fprintf(stdout, "(uint64_t) g_highbits = 0x%llX\n", g_highbits);
	return (0);
}
