from django.contrib.auth.models import User
from django.db import models
from datetime import date


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today())
    distance = models.SmallIntegerField()
    duration = models.SmallIntegerField()

    def __str__(self):
        return f'{self.user.username}_{self.date}_{self.distance}'

# from random import choices, randrange
# from datetime import date, timedelta
#
# def create_users():
#     start_date = date.fromisoformat('2018-10-12')
#     end_date = date.fromisoformat('2020-02-14')
#     while start_date < end_date:
#         for user in User.objects.all():
#             i_number = randrange(2, 7)
#             dates = [start_date+timedelta(x) for x in range(7)]
#             for i in range(i_number):
#                 distance_r = randrange(5, 70)
#                 duration_r = randrange(1, 7)
#                 date_r = choices(dates)[0]
#                 dates.remove(date_r)
#                 Report.objects.create(user=user,
#                                       date=date_r,
#                                       duration=duration_r,
#                                       distance=distance_r)
#         start_date += timedelta(7)


