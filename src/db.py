"""
    db.py
    ~~~~~

    :aciklama:
        Veritabani ile ilgili veri alimi islerini halleder.

    :yazar: github.com/serong
"""

import sqlite3


class SayisalDb(object):

    def __init__(self):
        self.db_name = "sayisal.db"

    def get_latest_week(self, row=False):
        """ En son haftanin sayisini getirir.

            :arguments:
                :param row: Son haftanin sadece hafta sayisindan fazla
                gelmesi istendigi durumda kullanilir.
                :type row: bool

            :returns:
                :rtype: int
        """

        connection = sqlite3.connect(self.db_name)

        q = "SELECT * FROM weeks ORDER BY week DESC LIMIT 1"
        query = connection.execute(q)

        result = query.fetchall()

        connection.close()

        if row:
            return result[0]
        else:
            return result[0][0]

    def get_week(self, week, numbers=False):
        """ Verilen haftayi getirir.

            :arguments:
                :param week: hafta sayisi.
                :type week: int

                :param numbers: Sadece sayilari getir?
                :type numbers: bool

            :returns:
                :rtype: tuple
        """

        connection = sqlite3.connect(self.db_name)

        d = (week, )
        q = "SELECT * FROM weeks WHERE week = ?"

        query = connection.execute(q, d)
        result = query.fetchall()
        connection.close()

        try:
            if numbers:
                return result[0][2:]
            else:
                return result[0]
        except:
            raise ValueError("Hafta veritabaninda bulunamadi.")

    def get_weeks(self, start=None, end=None):
        """ Verilen araliktaki haftalari getirir.

            :NOTE:
                start ve end parametreleri Python'daki list
                slicing ile ayni sekilde calisiyor. :method:get_weeks_offset
                ile farki buradan kaynaklaniyor.

                :method:get_weeks son 10 hafta icin de kullanilabilir.
                    get_weeks(start=-10)

                :method:get_weeks normal kullanim.
                    get_weeks(900, 905)
                    900, 901, 902, 903, 904. haftalari getirir.

            :arguments:
                :param start: Baslangic.
                :type start: int

                :param end: Son.
                :type end: int

            :returns:
                :rtype: list of tuples
        """

        connection = sqlite3.connect(self.db_name)

        q = "SELECT * FROM weeks"

        query = connection.execute(q)
        results = query.fetchall()
        connection.close()

        if start < 0 and end is None:
            return results[start:]
        else:
            return results[start-1:end-1]

    def get_weeks_offset(self, start, length):
        """ Verilen baslangic haftasindan itibaren :param:length kadar hafta getirir.

            :arguments:
                :param start: baslangic
                :param length: uzunluk

                :type start, len: int

            :returns:
                :rtype: list of tuples.
        """
        connection = sqlite3.connect(self.db_name)

        q = "SELECT * FROM weeks WHERE week BETWEEN ? and ?"
        d = (start, start+length-1)

        query = connection.execute(q, d)
        results = query.fetchall()
        connection.close()

        return results

    def get_date(self, week):
        """ Verilen haftanin tarihini getirir.

            :arguments:
                :param week: hafta sayisi.
                :type week: int

            :returns:
                :rtype: date object
        """

        connection = sqlite3.connect(self.db_name)

        # sorgu icin gerekli veriler.
        d = (week, )
        q = "SELECT date FROM weeks WHERE week = ?"

        query = connection.execute(q, d)
        result = query.fetchone()
        connection.close()

        try:
            return result[0]
        except:
            raise ValueError("Hafta veritabaninda bulunamadi.")


# x = SayisalDb()
# print x.get_weeks_offset(900, 5)
