from django.shortcuts import render_to_response,render
from django.http import HttpResponse 
from graphs.models import SaleData
from django.core.urlresolvers import reverse
from django.views.generic import View


# def show_chart(request):
# 	return render_to_response('graphs/chart_form.html')

# def my_data(request):
#     myData = {}
#     myData['apples'] = 7
#     myData['oranges'] = 3
#     myData['bananas'] = 5
#     return render(request,'graphs/chart_form.html',{"myData":myData})

class Audit(View):

	def get(self, request):
		raw_data = SaleData.objects.all()
		result_sale=[]
		result_month = []
		for obj in raw_data:
			result_sale.append(int(obj.sale))
			result_month.append(str(obj.month))


		pie_data = SaleData.objects.all()
		data_1=[]
		for obj in pie_data:
			temp = []
			temp.append(str(obj.month))
			temp.append(int(obj.sale))
			data_1.append(temp)
		dic=dict(data_1)

		day_data =SaleData.objects.all()
		per_day=[]
		for i in day_data:
			per_day.append(int(i.sale))

		return render(request,'graphs/chart_form.html',{'result_sale':result_sale,'result_month':result_month,'dic':dic,'per_day':per_day})

