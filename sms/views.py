import unicodedata
from requests import auth
from sms.forms import SmsRecordFormSms, SmsRecordFormSmsBlok
from django.shortcuts import render
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from telefony.models import Mieszkaniec, Blok
from smsapi.client import SmsApiPlClient
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.auth.models import Group
from datetime import date, datetime
from django.db.models import Q


@login_required(login_url="login")
def dashboard_sms(request):
	"""
	View function for rendering the dashboard for SMS records.

	Args:
		request (HttpRequest): The HTTP request object.

	Returns:
		HttpResponse: Rendered HTML response displaying the dashboard with SMS records.
	"""
	
	sms_group = Group.objects.get(name='sms_group')
	if request.user.groups.filter(name=sms_group).exists():
		# If the user is in the 'sms_group', render the dashboard-sms.html template
		my_records = Mieszkaniec.objects.all()
		p = Paginator(Mieszkaniec.objects.all(), 10)
		page = request.GET.get("page")
		my_record = p.get_page(page)
		return render(request, "dashboard-sms.html", {"records": my_records, "my_record": my_record})
	else:
		# If the user is not in the 'sms_group', redirect to a different page or display an error message
		return render(request, 'error-sms.html',
					  {'message': 'Access denied. You are not authorized to view this page.'})


def dashboard_sms_blok(request):
	"""
	View function for rendering the dashboard for SMS records related to blocks.

	Args:
		request (HttpRequest): The HTTP request object.

	Returns:
		HttpResponse: Rendered HTML response displaying the dashboard with SMS records related to blocks.
	"""
	my_records = Blok.objects.all()
	p = Paginator(Blok.objects.all(), 10)
	page = request.GET.get("page")
	my_record = p.get_page(page)
	
	return render(request, "dashboard-sms-blok.html",
				  {"records": my_records, "my_record": my_record})


def dashboard_sms_kontrahent(request):
	"""
	View function for rendering the dashboard for SMS records related to contractors.

	Args:
		request (HttpRequest): The HTTP request object.

	Returns:
		HttpResponse: Rendered HTML response displaying the dashboard with SMS records related to contractors.
	"""
	if request.method == 'POST':
		selected_record_ids = request.POST.getlist('record_ids')
		selected_records = Mieszkaniec.objects.filter(id__in=selected_record_ids)
		selected_phone_numbers = [record.telefon for record in selected_records]
		# Separating multiple phone numbers
		separated_phone_numbers = []
		for phone_number in selected_phone_numbers:
			separated_phone_numbers.extend(phone_number.split(','))  # Assuming phone numbers are separated by commas
		return render(request, "sms-sms-check.html", {"phone_numbers": separated_phone_numbers})
	
	my_records = Mieszkaniec.objects.filter(zgoda__contains="tak")
	p = Paginator(my_records, 10)
	page = request.GET.get("page")
	my_record = p.get_page(page)
	
	return render(request, "dashboard-sms-kontrahent.html",
				  {"records": my_records, "my_record": my_record})


def select_records_sms(request):
	"""
	View function for selecting SMS records.

	Args:
		request (HttpRequest): The HTTP request object.

	Returns:
		JsonResponse: JSON response containing selected phone numbers.
	"""
	if request.method == "POST" and request.is_ajax():
		record_ids = request.POST.getlist("record_ids[]")
		phone_numbers = []
		for record_id in record_ids:
			record = Mieszkaniec.objects.get(pk=record_id)
			phone_numbers.append(record.telefon)
		return JsonResponse({"phone_numbers": phone_numbers})
	else:
		return JsonResponse({})


def dashboard_sms_lu(request):
	"""
	View function for rendering the dashboard for SMS records related to 'LU'.

	Args:
		request (HttpRequest): The HTTP request object.

	Returns:
		HttpResponse: Rendered HTML response displaying the dashboard with SMS records related to 'LU'.
	"""
	my_records_lu = Mieszkaniec.objects.all().filter(administracja__contains="LU")
	p = Paginator(Mieszkaniec.objects.all().filter(zgoda__contains="tak"), 10)
	page = request.GET.get("page")
	my_record_lu = p.get_page(page)
	
	return render(request, "dashboard-sms-lu.html",
				  {"records": my_records_lu, "my_record": my_record_lu})


@login_required(login_url="login")
def view_record_sms(request, pk):
	"""
	View function for viewing a single SMS record.

	Args:
		request (HttpRequest): The HTTP request object.
		pk (int): The primary key of the SMS record to view.

	Returns:
		HttpResponse: Rendered HTML response displaying the details of the SMS record.
	"""
	all_records = Mieszkaniec.objects.get(id=pk)
	context = {"record": all_records}
	
	return render(request, "sms-view.html", context=context)


