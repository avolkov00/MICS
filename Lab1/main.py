import csv
from enum import Enum


# Тип наведения: тепловой/радиолокационный
class NAV(Enum):
    TEPL = 1
    RAD = 2


naved_id = 0


# Нахождение в полусфере относительно цели: передняя/задняя
class POLUSPHERE(Enum):
    PEREDN = 1
    ZADN = 2


polusph_id = 1
# Требование наведения за мин. время: 0/1
treb_nav_vrem_id = 2
# Требование к скрытности: 0/1
treb_skritn_id = 3
# Необходимость наведения в зад. полусферу: 0/1
treb_nav_zadn_id = 4
# Предпочтительно наведение в зад. полусферу: 0/1
predp_nav_zadn_id = 5
# Реализация по скорости ?Прямого метода?: 0/1
real_v_pr_id = 6
# Реализация по скорости ?Метода манёвра?: 0/1
real_v_man_id = 7
# Реализация по скорости ?Метода перехвата?: 0/1
real_v_per_id = 8
# Реализация траектории ?Прямого метода?: 0/1
real_tr_pr_id = 9
# Реализация траектории ?Метода манёвра?: 0/1
real_tr_man_id = 10
# Реализация траектории ?Метода перехвата?: 0/1
real_tr_per_id = 11
# Реализация по запасу топлива ?Прямого метода?: 0/1
real_top_pr_id = 12
# Реализация по запасу топлива ?Метода манёвра?: 0/1
real_top_man_id = 13
# Реализация по запасу топлива ?Метода перехвата?: 0/1
real_top_per_id = 14

# class syntax


