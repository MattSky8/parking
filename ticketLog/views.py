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
        datestr = request.POST["dateTime"]
        if len(datestr) > 0:
            # convert datetime-local string to a Python datetime
            dt = datetime.strptime(datestr, '%Y-%m-%dT%H:%M')  # replace the first argument
            ticket = Ticket()
            ticket.dateTime = dt
            ticket.dayOfWeek = dt.strftime('%A')
            ticket.section = request.POST["section"]
            ticket.save()
        return render(request, "home.html", {"days": Days.choices, "sections": Sections.choices})


class History(View):
    def get(self, request):
        return render(request, "history.html", {"days": Days.choices, "sections": Sections.choices})

    def post(self, request):
        # extract day and section from POST
        tickets = []
        if len(request.POST) != 0:
            day = request.POST["day"]
            section = request.POST["section"]
            # query (filter) for tickets
            results = list(Ticket.objects.filter(dayOfWeek=day, section=section))
            tickets = list(map(lambda ticket:
                          [f"{ticket.section}", f"{ticket.dateTime:%H:%M}", f"{ticket.dateTime:%d/%m/%yY}"],
                          results))
        # render a response (with a table of matching tickets)
        return render(request, "history.html", {"days": Days.choices, "sections": Sections.choices, "tickets": tickets})