@login_required(login_url="login")
def view_record_sms_blok(request, pk):
	"""
	View function for viewing a single SMS record related to a block.

	Args:
		request (HttpRequest): The HTTP request object.
		pk (int): The primary key of the SMS record related to a block to view.

	Returns:
		HttpResponse: Rendered HTML response displaying the details of the SMS record related to a block.
	"""
	my_records_blok = Blok.objects.get(id=pk)
	context = {"my_records_blok": my_records_blok}
	
	return render(request, "sms-view-blok.html", context=context)


@login_required(login_url="login")
def view_record_sms_lu(request, pk):
	"""
	View function for viewing a single SMS record related to 'LU'.

	Args:
		request (HttpRequest): The HTTP request object.
		pk (int): The primary key of the SMS record related to 'LU' to view.

	Returns:
		HttpResponse: Rendered HTML response displaying the details of the SMS record related to 'LU'.
	"""
	all_records = Mieszkaniec.objects.get(id=pk)
	context = {"record": all_records}
	
	return render(request, "sms-view-lu.html", context=context)


@login_required(login_url="login")
def sms_record(request, pk):
	"""
	View function for sending SMS records.

	Args:
		request (HttpRequest): The HTTP request object.
		pk (int): The primary key of the SMS record to send.

	Returns:
		HttpResponse: Rendered HTML response after sending the SMS record.
	"""
	record = Mieszkaniec.objects.get(id=pk)
	form = SmsRecordFormSms(instance=record)
	my_record = Mieszkaniec.objects.get(id=pk)
	
	if request.method == "POST":
		phone = request.POST.get("phone")
		content = request.POST.get("content")
		form = SmsRecordFormSms(request.POST, instance=record)
		to_remov = {"ą": "a", "Ą": "A", "ś": "s", "Ś": "S",
					"ę": "e", "Ę": "E", "Ł": "L", "ł": "l",
					"Ó": "O", "ó": "o",
					"Ń": "N", "ń": "n", "ć": "c", "Ć": "C",
					"Ż": "Z", "Ź": "Z", "ż": "z", "ź": "z",
					'„': "", '”': ""}
		for char in to_remov.keys():
			content = content.replace(char, to_remov[char])
		if request.method == "POST":
			token = "rM5DsJlOvDkbGnYnHAn9f9GmpphT0ovOywqPaiLL"
			client = SmsApiPlClient(access_token=token)
			send_results = client.sms.send(to=phone,
										   message=content,
										   from_="SMBUDOWLANI")
			my_records = Mieszkaniec.objects.all()
			p = Paginator(Mieszkaniec.objects.all(), 10)
			page = request.GET.get("page")
			my_record = p.get_page(page)
			
			now = datetime.now()
			today = str(date.today())
			hour = now.strftime("%H:%M:%S")
			user = auth.get_user(request)
			file = open("..//save/sms/sms_kontrahent.txt", "a+")
			file.write("Odbiorca = " + phone + "\n" +
					   "Tresc = " + content + "\n" +
					   "Data:" + today + "\n" +
					   "Wyslal = " + str(user) +
					   "\n" + "Godzina: " + hour + "\n" + "-----------" + "\n")
			file.close
			
			return render(request,
						  "dashboard-sms.html",
						  {"form": form,
						   "record": record, "my_record": my_record})
	
	context = {"form": form, "record": record, "my_record": my_record}
	return render(request, "sms-sms.html", context=context)


