import sqlite3


class DataBaseEditor:
    def __init__(self, counters_list=None):
        self.counters_list = counters_list  # --> [килы, смерти, выстрелы, урон, пройденные игры]

    def update_db(self):
        con = sqlite3.connect("data/bd/player_stats.sqlite")
        cur = con.cursor()

        stats = list(cur.execute('''SELECT * FROM stats''').fetchone())

        for x in range(0, 5):
            stats[x] += self.counters_list[x]

        cur.execute(f'''UPDATE stats SET kills = {stats[0]}, deaths = {stats[1]}, shots = {stats[2]},
         damage = {stats[3]}, completed_games = {stats[4]}''')
        con.commit()
        cur.close()

    def get_stats(self):
        con = sqlite3.connect("data/bd/player_stats.sqlite")
        cur = con.cursor()

        stats = cur.execute('''SELECT * FROM stats''').fetchone()
        con.commit()
        cur.close()

        return stats
