import json
import requests
import datetime
from .serializers import InputSerializer, InputSerializer2, InputSerializer3
import pytz
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

utc = pytz.UTC


def check_shift_a(time):
    if 13 >= time >= 6:
        return True
    return False


def check_shift_b(time):
    if 20 >= time >= 14:
        return True
    return False


def check_shift_c(time):
    if 23 >= time >= 20 or 5 >= time >= 0:
        return True
    return False


def calculate_runtime(runtime):
    minutes = runtime // 60
    seconds = runtime % 60
    hours = minutes // 60
    if hours > 0:
        minutes = minutes % 60
    output_runtime = str(hours) + "h:" + str(minutes) + "m:" + str(seconds) + "s"
    return output_runtime


@csrf_exempt
@api_view(['GET'])
def question_1(request):
    response = requests.get('https://gitlab.com/-/snippets/2094509/raw/master/sample_json_1.json')
    data = response.json()
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%SZ')
    end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%SZ')
    start_date_obj = utc.localize(start_date_obj)
    end_date_obj = utc.localize(end_date_obj)
    shiftA = {'production_A_count': 0, 'production_B_count': 0}
    shiftB = {'production_A_count': 0, 'production_B_count': 0}
    shiftC= {'production_A_count': 0, 'production_B_count': 0}
    for i in data:
        serialized_data = InputSerializer(data=i)
        serialized_data.is_valid()
        proc_data = serialized_data.validated_data
        if end_date_obj >= proc_data['time'] >= start_date_obj:
            if check_shift_a(start_date_obj.hour):
                if check_shift_a(end_date_obj.hour):
                    if end_date_obj.hour >= proc_data['time'].hour >= start_date_obj.hour:
                        if proc_data['production_A']:
                            shiftA['production_A_count'] += 1
                        if proc_data['production_B']:
                            shiftA['production_B_count'] += 1
                if check_shift_b(end_date_obj.hour):
                    if 13 >= proc_data['time'].hour >= start_date_obj.hour:
                        if proc_data['production_A']:
                            shiftA['production_A_count'] += 1
                        if proc_data['production_B']:
                            shiftA['production_B_count'] += 1
                    if end_date_obj.hour >= proc_data['time'].hour >= 14:
                        if proc_data['production_A']:
                            shiftB['production_A_count'] += 1
                        if proc_data['production_B']:
                            shiftB['production_B_count'] += 1
                if check_shift_c(end_date_obj.hour):
                    if 13 >= proc_data['time'].hour >= start_date_obj.hour:
                        if proc_data['production_A']:
                            shiftA['production_A_count'] += 1
                        if proc_data['production_B']:
                            shiftA['production_B_count'] += 1
                    if 19 >= proc_data['time'].hour >= 14:
                        if proc_data['production_A']:
                            shiftB['production_A_count'] += 1
                        if proc_data['production_B']:
                            shiftB['production_B_count'] += 1
                    if end_date_obj.hour >= proc_data['time'].hour >= 20:
                        if proc_data['production_A']:
                            shiftC['production_A_count'] += 1
                        if proc_data['production_B']:
                            shiftC['production_B_count'] += 1

            elif check_shift_b(start_date_obj.hour):
                if check_shift_b(end_date_obj.hour):
                    if end_date_obj.hour >= proc_data['time'].hour >= start_date_obj.hour:
                        if proc_data['production_A']:
                            shiftB['production_A_count'] += 1
                        if proc_data['production_B']:
                            shiftB['production_B_count'] += 1
                if check_shift_c(end_date_obj.hour):
                    if 19 >= proc_data['time'].hour >= start_date_obj.hour:
                        if proc_data['production_A']:
                            shiftB['production_A_count'] += 1
                        if proc_data['production_B']:
                            shiftB['production_B_count'] += 1
                    if end_date_obj.hour >= proc_data['time'].hour >= 20:
                        if proc_data['production_A']:
                            shiftC['production_A_count'] += 1
                        if proc_data['production_B']:
                            shiftC['production_B_count'] += 1
                if check_shift_a(end_date_obj.hour):
                    if 20 >= proc_data['time'].hour >= start_date_obj.hour:
                        if proc_data['production_A']:
                            shiftB['production_A_count'] += 1
                        if proc_data['production_B']:
                            shiftB['production_B_count'] += 1
                    if 23 >= proc_data['time'].hour >= 20 or 5 >= proc_data['time'].hour >= 0:
                        if proc_data['production_A']:
                            shiftC['production_A_count'] += 1
                        if proc_data['production_B']:
                            shiftC['production_B_count'] += 1
                    if end_date_obj.hour >= proc_data['time'].hour >= 6:
                        if proc_data['production_A']:
                            shiftA['production_A_count'] += 1
                        if proc_data['production_B']:
                            shiftA['production_B_count'] += 1
            else:
                if check_shift_c(end_date_obj.hour):
                    if end_date_obj.hour >= proc_data['time'].hour >= start_date_obj.hour:
                        if proc_data['production_A']:
                            shiftC['production_A_count'] += 1
                        if proc_data['production_B']:
                            shiftC['production_B_count'] += 1
                if check_shift_a(end_date_obj.hour):
                    if 11 >= proc_data['time'].hour >= start_date_obj.hour or \
                            5 >= proc_data['time'].hour >= 0:
                        if proc_data['production_A']:
                            shiftC['production_A_count'] += 1
                        if proc_data['production_B']:
                            shiftC['production_B_count'] += 1
                    if end_date_obj.hour >= proc_data['time'].hour >= 6:
                        if proc_data['production_A']:
                            shiftA['production_A_count'] += 1
                        if proc_data['production_B']:
                            shiftA['production_B_count'] += 1
                if check_shift_b(end_date_obj.hour):
                    if 11 >= proc_data['time'].hour >= start_date_obj.hour \
                            or 5 >= proc_data['time'].hour >= 0:
                        if proc_data['production_A']:
                            shiftC['production_A_count'] += 1
                        if proc_data['production_B']:
                            shiftC['production_B_count'] += 1
                    if 13 >= proc_data['time'].hour >= 6:
                        if proc_data['production_A']:
                            shiftA['production_A_count'] += 1
                        if proc_data['production_B']:
                            shiftA['production_B_count'] += 1
                    if end_date_obj.hour >= proc_data['time'].hour >= 14:
                        if proc_data['production_A']:
                            shiftB['production_A_count'] += 1
                        if proc_data['production_B']:
                            shiftB['production_B_count'] += 1
    response_data = {'shiftA': shiftA,
                     'shiftB': shiftB,
                     'shiftC': shiftC}
    return HttpResponse(json.dumps(response_data), content_type='application/json')


