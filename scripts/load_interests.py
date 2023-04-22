from users.models import Interest

def run():
	Interest.objects.all().delete()
    # Define your initial data here
	interests = [
		'Sport',
		'Music',
		'Food',
		'Travel',
		'Technology',
	]
	# Create Interest objects and save them to the database
	for interest in interests:
		interest_obj = Interest.objects.create(name=interest)
		interest_obj.save()
	print('Successfully loaded initial data for the Interest model.')