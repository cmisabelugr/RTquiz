from control.models import *
u1 = User.objects.first()
u2 = User.objects.all()[1]
g = Game.objects.first()
q = Question.objects.first()
a1 = Answer_option.objects.all()[0]
a2 = Answer_option.objects.all()[1]
v1 = Vote()
v1.user = u1
v1.answer_option = a1
