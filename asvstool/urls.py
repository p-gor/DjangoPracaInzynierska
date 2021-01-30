from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='tool-home'),
    path('about/', views.about, name='tool-about'),
    path('project/', include([
        path('', views.project, name='tool-project'),
        path('<int:id>', views.details_project, name='tool-details'),
        ])),
    path('new_project/', views.add_project, name='tool-add_project'),
    path('checklist/<int:id>/<int:id_state>', views.checklist, name='tool-checklist'),
    path('rejected/<int:id>/', views.rejected, name='tool-rejected'),
    path('reject_list/<int:id>/<int:id_state>', views.rejectlist, name='tool-rejectlist'),
    path('add_comment_checklist/<int:id_project>/<int:id_requirement>/<int:pk>', views.add_comment,
         name='tool-add-comment-checklist'),
    path('add_comment_rejectlist/<int:id_project>/<int:id_requirement>/<int:pk>', views.add_comment,
         name='tool-add-comment-rejectlist'),
    path('reject/<int:id_project>/<int:id_requirement>', views.reject,
         name='tool-reject'),
    path('restore/<int:id_project>/<int:id_requirement>', views.restore,
         name='tool-restore'),
    path('subsection/<int:pk>', views.subsection, name='tool-subsection'),
    path('tests/<int:pk>', views.tests, name='tool-test'),
]