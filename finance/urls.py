from django.urls import path
from . import views

urlpatterns = [
    path('set-budget/', views.set_budget, name='set_budget'),
    path('set-goal/', views.set_goal, name='set_goal'),
    path('budgets/', views.budget_list, name='budget_list'),
    path('goals/', views.goal_list, name='goal_list'),
    path('edit-budget/<int:budget_id>/', views.edit_budget, name='edit_budget'),
    path('delete-budget/<int:budget_id>/', views.delete_budget, name='delete_budget'),
    path('edit-goal/<int:goal_id>/', views.edit_goal, name='edit_goal'),
    path('delete-goal/<int:goal_id>/', views.delete_goal, name='delete_goal'),
    path('dashboard/', views.dashboard, name='finance_dashboard'),
]