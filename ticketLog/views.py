from django.shortcuts import render
from django.views import View
from datetime import datetime
from ticketLog.models import Sections, Days, Ticket


# Create your views here.
class Home(View):
    def get(self, request):
        print(Days.choices)
        return render(request, "home.html", {"days": Days.choices, "sections": Sections.choices})

    def post(self, request):
        print(Days.choices)
        # extract form data from POST
        datestr = request.GET["dateTime"]
        # convert datetime-local string to a Python datetime
        datetime.strptime(datestr, '%Y-%m-%dT%H:%M')  # replace the first argument
        # instantiate and save a Ticket
        # to get day of the week, use strftime("%A")
        # like
        # a = datetime.now()
        # print(a.strftime("%A"))
        # also you can use the class Days like a dictionary
        # print(Days["Monday"]) #prints "M", just like print(Days.Monday)
        # render a response, identical to the page rendered by get
        return render(request, "home.html", {"days": Days.choices, "sections": Sections.choices})


class History(View):
    def get(self, request):
        return render(request, "history.html", {"days": Days.choices, "sections": Sections.choices})

    def post(self, request):
        # extract day and section from POST
        tickets = []
        if len(request.GET) != 0:
            day = request.GET["day"]
            section = request.GET["section"]
            # query (filter) for tickets
            results = list(Ticket.objects.filter(dayOfWeek=day, section=section))
            tickets = map(lambda ticket: [f"{ticket.section}", f"{ticket.dateTime:%H:%M}", f"{ticket.dateTime:%d/%m/%yY}"])
        # render a response (with a table of matching tickets)
        return render(request, "history.html", {"days": Days.choices, "sections": Sections.choices, "tickets": tickets})
