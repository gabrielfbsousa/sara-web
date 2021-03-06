from django.core.management.base import BaseCommand, CommandError
from manager.models import Class
from manager.models import Schedule
from manager.models import Slot
import json

class Command(BaseCommand):

    def reset_slots(self):
        Slot.reset_all()

    def reset_timetabling(self):
        Class.reset_all_schedules()

    def load_json_data(self, file_name):
        with open(file_name) as json_data:
            f_json = json.load(json_data)
        return f_json

    def fill_class_assignment(self, data):
        for element in data:
            for slot in element["slots"]:
                saved_class = Class.objects.get(id = element["s_class"])
                saved_slot = Slot.objects.get(day = slot["day"], time_interval = slot["time_interval"], room = slot["room"])
                if saved_slot and saved_class:
                    saved_slot.s_class = saved_class
                    saved_slot.save()

    def fill_timetabling(self, data):
        for element in data:
            for schedule in element["schedules"]:
                saved_class = Class.objects.get(id = element["s_class"])
                if saved_class:
                    saved_schedule = Schedule.objects.get(day = schedule["day"], time_interval = schedule["time_interval"])
                    if saved_schedule:
                        saved_class.schedules.add(saved_schedule)

    def add_arguments(self, parser):
        parser.add_argument('type_request', type=str)
        parser.add_argument('file_name', type=str)

    def handle(self, *args, **options):
        type_request = options['type_request']
        file_name = options['file_name']
        print("processing request...")

        data = self.load_json_data(file_name)
        print("json file was loaded...")

        if type_request == "timetabling":
            self.reset_timetabling()
            print("schedules were deleted...")
            self.fill_timetabling(data)
            print("request \"fill timetabling\" completed successfully...")

        elif type_request == "class_assignment":
            self.reset_slots()
            print("slots were reseted...")
            self.fill_class_assignment(data)
            print("request \"fill  class assignment\" completed successfully...")

        else:
            print("type request invalid!")
