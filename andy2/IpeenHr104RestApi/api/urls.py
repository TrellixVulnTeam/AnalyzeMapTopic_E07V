from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^ipeen$', views.ipeen_list, name='ipeen_list'),
    url(r'^hr104$', views.hr104_list, name='hr104_list'),
    url(r'^human$', views.human_count_list, name='human_count_list'),
    url(r'^cost$', views.cost_power_list, name='cost_power_list'),
    url(r'^bus$', views.bus_list, name='bus_list'),
    url(r'^store$', views.store_list, name='store_list'),
    url(r'^watsons$', views.watsons_list, name='watsons_list'),
    url(r'^canSuMe$', views.canSuMe_list, name='canSuMe_list'),
    url(r'^carrefour$', views.carrefour_list, name='carrefour_list'),
    url(r'^pxmart$', views.pxmart_list, name='pxmart_list'),
    url(r'^Tstore$', views.tstore_list, name='Tstore_list'),
    url(r'^dahu$', views.dahu_list, name='dahu_list'),
    url(r'^taiwan$', views.taiwan_list, name='taiwan_list'),
    url(r'^stonetwo$', views.stonetwo_list, name='stonetwo_list'),
    url(r'^hot7$', views.hot7_list, name='hot7_list'),
    url(r'^maBoss$', views.maBoss_list, name='maBoss_list'),
    url(r'^suFood$', views.suFood_list, name='suFood_list'),
    url(r'^ita$', views.ita_list, name='ita_list'),
    url(r'^realprice$', views.realPrice_list, name='realprice_list'),
    url(r'^clinic$', views.clinic_list, name='clinic_list'),
    url(r'^psch$', views.psch_list, name='psch_list'),
    url(r'^MRT$', views.mrt_list, name='MRT_list'),
    url(r'^train$', views.train_list, name='train_list'),
    url(r'^eslite$', views.eslite_list, name='eslite_list'),
    url(r'^info591$', views.info591_list, name='info591_list'),
    url(r'^push$', views.push, name='data_push'),
    url(r'^wow$', views.wow, name='wow_list'),
    url(r'^my591$', views.my591_list, name='my591_list'),
    url(r'^legality$', views.legality, name='legality'),

    url(r'^legalityNet$', views.legalityNet, name='legalityNet'),
    url(r'^map$', views.Tmap, name='map'),
    url(r'^compare$', views.Amap, name='Tmap')
]