@login_required(login_url="login")
def sms_record_blok(request, pk):
	"""
	View function for sending SMS records related to a block.

	Args:
		request (HttpRequest): The HTTP request object.
		pk (int): The primary key of the SMS record related to a block to send.

	Returns:
		HttpResponse: Rendered HTML response after sending the SMS record related to a block.
	"""
	record = Blok.objects.get(id=pk)
	form = SmsRecordFormSms(instance=record)
	my_record = Blok.objects.get(id=pk)
	telefony_queryset = Mieszkaniec.objects.filter(zgoda='tak').filter(
		symbol_budynku=my_record.indeks_blok).values_list('telefon', flat=True)
	telefony_str = ', '.join(map(str, telefony_queryset))
	
	if request.method == "POST":
		phone = request.POST.get("phone")
		content = request.POST.get("content")
		form = SmsRecordFormSms(request.POST, instance=record)
		to_remov = {"ą": "a", "Ą": "A", "ś": "s", "Ś": "S",
					"ę": "e", "Ę": "E", "Ł": "L", "ł": "l",
					"Ó": "O", "ó": "o",
					"Ń": "N", "ń": "n", "ć": "c", "Ć": "C",
					"Ż": "Z", "Ź": "Z", "ż": "z", "ź": "z",
					'„': "", '”': ""}
		for char in to_remov.keys():
			content = content.replace(char, to_remov[char])
		if request.method == "POST":
			token = "rM5DsJlOvDkbGnYnHAn9f9GmpphT0ovOywqPaiLL"
			client = SmsApiPlClient(access_token=token)
			send_results = client.sms.send(to=phone,
										   message=content,
										   from_="SMBUDOWLANI")
			my_records = Mieszkaniec.objects.all()
			p = Paginator(Mieszkaniec.objects.all(), 10)
			page = request.GET.get("page")
			my_record = p.get_page(page)
			
			now = datetime.now()
			today = str(date.today())
			hour = now.strftime("%H:%M:%S")
			user = auth.get_user(request)
			file = open("..//save/sms/sms_blok.txt", "a+")
			file.write("Odbiorca = " + phone + "\n" +
					   "Tresc = " + content + "\n" +
					   "Data:" + today + "\n" +
					   "Wyslal = " + str(user) +
					   "\n" + "Godzina: " + hour + "\n" + "-----------" + "\n")
			file.close
			
			return render(request,
						  "dashboard-sms.html",
						  {"form": form,
						   "record": record, "my_record": my_record, "telefony_str": telefony_str})
	
	context = {"form": form, "record": record, "my_record": my_record, "telefony_str": telefony_str}
	return render(request, "sms-sms-blok.html", context=context)


@login_required(login_url="login")
def sms_record_lu(request):
	"""
	View function for sending SMS records related to 'LU'.

	Args:
		request (HttpRequest): The HTTP request object.

	Returns:
		HttpResponse: Rendered HTML response after sending the SMS record related to 'LU'.
	"""
	record_lu = Mieszkaniec.objects.all()
	form = SmsRecordFormSms(instance=record_lu)
	my_record_lu = Mieszkaniec.objects.all().filter(zgoda__contains="tak") | Mieszkaniec.objects.all().filter(
		administracja__contains="LU")
	telefony_queryset = Mieszkaniec.objects.filter(zgoda='tak').filter(
		symbol_budynku=my_record_lu.administracja).values_list('telefon', flat=True)
	telefony_str = ', '.join(map(str, telefony_queryset))
	
	if request.method == "POST":
		phone = request.POST.get("phone")
		content = request.POST.get("content")
		form = SmsRecordFormSms(request.POST, instance=record_lu)
		to_remov = {"ą": "a", "Ą": "A", "ś": "s", "Ś": "S",
					"ę": "e", "Ę": "E", "Ł": "L", "ł": "l",
					"Ó": "O", "ó": "o",
					"Ń": "N", "ń": "n", "ć": "c", "Ć": "C",
					"Ż": "Z", "Ź": "Z", "ż": "z", "ź": "z",
					'„': "", '”': ""}
		for char in to_remov.keys():
			content = content.replace(char, to_remov[char])
		if request.method == "POST":
			token = "rM5DsJlOvDkbGnYnHAn9f9GmpphT0ovOywqPaiLL"
			client = SmsApiPlClient(access_token=token)
			send_results = client.sms.send(to=phone,
										   message=content,
										   from_="SMBUDOWLANI")
			my_records = Mieszkaniec.objects.all()
			p = Paginator(Mieszkaniec.objects.all(), 10)
			page = request.GET.get("page")
			my_record = p.get_page(page)
			
			now = datetime.now()
			today = str(date.today())
			hour = now.strftime("%H:%M:%S")
			user = auth.get_user(request)
			file = open("..//save/sms/sms_blok.txt", "a+")
			file.write("Odbiorca = " + phone + "\n" +
					   "Tresc = " + content + "\n" +
					   "Data:" + today + "\n" +
					   "Wyslal = " + str(user) +
					   "\n" + "Godzina: " + hour + "\n" + "-----------" + "\n")
			file.close
			
			return render(request,
						  "dashboard-sms.html",
						  {"form": form,
						   "record_lu": record_lu, "my_record": my_record, "telefony_str": telefony_str})
	
	context = {"form": form, "record_lu": record_lu, "my_record_lu": my_record_lu, "telefony_str": telefony_str}
	return render(request, "sms-sms-lu.html", context=context)


