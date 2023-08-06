import numpy
def potato(days):
    if days == 0:
        return 'seed'
    elif days=='e':
        return numpy.e
    elif days >0 and days < 8:
        return 'sprout'
    elif days >8 and days < 20 :
        return 'potato'
    else:
        return 'withered crop'



