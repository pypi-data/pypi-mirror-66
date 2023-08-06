from rest_framework.views import APIView
from rest_framework.response import Response
from .system_info import (
    system_information,
    boot_time,
    cpu_info,
    virtual_memory,
    swap_memory,
    disk_info,
    network_info,
    battery_info,
    temperature_info
)

from .scheduleCron import (
    creating_new_cron_job,
    is_cron_job_present_or_not,
    editing_a_cron_job,
    deleting_a_cron_job,
    deleting_all_cron_jobs
)

class HealthCheckView(APIView):
    def get(self, request):
        Response.status_code = 200
        return Response({
            "status": "success",
            "message": "Server is working fine"
        })


choices = {
    1: "System Information",
    2: "Boot Time",
    3: "Cpu Info",
    4: "Virtual Memory Info",
    5: "Swap Memory",
    6: "Disk Info",
    7: "Network Info"
}


class AvailableSystemMonitoringChoicesView(APIView):
    def get(self, request):
        return Response({
            "choice": choices.values()
        })


class ReturningSystemDataView(APIView):
    def get(self, request):
        choice = request.query_params.get('metric')
        if choice == choices[1]:
            return Response(system_information())
        elif choice == choices[2]:
            return Response(boot_time())
        elif choice == choices[3]:
            return Response(cpu_info())
        elif choice == choices[4]:
            return Response(virtual_memory())
        elif choice == choices[5]:
            return Response(swap_memory())
        elif choice == choices[6]:
            return Response(disk_info())
        elif choice == choices[7]:
            return Response(network_info())
        # elif choice == choices[8]:
        #     return Response(battery_info)
        elif choice == 'All':
            return Response({
                choices[1]: system_information(),
                choices[2]: boot_time(),
                choices[3]: cpu_info(),
                choices[4]: virtual_memory(),
                choices[5]: swap_memory(),
                choices[6]: disk_info(),
                choices[7]: network_info()
            })
        else:
            return Response({
              "status": "error, query parameter incorrect, missing or invalid"  
            })


class SettingCronJobForCurrentUserView(APIView):
    def post(self, request):
        params = request.data
        print(params)
        if is_cron_job_present_or_not(request.data.get('name_of_job')):
            Response.status_code = 409
            return Response({"status": "error", "message": "A job by that name already exists"})
        output = creating_new_cron_job(**params)
        if output:
            Response.status_code = 201
            return Response({"status": "success", "message": "created the cron monitor successfully"})
        else:
            Response.status_code = 400
            return Response({"status": "error", "message": "Unable to create the script, check logs"})


class CheckingIfACronJobIsPresentOrNotView(APIView):
    def post(self, request):
        name_of_the_job = request.data.get('name_of_the_job')
        if is_cron_job_present_or_not(name_of_the_job):
            Response.status_code = 200
            return Response({"status": "success"})
        else:
            Response.status_code = 404
            return Response({"status": "error"})


class EditingACronJobView(APIView):
    def post(self, request):
        if not is_cron_job_present_or_not(request.data.get('name_of_job')):
            Response.status_code = 409
            return Response({"status": "error", "message": "No job exists by this name"})
        params = request.data

        if editing_a_cron_job(**params):
            Response.status_code = 202
            return Response({"status": "success"})
        else:
            Response.status_code = 500
            return Response({"status": "error"})

class DeletingACronJobView(APIView):
    def post(self, request):
        name_of_job = request.data.get('name_of_job')
        if not is_cron_job_present_or_not(name_of_job):
            Response.status_code = 409
            return Response({"status": "error", "message": "No job exists by this name"})
        if deleting_a_cron_job(name_of_job):
            Response.status_code = 204
            return Response({"status": "success"})
        else:
            Response.status_code = 500
            return Response({"status": "error"})
        
class DeletingAllCronJobView(APIView):
    def post(self, request):
        if deleting_all_cron_jobs():
            Response.status_code = 204
            return Response({"status": "success"})
        else:
            Response.status_code = 500
            return Response({"status": "error"})


