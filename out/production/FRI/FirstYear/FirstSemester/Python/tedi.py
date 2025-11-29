#
# TMI calculator
#
tm_kg = int(input("Telesna teža: "))
tv_cm = int(input("Telesna višina: "))
tv_m = tv_cm/100
TMI = (tm_kg)/(tv_m**2)
TMI = round(TMI, 2)
print("Tvoj indeks telesne mase je: ", TMI)