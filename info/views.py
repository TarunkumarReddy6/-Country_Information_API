from django.shortcuts import render
from django.http import HttpResponse
from info.models import *
import smtplib
import requests
# Create your views here.
def university_info(req):
	result1 = requests.get('http://universities.hipolabs.com/search?country')
	list1=result1.json()
	country_list = []
	name_list = []
	for i in list1:
		country_list.append(i['country'])
	for j in list1:
		name_list.append(j['name'])
	if(req.GET.get('name')):
		name = req.GET.get('name')
		if(name in country_list):
			result = requests.get('http://universities.hipolabs.com/search?country='+name)
			return render(req,'universities_info.html',{'obj1':result.json()})
		else:
			return render(req,'countery.html',{'msg':'Enter correct country name'})
	else:
		return render(req,'countery.html')


def count_universities(name):
    count = 0
    for i in list1:
        if(i['country']==name):
            count+=1
    return count

#result1 = requests.get('http://universities.hipolabs.com/search?country')
#list1=result1.json()
#country_list = list(set([i['country'] for i in list1]))
#uni_count = dict()
#for j in country_list:
#	uni_count[j]=count_universities(j)

def visvalization(req):
	if(req.GET.get('name')):
		list_of_con = req.GET.get('name')
		list_of_con_split = list_of_con.split(',')
		list_of_uni = list()
		for i in list_of_con_split:
			list_of_uni.append(count_universities(i))
		print(list_of_uni)
		print(list_of_con_split)
		return render(req,"visvalize.html",{'obj1':list_of_con_split, 'obj2':list_of_uni})
	else:
		return render(req,"visvalize.html",{'obj':"Enter Correct name's"})

def Info(req):
	values1 = requests.get('https://restcountries.com/v3.1/all')
	all_list = values1.json()
	name_con = []
	for i in all_list:
		name_con.append(i['name']['common'])
	#print('---->',name_con)
	if(req.GET.get('country_name')):
		country_name = req.GET.get('country_name')
		if(country_name in name_con):
			result = requests.get('https://restcountries.com/v3.1/name/'+country_name)
			info_of_country = result.json()
			name_of_con = info_of_country[0]['name']['common']
			continents = info_of_country[0]['continents'][0]
			independent = info_of_country[0]['independent']
			status = info_of_country[0]['status']
			#currencies_name = info_of_country[0]['currencies'].keys()
			currencies = list(info_of_country[0]['currencies'].keys())[0]
			capital = info_of_country[0]['capital'][0]
			region = info_of_country[0]['region']
			languages = info_of_country[0]['languages']
			languages = languages.values()
			lan_list = []
			for i in languages:
				lan_list.append(i)
			languages_all =','.join(str(item)for item in lan_list)
			area = info_of_country[0]['area']
			flag = info_of_country[0]['flags']['png']
			pop = info_of_country[0]['population']
			visval_value = visval_bar(pop,name_of_con)
			print(visval_value)
			top_pop_values = []
			top_pop_names = []
			for i in visval_value:
				top_pop_values.append(i[0])
				top_pop_names.append(i[1])
			return render(req,'universities_info.html',{'top_pop_values':top_pop_values,'top_pop_names':top_pop_names,'name_of_con':name_of_con,'continents':continents,'independent':independent,'status':status,'currencies':currencies,'capital':capital,'region':region,'languages':languages_all,'area':area,'flag':flag})
		else:
			return render(req,'countery.html',{'msg':'Enter correct country name'})
	else:
		return render(req,'countery.html')


values1 = requests.get('https://restcountries.com/v3.1/all')
all_list = values1.json()
population_list = []
top_population = []
country_list = []
for i in all_list:
	population_list.append(i['population'])
	country_list.append(i['name']['common'])
top_pop = sorted(zip(population_list,country_list), reverse=True)[:3]

def visval_bar(pop,name):
	#values1 = requests.get('https://restcountries.com/v3.1/all')
	#all_list = values1.json()
	#population_list = []
	#top_population =[]
	#for i in all_list:
	#	population_list.append(i['population'])
	#	country_list.append(i['name']['common'])
	#top_pop = sorted(zip(population_list,country_list), reverse=True)[:3]
	just_info = (pop,name)
	top_pop.append(just_info)
	return top_pop

#top population names	top_names = ['top1','top2','top3',name]

#top population max 	top_population = population_list[0:3]
