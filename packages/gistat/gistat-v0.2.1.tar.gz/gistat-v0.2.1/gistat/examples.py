import gistat
import time

if __name__ == "__main__":
    start = time.time()
    with gistat.GiStat(debug=True) as stat:
        stat.load()

        print(stat.get_general_stat())
        print('by country')
        print(stat.get_cases_by_country())
        print('by country full')
        # This operation is very expensive.
        print(stat.get_full_cases_by_country())

    print('Execution time: {:.6}'.format(time.time() - start))
