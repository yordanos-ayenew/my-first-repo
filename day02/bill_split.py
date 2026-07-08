bill=2000
people=5
names=["Almaz","Kebede","Abebe","Selam","Blen"]
def split_bill(bill,people,tip_rate=0.1):
    total=bill+(bill*tip_rate)
    per_person=total/people
    return per_person
price=split_bill(bill,people,tip_rate=0.1)
for person in names:
    print(person," pays ",price," ETB")