@csrf_exempt
@api_view(['GET'])
def question_2(request):
    response = requests.get('https://gitlab.com/-/snippets/2094509/raw/master/sample_json_2.json')
    data = response.json()
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%SZ')
    end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%SZ')
    start_date_obj = utc.localize(start_date_obj)
    end_date_obj = utc.localize(end_date_obj)
    runtime = 0
    downtime = 0
    for i in data:
        serialized_data = InputSerializer2(data=i)
        serialized_data.is_valid()
        proc_data = serialized_data.validated_data
        if end_date_obj >= proc_data['time'] >= start_date_obj:
            if proc_data['runtime'] > 1021:
                calculated_downtime = proc_data['runtime'] - 1021
                calculated_runtime = 1021
            else:
                calculated_downtime = 0
                calculated_runtime = proc_data['runtime']
            runtime = runtime + calculated_runtime
            downtime += calculated_downtime
    utilization = runtime / (runtime + downtime) * 100
    output_runtime = calculate_runtime(runtime)
    downtime = calculate_runtime(downtime)
    response = {"runtime": output_runtime, "downtime": downtime,
                "utilization": round(utilization, 2)}
    return HttpResponse(json.dumps(response), content_type="application/json")


@csrf_exempt
@api_view(['GET'])
def question_3(request):
    response = requests.get('https://gitlab.com/-/snippets/2094509/raw/master/sample_json_3.json')
    data = response.json()
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%SZ')
    end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%SZ')
    start_date_obj = utc.localize(start_date_obj)
    end_date_obj = utc.localize(end_date_obj)
    belt_data = []
    belts = {}
    for i in data:
        serialized_data = InputSerializer3(data=i)
        serialized_data.is_valid()
        proc_data = serialized_data.validated_data
        belts_id = {}
        id = proc_data['id']
        stripped_id = id.strip('ch')
        stripped_id = int(stripped_id)
        if end_date_obj >= proc_data['time'] >= start_date_obj:
            if proc_data['state']:
                if stripped_id in belts:
                    list_belt = belts[stripped_id]['belt2']
                    list_belt1 = belts[stripped_id]['belt1']
                    list_belt.append(proc_data['belt2'])
                    list_belt1.append(0)
                    belts[stripped_id]['belt2'] = list_belt
                    belts[stripped_id]['belt1'] = list_belt1
                else:
                    belts_id['belt2'] = [proc_data['belt2']]
                    belts_id['belt1'] = [0]
                    belts[stripped_id] = belts_id
            else:
                if stripped_id in belts:
                    list_belt = belts[stripped_id]['belt1']
                    list_belt1 = belts[stripped_id]['belt2']
                    list_belt.append(proc_data['belt1'])
                    list_belt1.append(0)
                    belts[stripped_id]['belt1'] = list_belt
                    belts[stripped_id]['belt2'] = list_belt1
                else:
                    belts_id['belt1'] = [proc_data['belt1']]
                    belts_id['belt2'] = [0]
                    belts[stripped_id] = belts_id
    for i in sorted(belts.keys()):
        belt1 = belts[i]['belt1']
        belt2 = belts[i]['belt2']
        sum_belt1 = 0
        sum_belt2 = 0
        for j in belt1:
            sum_belt1 = sum_belt1 + j
        for k in belt2:
            sum_belt2 = sum_belt2 + k
        average_belt1 = sum_belt1//len(belt1)
        average_belt2 = sum_belt2//len(belt2)
        belt_final_data = {'id': i, 'belt1': average_belt1, 'belt2': average_belt2}
        belt_data.append(belt_final_data)
    return HttpResponse(json.dumps(belt_data), content_type="application/json")
