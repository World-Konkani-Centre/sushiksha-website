import random
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView, FormView

from users.models import Badge, Reward
from .forms import QuestionForm, EssayForm
from .models import Quiz, Category, Progress, Sitting, Question,Essay_Question


class QuizMarkerMixin(object):
    @method_decorator(login_required)
    @method_decorator(permission_required('is_superuser'))
    @method_decorator(permission_required('quiz.view_sittings'))
    def dispatch(self, *args, **kwargs):
        return super(QuizMarkerMixin, self).dispatch(*args, **kwargs)


class SittingFilterTitleMixin(object):
    def get_queryset(self):
        queryset = super(SittingFilterTitleMixin, self).get_queryset()
        quiz_filter = self.request.GET.get('quiz_filter')
        if quiz_filter:
            queryset = queryset.filter(quiz__title__icontains=quiz_filter)

        return queryset

@method_decorator(login_required, name='dispatch')
class QuizListView(ListView):
    model = Quiz

    def get_queryset(self):
        queryset = super(QuizListView, self).get_queryset()
        return queryset.filter(draft=False)

@method_decorator(login_required, name='dispatch')
class QuizDetailView(DetailView):
    model = Quiz
    slug_field = 'url'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

@method_decorator(login_required, name='dispatch')
class CategoriesListView(ListView):
    model = Category

@method_decorator(login_required, name='dispatch')
class ViewQuizListByCategory(ListView):
    model = Quiz
    template_name = 'quiz/view_quiz_category.html'

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category,
            category=self.kwargs['category_name']
        )

        return super(ViewQuizListByCategory, self).\
            dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ViewQuizListByCategory, self)\
            .get_context_data(**kwargs)

        context['category'] = self.category
        return context

    def get_queryset(self):
        queryset = super(ViewQuizListByCategory, self).get_queryset()
        return queryset.filter(category=self.category, draft=False)

@method_decorator(login_required, name='dispatch')
class QuizUserProgressView(TemplateView):
    template_name = 'quiz/progress.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(QuizUserProgressView, self)\
            .dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QuizUserProgressView, self).get_context_data(**kwargs)
        progress, c = Progress.objects.get_or_create(user=self.request.user)
        context['cat_scores'] = progress.list_all_cat_scores
        context['exams'] = progress.show_exams()
        return context

@method_decorator(login_required, name='dispatch')
class QuizMarkingList(QuizMarkerMixin, SittingFilterTitleMixin, ListView):
    model = Sitting

    def get_queryset(self):
        queryset = super(QuizMarkingList, self).get_queryset()\
                                               .filter(complete=True)

        user_filter = self.request.GET.get('user_filter')
        if user_filter:
            queryset = queryset.filter(user__username__icontains=user_filter)

        return queryset

@method_decorator(login_required, name='dispatch')
class QuizMarkingDetail(QuizMarkerMixin, DetailView):
    model = Sitting

    def post(self, request, *args, **kwargs):
        sitting = self.get_object()

        q_to_toggle = request.POST.get('qid', None)
        if q_to_toggle:
            q = Question.objects.get_subclass(id=int(q_to_toggle))
            if int(q_to_toggle) in sitting.get_incorrect_questions:
                sitting.remove_incorrect_question(q)
            else:
                sitting.add_incorrect_question(q)

        return self.get(request)

    def get_context_data(self, **kwargs):
        context = super(QuizMarkingDetail, self).get_context_data(**kwargs)
        context['questions'] =\
            context['sitting'].get_questions(with_answers=True)
        return context

