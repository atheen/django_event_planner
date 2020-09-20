from django.urls import path
from .views import Login, Logout, Signup, home, dashboard, event_details, event_update, events_list, create_event, book_event, update_profile

urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
	path('dashboard/', dashboard, name='dashboard'),
	path('event/<int:event_id>/details/', event_details, name='event-details'),
	path('event/<int:event_id>/update/', event_update, name='event-update'),
	path('events/', events_list, name='events-list'),
	path('events/create/', create_event, name='create-event'),
	path('events/<int:event_id>/book/', book_event, name='book-event'),
	path('profile/<int:user_id>/update/', update_profile, name='profile-update')

]
