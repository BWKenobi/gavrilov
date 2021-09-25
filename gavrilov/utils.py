from datetime import date

from children.models import Child
from teachers.models import Teacher
from nominations.models import Nomination, SubNomination

def base_context(request):
	start = False
	my_children = None
	my_teachers = None

	dte = date.today()
	dte_deadline = date(2021,10,15)
	register_block = True
	if dte<dte_deadline:
		register_block = False

	if not request.user.is_authenticated:
		start = True
	else:
		my_children = Child.objects.filter(teacher=request.user)
		my_teachers = Teacher.objects.filter(host_accaunt=request.user)

	nominations = Nomination.objects.all()
	subnominations = {}
	for nomination in nominations:
		s = SubNomination.objects.filter(nomination = nomination)
		if s:
			subnominations[nomination.id] = s

	args = {
		'start': start,
		'register_block': register_block,
		'nominations': nominations,
		'subnominations': subnominations,
		'my_children': my_children,
		'my_teachers': my_teachers
	}
	return args
