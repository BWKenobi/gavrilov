from django import template

register = template.Library()

@register.filter(name='lookup')
def lookup(d, key):
	try:
		t = d[key]
	except:
		return None

	return t


@register.filter(name = 'addstr')
def addstr(arg1, arg2):
	return str(arg1) + str(arg2)
