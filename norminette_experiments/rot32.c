/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rot32.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: callen <callen@student.42.us.org>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/03/03 13:44:28 by callen            #+#    #+#             */
/*   Updated: 2019/03/03 13:44:43 by callen           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

uint32_t	rotl32(uint32_t value, unsigned int count)
{
	const unsigned int mask = 8 * sizeof(value) - 1;

	count &= mask;
	return ((value << count) | (value >> (-count & mask)));
}

uint32_t	rotr32(uint32_t value, unsigned int count)
{
	const unsigned int mask = 8 * sizeof(value) - 1;

	count &= mask;
	return ((value >> count) | (value << (-count & mask)));
}
