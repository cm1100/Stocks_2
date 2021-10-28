import datetime

def save_data(data,stock,model):
    dict1 = {}
    i=0
    for d in data:
        if i == 1:
            for m in d.text.split()[:-3]:
                dict1[m] = []

        elif i > 2:
            keys = list(dict1)
            print(keys)
            dim = d.text.split()

            [dict1[keys[k]].append(dim[k]) for k in range(5)]
            date = dim[0].split('-')


            date = datetime.date(int(date[0]), int(date[1]), int(date[2]))

            if model.objects.filter(indice=stock,date=date).count() == 0:

                obj = model(indice=stock, date=date, open_p=float(dim[1]), high_p=float(dim[2]), low_p=float(dim[3]),
                           close_p=float(dim[4]))
                obj.save()
                print("saved")


        i += 1