@method_decorator(login_required, name='dispatch')
class QuizTake(FormView):
    form_class = QuestionForm
    template_name = 'quiz/question.html'
    result_template_name = 'quiz/result.html'
    single_complete_template_name = 'quiz/single_complete.html'

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, url=self.kwargs['quiz_name'])
        self.sitting = Sitting.objects.user_sitting(request.user,
                                                        self.quiz)

        if self.sitting is False:
            return render(request, self.single_complete_template_name,context={'quiz':self.quiz})


        return super(QuizTake, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        self.question = self.sitting.get_first_question()
        self.progress = self.sitting.progress()

        if self.question.__class__ is Essay_Question:
            form_class = EssayForm
        else:
            form_class = self.form_class

        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(QuizTake, self).get_form_kwargs()

        return dict(kwargs, question=self.question)

    def form_valid(self, form):
        self.form_valid_user(form)
        if self.sitting.get_first_question() is False:
            return self.final_result_user()

        self.request.POST = {}

        return super(QuizTake, self).get(self, self.request)

    def get_context_data(self, **kwargs):
        context = super(QuizTake, self).get_context_data(**kwargs)
        context['question'] = self.question
        context['quiz'] = self.quiz
        if hasattr(self, 'previous'):
            context['previous'] = self.previous
        if hasattr(self, 'progress'):
            context['progress'] = self.progress
        return context

    def form_valid_user(self, form):
        progress, c = Progress.objects.get_or_create(user=self.request.user)
        guess = form.cleaned_data['answers']
        is_correct = self.question.check_if_correct(guess)
        is_timeout = form.cleaned_data['timeout_count']
        if is_correct is True and not is_timeout:
            self.sitting.add_to_score(1)
            progress.update_score(self.question, 1, 1)
        else:
            self.sitting.add_incorrect_question(self.question)
            progress.update_score(self.question, 0, 1)

        if self.quiz.answers_at_end is not True:
            self.previous = {'previous_answer': guess,
                             'previous_outcome': is_correct,
                             'previous_question': self.question,
                             'answers': self.question.get_answers(),
                             'question_type': {self.question
                                               .__class__.__name__: True}}
        else:
            self.previous = {}

        self.sitting.add_user_answer(self.question, guess)
        self.sitting.remove_first_question()

    def final_result_user(self):
        results = {
            'quiz': self.quiz,
            'score': self.sitting.get_current_score,
            'max_score': self.sitting.get_max_score,
            'percent': self.sitting.get_percent_correct,
            'sitting': self.sitting,
            'previous': self.previous,
        }

        self.sitting.mark_quiz_complete()

        if self.quiz.answers_at_end:
            results['questions'] =\
                self.sitting.get_questions(with_answers=True)
            results['incorrect_questions'] =\
                self.sitting.get_incorrect_questions

        if self.quiz.exam_paper is False:
            self.sitting.delete()

        percent = results['percent']
        describe = "This is a badge for your aptitude practice session, keep learning."
        awarded = 'ADMIN'
        if percent == 100:
            badge_obj = get_object_or_404(Badge,id=129)
            Reward.objects.create(user=get_object_or_404(User, id=int(self.request.user.id)), description=describe,
                                  awarded_by=awarded, badges=badge_obj)
            messages.success(self.request,
                             f'You have successfully completed the quiz and you are awarded with {badge_obj.title} badge')
        elif percent >= 80:
            badge_obj = get_object_or_404(Badge,id=130)
            Reward.objects.create(user=get_object_or_404(User, id=int(self.request.user.id)), description=describe,
                                  awarded_by=awarded, badges=badge_obj)
            messages.success(self.request,
                             f'You have successfully completed the quiz and you are awarded with {badge_obj.title} badge')
        elif percent >= 50:
            badge_obj = get_object_or_404(Badge,id=131)
            Reward.objects.create(user=get_object_or_404(User, id=int(self.request.user.id)), description=describe,
                                  awarded_by=awarded, badges=badge_obj)
            messages.success(self.request, f'You have successfully completed the quiz and you are awarded with {badge_obj.title} badge')
        else:
            messages.warning(self.request,
                             f'Keep learning and score higher percentage to win a badge')
        return render(self.request, self.result_template_name, results)
