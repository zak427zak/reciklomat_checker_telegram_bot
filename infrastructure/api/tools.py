

def plural_days(n, what):
    if what == 'recipes':
        days = ['рецепт', 'рецепта', 'рецептов']

    if n % 10 == 1 and n % 100 != 11:
        p = 0
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        p = 1
    else:
        p = 2

    return str(n) + ' ' + days[p]