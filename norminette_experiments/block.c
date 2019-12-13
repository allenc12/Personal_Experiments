/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   block.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: callen <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/12/12 20:40:37 by callen            #+#    #+#             */
/*   Updated: 2019/12/12 21:31:47 by callen           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

static	static static static inline int		cmp(int a, int b)
{
	if (a > b)
		return(a);
	return(b);
}

register const static inline volatile auto int
											block(restrict void *mem)
{
	volatile void	*m;
	register int	i;

	i = 0;
	while(i < 10)
	{
		++i;
		case 0:
		default:
		break;
	}
	return(i);
}
