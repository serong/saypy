"""
    db_triggers.py
    ~~~~~~~~~~~~~~

    :aciklama:
        Veritabanina veri girisi ve gerekli triggerlar icin

    :yazar: github.com/serong
"""

import sqlite3
import db as saydb


class SayisalDBT(object):

    def __init__(self, week, the_date, numbers):
        self.db_name = "sayisal.db"
        self.weeks(week, the_date, numbers)
        self.update_picked_table(numbers)
        self.update_numbers_weeks_table(week, numbers)
        self.update_numbers_group_table(week, numbers)
        self.update_last_pick_table(week, numbers)

    def weeks(self, week, the_date, numbers):
        """ Veritabanina hafta girer.

            :arguments:
                :param week: haftanin sayisi.
                :type week: int

                :param the_date: haftanin tarihi.
                :type the_date: str (2014-12-31)

                :param numbers: sayilar.
                :type numbers: tuple

            :returns:
                :rtype: bool
        """

        connection = sqlite3.connect(self.db_name)

        q = "INSERT INTO weeks VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        d = (week, the_date, numbers[0], numbers[1], numbers[2], numbers[3], numbers[4], numbers[5])

        try:
            connection.execute(q, d)
            connection.commit()
            return True

        # Haftanin daha once girilmesi ihtimaline karsi.
        except sqlite3.IntegrityError:
            connection.close()
            return False

    def update_picked_table(self, numbers):
        """ Hafta icin verilen sayilarin secilme miktarlarini bir arttirir.

            :arguments:
                :param numbers: sayilar
                :type numbers: tuple
            :returns:
                :rtype: bool
        """

        connection = sqlite3.connect(self.db_name)

        for number in numbers:
            q = "UPDATE numbers_picked SET picked = picked + 1 WHERE number = ?"
            d = (number,)
            connection.execute(q, d)

        connection.commit()
        connection.close()

        return True

    def update_numbers_weeks_table(self, week, numbers):
        """ Verilen hafta icin numbers_weeks tablosunu guncelle.
        """

        connection = sqlite3.connect(self.db_name)

        for number in numbers:
            q = "INSERT INTO numbers_weeks VALUES(NULL, ?, ?)"
            d = (week, number)
            connection.execute(q, d)

        connection.commit()
        connection.close()

        return True

    def update_numbers_group_table(self, week, numbers):
        """ Sayi gruplarini gunceller.

            :arguments:
                :param numbers: sayilar.
                :type numbers: tuple

                :param week: hafta
                :type week: int
        """

        connection = sqlite3.connect(self.db_name)

        # 1, 2, 3
        q = "INSERT INTO numbers_group VALUES(NULL, ?, ?, ?, ?)"
        d = (week, numbers[0], numbers[1], numbers[2])
        connection.execute(q, d)

        # 2, 3, 4
        q = "INSERT INTO numbers_group VALUES(NULL, ?, ?, ?, ?)"
        d = (week, numbers[1], numbers[2], numbers[3])
        connection.execute(q, d)

        # 3, 4, 5
        q = "INSERT INTO numbers_group VALUES(NULL, ?, ?, ?, ?)"
        d = (week, numbers[2], numbers[3], numbers[4])
        connection.execute(q, d)

        # 4, 5, 6
        q = "INSERT INTO numbers_group VALUES(NULL, ?, ?, ?, ?)"
        d = (week, numbers[3], numbers[4], numbers[5])
        connection.execute(q, d)

        connection.commit()
        connection.close()

        return True

    def update_last_pick_table(self, week, numbers):
        """ Cikan sayilar icin numbers_last_pick tablosunu guncelle.
        """

        connection = sqlite3.connect(self.db_name)

        for number in numbers:
            q = "UPDATE numbers_last_pick SET last_pick = ? WHERE number = ?"
            d = (week, number)
            connection.execute(q, d)

        connection.commit()
        connection.close()

        return True


wnine = SayisalDBT(961, "2015-04-11", (2, 3, 8, 15, 16, 48))
