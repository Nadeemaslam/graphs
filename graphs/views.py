from django.shortcuts import render_to_response,render
from django.http import HttpResponse 
from graphs.models import SaleData
from django.core.urlresolvers import reverse
from django.views.generic import View


def show_chart(request):
	return render_to_response('graphs/chart_form.html')

def my_data(request):
    myData = {}
    myData['apples'] = 7
    myData['oranges'] = 3
    myData['bananas'] = 5
    return render(request,'graphs/chart_form.html',{"myData":myData})

class Audit(View):

	def get(self, request):
		# print dir(request.user)
		raw_data = SaleData.objects.all()
		result_sale=[]
		result_month = []
		for d in raw_data:
			result_sale.append(int(d.sale))
			result_month.append(str(d.month))


		pie_data = SaleData.objects.all()
		data_1=[]
		for d in pie_data:
			temp = []
			temp.append(str(d.month))
			temp.append(int(d.sale))
			data_1.append(temp)


		dic=dict(data_1)

		print pie_data

		day_data =SaleData.objects.all()
		per_day=[]
		for x in day_data:
			per_day.append(int(x.sale))

		



		return render(request,'graphs/chart_form.html',{'result_sale':result_sale,'result_month':result_month,'dic':dic,'per_day':per_day})

