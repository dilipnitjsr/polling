from django.urls import path
from background_task import background
from . import views
from  . import randomvoting

app_name='polls'
urlpatterns=[
	# path('',views.index, name='index'),
	# path('<int:question_id>/',views.detail,name='detail'),
	# path('<int:question_id>/results/',views.results,name='results'),
	# path('<int:question_id>/vote/', views.vote, name='vote'),
	# path('add/',views.newQuestion,name='add'),

	path('',views.IndexView.as_view(), name='index'),
	path('<int:pk>/',views.DetailView.as_view(),name='detail'),
	path('<int:pk>/results/',views.ResultsView.as_view(),name='results'),
	path('<int:question_id>/vote/', views.vote, name='vote'),
	path('add/',views.newQuestion,name='add'),
	path('api/',views.votesApi,name='voteapi'),
]

#@background(schedule=5,)
from threading import Thread 
x=Thread(target=randomvoting.testfunc,args='')
x.start()
