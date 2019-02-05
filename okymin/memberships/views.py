from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Membership,UserMembership,Subsciption
# Create your views here.
def get_user_membership(request):
	user_membership_qs = UserMembership.objects.filter(user = request.user)
	if user_membership_qs.exists():
		return user_membership_qs.first()
	return None

def get_user_subscription(request):
	user_subscription_qs = Subsciption.objects.filter(user_membership = get_user_membership(request))
	if user_subscription_qs.exists():
		 user_subscription = user_subscription_qs.first()
		 return user_subscription
	return None

class MembershipSelectView(ListView):
	model = Membership

	def get_context_data(self,*args,**kwargs):
		context = super().get_context_data(**kwargs)
		current_membership = get_user_membership(self.request)
		context['current_membership'] = str(current_membership.membership)
		return context

	def post(self,request,**kwargs):
		user_membership = get_user_membership(request)
		user_subscription = get_user_subscription(request)

		selected_membership_type = request.POST.get('membership_type')

		selected_membership_qs = Membership.objects.filter(membership_type = selected_membership_type)

		print(selected_membership_qs)

		selected_membership  = selected_membership_qs.first()

		print(selected_membership)

		if user_membership.membership == selected_membership:
			if user_subscription is not None:
				messages.info(request, """You already have this membership. Your 
					next payment is due {}""".format('get this value from stripe'))
				return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

		request.session['selected_membership_type'] = selected_membership.membership_type

		return HttpResponseRedirect(reverse('memberships:payment'))

