/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pass.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: callen <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/11/26 17:35:08 by callen            #+#    #+#             */
/*   Updated: 2019/11/26 17:43:50 by callen           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int		main(int argc, const char *argv[])
{
	const char	*arg = 0;
	int			flag;

	if (argc >= 2)
	{
		if (ft_strequ(argv[1], "-butts"))
			flag = 1;
		else
			flag = 0;
	}
	return (flag);
}