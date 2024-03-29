from django.urls import path
from .views import *

urlpatterns = [
    path('incidents/', IncidentList.as_view(), name='incident-list'),
    path('incidents/approved/',ApprovedIncidentList.as_view(),name='approved-incident-list'),
    path('incidents/not-approved/',NotApprovedIncidentList.as_view(),name='not-approved-incident-list'),
    path('incidents/<int:pk>/',IncidentDetail.as_view(),name='incident-detail'),
    path('incidents/location_ids',IncidentListByLocations.as_view(),name='incident-list-location-ids'),
    path('types/parent/',TypeList.as_view(),name='type-list'),
    path('types/sub/',SubTypeList.as_view(),name='type-list'),
    path('types/',AllTypesList.as_view(),name='type-list'),
    path('types/<int:pk>/',TypeDetail.as_view(),name='type-detail'),
    path('rmq/',send_message_to_rabbitmq, name='test-rmq'),
    path('incidents/filter/',IncidentListFilter.as_view(),name='incident-filter'),
    path('incidents/nlp/',GroupedIncidentsView.as_view(),name='incident-nlp'),
    path('incidents/analysis/types/',IncidentAnalysisTypesView.as_view(),name='incident-analysis'),
    path('incidents/analysis/months/',IncidentAnalysisMonthsView.as_view(),name='incident-months'),
    path('incidents/analysis/days/',IncidentAnalysisDaysView.as_view(),name='incident-days')

]
