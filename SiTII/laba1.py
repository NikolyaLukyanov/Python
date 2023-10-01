from statistics import mean

my_departments = """Отдел-1:182,230,204,219,161,218,196,161,228,202,164,189,178,240,205,200,153,191,183,231;Отдел-2:236,
213,222,185,163,207,187,163,167,172,193,168,231,218,248,184,174,237,246,188;Отдел-3:248,194,175,170,215,171,157,248,
165,213,208,184,175,205,236,194,151,156,183,225;Отдел-4:186,230,169,220,166,234,217,243,233,211,207,227,246,164,217,
250,213,152,153,187;Отдел-5:189,237,188,207,173,220,183,186,156,188,220,229,161,165,157,151,172,205,250,
199;Отдел-6:226,170,193,242,233,194,178,181,167,172,174,209,217,177,196,240,226,225,155,224;Отдел-7:228,173,178,235,
165,205,239,247,214,229,220,228,231,246,235,173,207,156,238,151;Отдел-8:190,236,220,150,212,210,190,153,216,188,225,
200,226,162,207,217,170,170,160,206;Отдел-9:184,160,184,238,223,176,237,228,236,195,215,155,223,217,198,162,250,184,
194,236;Отдел-10:218,209,232,183,208,205,152,206,159,213,241,227,196,245,210,244,241,214,200,160"""
my_departments = my_departments.split(';')

for my_department in my_departments:
    data = []
    my_department = ''.join(char for char in my_department if char != "'")
    my_department = my_department.split(':')
    name_department = my_department[0]
    electric_consums = my_department[1]
    electric_consums = electric_consums.split(',')
    electric_consums = [int(item) for item in electric_consums]
    for electric_consum in electric_consums:
        if electric_consum > mean(electric_consums):
            index = electric_consums.index(electric_consum)
            data.append(index + 1)

    print("В отделе", name_department, "высокое потребление в дни: ", str(data).strip('[]'), ". Среднее потребление: ",
          mean(electric_consums))
