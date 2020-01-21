from rest_framework import generics
from datetime import date, timedelta

from .models import User, Report
from .serializers import ReportSerializer, UserSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ReportListView(generics.ListCreateAPIView):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Report.objects.filter(user=self.request.user)
        else:
            return Report.objects.none()

    def finalize_response(self, request, response, *args, **kwargs):
        total_distance = total_duration = 0
        for d in response.data:
            total_distance += d['distance']
            total_duration += d['duration']
        response.data = {
            'reports': response.data,
            'average_speed': total_distance / total_duration
        }

        return super(ReportListView, self).finalize_response(request, response, *args, **kwargs)

    serializer_class = ReportSerializer


class ReportDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Report.objects.filter(user=self.request.user,
                                         pk=self.kwargs['pk'])
        else:
            return Report.objects.none()

    serializer_class = ReportSerializer


class ReportDateFilterView(ReportListView):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Report.objects.filter(user=self.request.user,
                                         date__range=(self.kwargs['date_first'],
                                                      self.kwargs['date_last']))
        else:
            return Report.objects.none()


class ReportPerWeekView(generics.ListAPIView):
    start_date = date.fromisoformat(f'{date.today().year - 1}-01-01')
    end_date = date.fromisoformat(f'{date.today().year - 1}-12-31')

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Report.objects.filter(user=self.request.user,
                                         date__range=(self.start_date, self.end_date))
        else:
            return Report.objects.none()

    def finalize_response(self, request, response, *args, **kwargs):
        week_list = list()
        week_number = 1
        while self.start_date < self.end_date:
            report_week_dict = get_data_per_week(response.data, self.start_date, self.start_date + timedelta(7))
            report_week_dict['week_number'] = week_number
            week_list.append(report_week_dict)
            week_number += 1
            self.start_date += timedelta(7)
        total_distance = total_duration = 0
        for d in response.data:
            total_distance += d['distance']
            total_duration += d['duration']
        response.data = week_list
        return super(ReportPerWeekView, self).finalize_response(request, response, *args, **kwargs)

    serializer_class = ReportSerializer


def get_data_per_week(data: list, start_date: date, end_date: date):
    return_dict = {
        "count": 0,
        "sum_distance": 0,
        "sum_duration": 0
    }
    for d in data:
        if start_date <= date.fromisoformat(d['date']) < end_date:
            return_dict['count'] += 1
            return_dict['sum_distance'] += d['distance']
            return_dict['sum_duration'] += d['duration']
    return_dict['avg_speed'] = 0 if return_dict['sum_duration'] == 0 else \
        return_dict['sum_distance'] / return_dict['sum_duration']
    return return_dict
