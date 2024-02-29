.PHONY: install migrate createsuperuser runserver


install:
	pip install -r requirements.txt
 
migrate:
	python manage.py makemigrations app_chat
	python manage.py makemigrations app_comment
	python manage.py makemigrations app_like
	python manage.py makemigrations app_support_service
	python manage.py makemigrations Category
	python manage.py makemigrations notification
	python manage.py makemigrations product
	python manage.py makemigrations user_profiles
	python manage.py migrate
 
createsuperuser:
	python manage.py createsuperuser
 
runserver:
	python manage.py runserver