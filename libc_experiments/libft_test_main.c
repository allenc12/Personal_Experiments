/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   libft_test_main.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: callen <callen@student.42.us.org>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/01/23 12:36:37 by callen            #+#    #+#             */
/*   Updated: 2019/02/17 20:00:33 by callen           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
#include <errno.h>

int		main(int ac, char **av)
{
	char *s1;
	if (ac == 2)
		s1 = av[1];
	else
		s1 = "bobalafulaaaaaaaaaaa";
	printf("ft_strlen(s1) = %zu\n", ft_strlen(s1));
	printf("   strlen(s1) = %zu\n", strlen(s1));
	return (0);
}