if __name__ == '__main__':

    with open('data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        rows = []
        for row in reader:
            rows.append(row)
        row = rows[1]

        naved = NAV.RAD
        # Тип наведения: тепловой/радиолокационный
        if row[naved_id] == "тепловой":
            naved = NAV.TEPL
        elif row[naved_id] == "радиолокационный":
            naved = NAV.RAD
        else:
            print("Неопознанный способ наведения\n")
            exit(0)

        polusph = POLUSPHERE.PEREDN
        # Нахождение в полусфере относительно цели: передняя/задняя
        if row[polusph_id] == "передняя":
            polusph = POLUSPHERE.PEREDN
        elif row[polusph_id] == "задняя":
            polusph = POLUSPHERE.ZADN
        else:
            print("Неопознанная полусфера относительно цели\n")
            exit(0)

        treb_nav_vrem = False
        # Требование наведения за мин. время: 0/1
        if row[treb_nav_vrem_id] == "1":
            treb_nav_vrem = True
        elif row[treb_nav_vrem_id] == "0":
            treb_nav_vrem = False
        else:
            print("Неопознанное требование наведения за мин. время\n")
            exit(0)

        treb_skritn = False
        # Требование к скрытности: 0/1
        if row[treb_skritn_id] == "1":
            treb_skritn = True
        elif row[treb_skritn_id] == "0":
            treb_skritn = False
        else:
            print("Неопознанное требование к скрытности\n")
            exit(0)
        treb_skritn_id = 3

        # Необходимость наведения в зад. полусферу: 0/1
        treb_nav_zadn = False
        if row[treb_nav_zadn_id] == "1":
            treb_nav_zadn = True
        elif row[treb_nav_zadn_id] == "0":
            treb_nav_zadn = False
        else:
            print("Неопознанное требование наведения в зад. полусферу\n")
            exit(0)

        # Предпочтительно наведение в зад. полусферу: 0/1
        predp_nav_zadn = False
        if row[predp_nav_zadn_id] == "1":
            predp_nav_zadn = True
        elif row[predp_nav_zadn_id] == "0":
            predp_nav_zadn = False
        else:
            print("Неопознанное предпочтитение наведения в задн. полусферу\n")
            exit(0)

        # Реализация по скорости ?Прямого метода?: 0/1
        real_v_pr = False
        if row[real_v_pr_id] == "1":
            real_v_pr = True
        elif row[real_v_pr_id] == "0":
            real_v_pr = False
        else:
            print("Неопознанная возможность реализации по скорости прямого метода\n")
            exit(0)

        # Реализация по скорости ?Метода манёвра?: 0/1
        real_v_man = False
        if row[real_v_man_id] == "1":
            real_v_man = True
        elif row[real_v_man_id] == "0":
            real_v_man = False
        else:
            print("Неопознанная возможность реализации по скорости Метода манёвра\n")
            exit(0)

        # Реализация по скорости ?Метода перехвата?: 0/1
        real_v_per = False
        if row[real_v_per_id] == "1":
            real_v_per = True
        elif row[real_v_per_id] == "0":
            real_v_per = False
        else:
            print("Неопознанная возможность реализации по скорости Метода перехвата\n")
            exit(0)

        # Реализация траектории ?Прямого метода?: 0/1
        real_tr_pr = False
        if row[real_tr_pr_id] == "1":
            real_tr_pr = True
        elif row[real_tr_pr_id] == "0":
            real_tr_pr = False
        else:
            print("Неопознанная возможность реализации по траектории прямого метода\n")
            exit(0)

        # Реализация траектории ?Метода манёвра?: 0/1
        real_tr_man = False
        if row[real_tr_man_id] == "1":
            real_tr_man = True
        elif row[real_tr_man_id] == "0":
            real_tr_man = False
        else:
            print("Неопознанная возможность реализации по траектории Метода манёвра\n")
            exit(0)

        # Реализация траектории ?Метода перехвата?: 0/1
        real_tr_per = False
        if row[real_tr_per_id] == "1":
            real_tr_per = True
        elif row[real_tr_per_id] == "0":
            real_tr_per = False
        else:
            print("Неопознанная возможность реализации по траектории Метода перехвата\n")
            exit(0)

        # Реализация по запасу топлива ?Прямого метода?: 0/1
        real_top_pr = False
        if row[real_top_pr_id] == "1":
            real_top_pr = True
        elif row[real_top_pr_id] == "0":
            real_top_pr = False
        else:
            print("Неопознанная возможность реализации по запасу топлива прямого метода\n")
            exit(0)

        # Реализация по запасу топлива ?Метода манёвра?: 0/1
        real_top_man = False
        if row[real_top_man_id] == "1":
            real_top_man = True
        elif row[real_top_man_id] == "0":
            real_top_man = False
        else:
            print("Неопознанная возможность реализации по запасу топлива Метода манёвра\n")
            exit(0)

        # Реализация по запасу топлива ?Метода перехвата?: 0/1
        real_top_per = False
        if row[real_top_per_id] == "1":
            real_top_per = True
        elif row[real_top_per_id] == "0":
            real_top_per = False
        else:
            print("Неопознанная возможность реализации по запасу топлива Метода перехвата\n")
            exit(0)
        #############################################################################################
        #############################################################################################
        #############################################################################################
        vozm_pr = True
        vozm_man = True
        vozm_per = True

        if (naved == NAV.RAD) and treb_skritn:
            print("Невозможно выбрать метод наведения из за рад. наведения и треб. к скрытности")
            exit(0)
        if ((naved == NAV.TEPL) or treb_skritn) and (polusph == POLUSPHERE.PEREDN):
            vozm_per = False

        if (not real_top_per) and (not real_v_per) and (not real_tr_per):
            vozm_per = False
        if (not real_top_pr) and (not real_v_pr) and (not real_tr_pr):
            vozm_pr = False
        if (not real_top_man) and (not real_v_man) and (not real_tr_man):
            vozm_man = False
        if predp_nav_zadn and (vozm_man or vozm_pr) and (polusph == POLUSPHERE.PEREDN):
            vozm_per = False
        if treb_nav_zadn and (polusph == POLUSPHERE.PEREDN):
            vozm_per = False
        if not (vozm_man or vozm_pr or vozm_per):
            print("Невозможно выбрать метод наведения")
            exit(0)
        if vozm_per:
            print("Метод наведения - перехват")
            exit(0)
        if vozm_pr:
            print("Метод наведения - прямой")
            exit(0)
        if vozm_man:
            print("Метод наведения - маневра")
            exit(0)
