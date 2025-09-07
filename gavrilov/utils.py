from datetime import date

from nominations.models import ArtNomination, VocalNomination

def base_context(request):
	start = False

	dte = date.today()
	dte_deadline = date(2025,10,6)
	register_block = True
	if dte<dte_deadline:
		register_block = False

	if not request.user.is_authenticated:
		start = True

	arts = ArtNomination.objects.all()
	vocals = VocalNomination.objects.all()

	args = {
		'start': start,
		'register_block': register_block,
		'arts': arts,
		'vocals': vocals
	}
	
	return args
