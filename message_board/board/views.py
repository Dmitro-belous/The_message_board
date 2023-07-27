from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .filters import AnnouncementFilter
from .forms import AnnouncementForm, ResponseForm
from .models import Announcement, Response


class AnnouncementDetail(DetailView):
    template_name = 'message.html'
    # Название объекта, в котором будет выбранный пользователем пост
    context_object_name = 'announcement'
    queryset = Announcement.objects.all()

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта
            self.obj = super().get_object(queryset=self.queryset)
            self.res = self.obj.response.all()
            return self.obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = self.obj.author != self.request.user
        context['responses'] = self.res
        return context


class SearchAnnouncement(ListView):
    model = Announcement
    ordering = '-time_add'
    template_name = 'search.html'
    context_object_name = 'announcements'
    paginate_by = 10

    # Переопределяем функцию получения списка постов
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict
        # Сохраняем фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = AnnouncementFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = self.request.user.groups.filter(name='Admins').exists()
        context['superuser'] = self.request.user.is_superuser
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class AnnouncementCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_announcement',)
    raise_exception = True
    # Указываем разработанную форму
    form_class = AnnouncementForm
    # модель постов
    model = Announcement
    # и шаблон, в котором используется форма.
    template_name = 'announcement_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)


# Добавляем представление для изменения поста.
class AnnouncementUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('board.change_announcement',)
    raise_exception = True
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcement_edit.html'


# Представление удаляющее пост.
class AnnouncementDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('board.delete_announcement',)
    raise_exception = True
    model = Announcement
    template_name = 'announcement_delete.html'
    success_url = reverse_lazy('announcement_list')


class PrivateAnnouncements(ListView):
    model = Announcement
    ordering = '-time_add'
    template_name = 'private.html'
    context_object_name = 'announcements'
    paginate_by = 10

    def get_queryset(self):
        queryset = Announcement.objects.filter(author=self.request.user).order_by('-time_add')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ResponseList(ListView):
    model = Response
    ordering = '-time_add'
    template_name = 'responses.html'
    context_object_name = 'responses'
    paginate_by = 10

    def get_queryset(self):
        self.announcement = get_object_or_404(Announcement, id=self.kwargs['pk'])
        queryset = Response.objects.filter(response_post=self.announcement).order_by('-time_add')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = self.request.user.groups.filter(name='Admins').exists()
        context['superuser'] = self.request.user.is_superuser
        context['announcement'] = self.announcement
        return context


class PrivateResponseList(ListView):
    model = Response
    ordering = '-time_add'
    template_name = 'private_responses.html'
    context_object_name = 'responses'
    paginate_by = 10

    def get_queryset(self):
        queryset = Response.objects.filter(response_user=self.request.user).order_by('-time_add')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ResponseDetail(DetailView):
    template_name = 'response_detail.html'
    # Название объекта, в котором будет выбранный пользователем пост
    context_object_name = 'response'
    queryset = Response.objects.all()

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта
        self.obj = super().get_object(queryset=self.queryset)
        self.post = self.obj.response_post
        return self.obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user == self.post.author
        return context


class ResponseCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_response',)
    raise_exception = True
    form_class = ResponseForm
    model = Response
    template_name = 'response_edit.html'

    def form_valid(self, form):
        form.instance.response_user = self.request.user
        announcement = get_object_or_404(Announcement, id=self.kwargs['pk'])
        form.instance.response_post = announcement

        return super().form_valid(form)


class ResponseUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('board.change_response',)
    raise_exception = True
    form_class = ResponseForm
    model = Response
    template_name = 'response_edit.html'


class ResponseDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('board.delete_response',)
    raise_exception = True
    model = Response
    template_name = 'response_delete.html'
    success_url = reverse_lazy('private_resp')


@login_required
@csrf_protect
def accept(request, pk):
    response = Response.objects.get(id=pk)
    announcement = Announcement.objects.get(response=response)
    response.status = True
    response.save()

    Response.objects.filter(response_post=announcement, status=False).delete()

    message = 'You have accepted the response to your announcement'

    return render(
        request, 'accept.html', {
            'announcement': announcement, 'message': message, 'link': f'{settings.SITE_URL}/announcements/private'
        }
    )


@login_required
@csrf_protect
def reject(request, pk):
    response = Response.objects.get(id=pk)
    announcement = Announcement.objects.get(response=response)
    response.delete()

    message = 'You have rejected the response to your announcement'

    return render(
        request, 'reject.html', {
            'announcement': announcement, 'message': message, 'link': f'{settings.SITE_URL}/announcements/private'
        }
    )