@login_required(login_url="login")
def search(request):
	"""
	View function for searching SMS records.

	Args:
		request (HttpRequest): The HTTP request object.

	Returns:
		HttpResponse: Rendered HTML response displaying the search results for SMS records.
	"""
	if request.method == "POST":
		searched = request.POST["searched"]
		my_records = Mieszkaniec.objects.filter(nazwa__contains=searched).filter(
			zgoda__contains="tak") | Mieszkaniec.objects.filter(
			indeks__contains=searched).filter(zgoda__contains="tak") | Mieszkaniec.objects.filter(
			adres__contains=searched).filter(zgoda__contains="tak") | Mieszkaniec.objects.filter(
			telefon__contains=searched).filter(zgoda__contains="tak")
		return render(request, "sms-search.html",
					  {"searched": searched, "my_records": my_records})
	else:
		return render(request, "sms-search.html", {})


@login_required(login_url="login")
def search_kontrahent(request):
	"""
	View function for searching SMS records related to contractors.

	Args:
		request (HttpRequest): The HTTP request object.

	Returns:
		HttpResponse: Rendered HTML response displaying the search results for SMS records related to contractors.
	"""
	if request.method == "POST":
		searched = request.POST["searched"]
		my_records = Mieszkaniec.objects.filter(nazwa__contains=searched).filter(
			zgoda__contains="tak") | Mieszkaniec.objects.filter(
			indeks__contains=searched).filter(zgoda__contains="tak") | Mieszkaniec.objects.filter(
			adres__contains=searched).filter(zgoda__contains="tak")
		return render(request, "sms-search-kontrahent.html",
					  {"searched": searched, "my_records": my_records})
	else:
		return render(request, "sms-search-kontrahent.html", {})


def search_blok(request):
	"""
	View function for searching SMS records related to blocks.

	Args:
		request (HttpRequest): The HTTP request object.

	Returns:
		HttpResponse: Rendered HTML response displaying the search results for SMS records related to blocks.
	"""
	if request.method == "POST":
		searched = request.POST.get("searched", "").strip()
		searched_upper = searched.upper()
		my_records = Blok.objects.filter(
			adres_blok__icontains=searched_upper
		) | Blok.objects.filter(
			indeks_blok__icontains=searched_upper
		)
		
		return render(request, "sms-search-blok.html",
					  {"searched": searched, "my_records": my_records})
	else:
		return render(request, "sms-search-blok.html", {})


@login_required(login_url="login")
def dashboard_szablony(request):
	"""
	View function for rendering the dashboard for SMS templates.

	Args:
		request (HttpRequest): The HTTP request object.

	Returns:
		HttpResponse: Rendered HTML response displaying the dashboard with SMS templates.
	"""
	return render(request, "dashboard_szablony.html")


@login_required(login_url="login")
def sms_test(request):
	"""
	View function for testing SMS functionality.

	Args:
		request (HttpRequest): The HTTP request object.

	Returns:
		HttpResponse: Rendered HTML response after testing the SMS functionality.
	"""
	record = Mieszkaniec.objects.all()
	form = SmsRecordFormSms()
	my_record = Mieszkaniec.objects.all()
	
	if request.method == "POST":
		phone = request.POST.get("phone")
		content = request.POST.get("content")
		form = SmsRecordFormSms(request.POST)
		to_remov = {"ą": "a", "Ą": "A", "ś": "s", "Ś": "S",
					"ę": "e", "Ę": "E", "Ł": "L", "ł": "l",
					"Ó": "O", "ó": "o",
					"Ń": "N", "ń": "n", "ć": "c", "Ć": "C",
					"Ż": "Z", "Ź": "Z", "ż": "z", "ź": "z",
					'„': "", '”': ""}
		for char in to_remov.keys():
			content = content.replace(char, to_remov[char])
		if request.method == "POST":
			token = "rM5DsJlOvDkbGnYnHAn9f9GmpphT0ovOywqPaiLL"
			client = SmsApiPlClient(access_token=token)
			send_results = client.sms.send(to=phone,
										   message=content,
										   from_="SMBUDOWLANI")
			my_records = Mieszkaniec.objects.all()
			
			# now = datetime.now()
			# today = str(date.today())
			# hour = now.strftime("%H:%M:%S")
			# user = auth.get_user(request)
			# file = open("/save/sms/sms_blok.txt", "a+")
			# file.write("Odbiorca = " + phone + "\n" +
			#            "Tresc = " + content + "\n" +
			#            "Data:" + today + "\n" +
			#            "Wyslal = " + str(user) +
			#            "\n" + "Godzina: " + hour + "\n" + "-----------" + "\n")
			# file.close
			
			return render(request,
						  "dashboard-sms.html",
						  {"form": form,
						   "record": record, "my_record": my_record})
	
	context = {"form": form, "record": record, "my_record": my_record}
	return render(request, "sms-sms.html", context=context)


