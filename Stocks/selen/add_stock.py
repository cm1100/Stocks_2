list1 =["Reliance Industries","Infosys","Tata consultancy services","Divis Laboratories","Sun Pharmaceutical Industries Limited"
        ,"HDFC Bank Limited","Axis Bank","Tata Motors","Bharti Airtel","Mahindra and mahindra","Adani Ports","Avenue supermarts",
        "State Bank Of India"]


from db_structure.models import Stock


def add_s():
    for l in list1:
        if Stock.objects.filter(name=l.lower()).count()==0:
            obj = Stock(name=l.lower())
            obj.save()
