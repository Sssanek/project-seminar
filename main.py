import jinja2
from datetime import *
import json
from math import ceil
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

email = 'aalapin_2@miem.hse.ru'
mark = 0
# Даты постерной сессии
dateBegin = datetime.strptime('2021-01-25', '%Y-%m-%d')
dateEnd = datetime.strptime('2021-01-29', '%Y-%m-%d')

git = []
gitAccount = 'Нет'
gitDate = {}

with open('/home/student/rawData/GitStats.json', 'r', encoding='utf-8') as f:
    for line in f:
        git.append(json.loads(line))

commitAmount = 0
for i in git[0]:
    if i['email'] == email:
        gitAccount = 'Да'
        for j in i['projects']:
            for c in j['commits']:
                date = c['committed_date'].split('T')[0]
                gitDate[date] = gitDate.get(date, commitAmount) + 1
                commitAmount += 1

'''
print('моя почта:', email)
print('есть ли у меня аккаунт в gitLab:', gitAccount)
print('Какое у меня количество коммитов:', commitAmount)
'''

jitsiClasses = []
classesAmount = 0
jitsiDate = {}

with open('/home/student/rawData/JitsiClasses.json', 'r', encoding='utf-8') as f:
    for line in f:
        jitsiClasses.append(json.loads(line))

for i in jitsiClasses[0]:
    for j in i['auditoriums']:
        for c in j['classes']:
            if email in c['members']:
                jitsiDate[i['date']] = jitsiDate.get(i['date'], classesAmount) + 1
                classesAmount += 1

'''
print()
print('моя почта:', email)
print('сколько занятий я посетил:', classesAmount)
print('когда я их посетил:')
print(jitsiDate)
'''

jitsiSession = []
jitsiSessionAmount = 0
jitsiSessionDate = {}

with open('/home/student/rawData/JitsiSession.json', encoding='utf-8') as f:
    for line in f:
        jitsiSession.append(json.loads(line))

for i in jitsiSession[0]:
    date = datetime.strptime(i['date'], '%Y-%m-%d')
    if 'project' in i['room'] and i['username'] == email and date >= dateBegin and date <= dateEnd:
        jitsiSessionDate[i['date']] = jitsiSessionDate.get(i['date'], jitsiSessionAmount) + 1
        jitsiSessionAmount += 1

'''
print()
print('сколько я отсмотрел проектов на постерной сессии:', jitsiSessionAmount)
print('когда это было:')
print(jitsiSessionDate)
'''

zulipMessagesAmount = 0
zulipDate = {}
zulip = []
zulipAccount = 'Нет'

with open('/home/student/rawData/ZulipStats.json', encoding='utf-8') as f:
    for line in f:
        zulip.append(json.loads(line))

for i in zulip[0]:
    if i['email'] == email:
        zulipAccount = 'Да'
        for j in i['messages']:
            date = j['timestamp'].split('T')[0]
            zulipDate[date] = zulipDate.get(date, zulipMessagesAmount) + 1
            zulipMessagesAmount += 1
'''
print()
print('есть ли у меня аккаунт в зулипе:', zulipAccount)
print('сколько я сообщений написал:', zulipMessagesAmount)
print('когда я их написал:')
print(zulipDate)
'''

if gitAccount == 'Да':
    mark += 1
if commitAmount:
    mark += 1
if zulipAccount == 'Да':
    mark += 1
if zulipMessagesAmount:
    mark += 1
mark += classesAmount * 0.5
mark += jitsiSessionAmount * 0.5
mark = ceil(mark)

'''
print()
print('моя итоговая оценка:', mark)
'''

template = jinja2.Template('''
<!DOCTYPE html>
<html>
<head>
<title>Title of the document</title>
<meta charset="utf-8">
</head>

<body>
<h1>Аккаунт в gitLab</h1>
    <table border="2">
        <thead>
            <th align="center">Почта</th>
            <th align="center">Есть аккаунт в gitLab</th>
            <th align="center">Количество коммитов</th>
        </thead>
        <tbody>
            <tr>
                <td align="center">{{ email }}</td>
                <td align="center">{{ gitAccount }}</td>
                <td align="center">{{ commitAmount }}</td>
            </tr>
        </tbody>
    </table>
    <br>
    <br>
<h1>Посещение занятий по проектному семинару</h1>
    <table border="2">
        <thead>
            <th align="center">Почта</th>
            <th align="center">	Количество посещений</th>
        </thead>
        <tbody>
            <tr>
                <td align="center">{{ email }}</td>
                <td align="center">{{ classesAmount }}</td>
            </tr>
        </tbody>
    </table>
    <br>
<h1>Посещение постерной сессии</h1>
    <table border="2">
        <thead>
            <th align="center">Почта</th>
            <th align="center">	Количество посещений</th>
        </thead>
        <tbody>
            <tr>
                <td align="center">{{ email }}</td>
                <td align="center">{{ jitsiSessionAmount }}</td>
            </tr>
        </tbody>
    </table>
    <br>
<h1>Аккаунт в zulip</h1>
    <table border="2">
        <thead>
            <th align="center">Почта</th>
            <th align="center">	Есть аккаунт в zulip</th>
            <th align="center">	Количество сообщений</th>
        </thead>
        <tbody>
            <tr>
                <td align="center">{{ email }}</td>
                <td align="center">{{ zulipAccount }}</td>
                <td align="center">{{ zulipMessagesAmount }}</td>
            </tr>
        </tbody>
    </table>
    <br>
    <br>
<h1>Итоговая оценка: {{ mark }}</h1>
</body>
<body>

<h1>комиты в Гитлабе</h1>

<img src="gitlab.png">

</body>
<body>

<h1>посещение занятий</h1>

<img src="classes.png">

</body>
<body>

<h1>сообщения в зулипе</h1>

<img src="zulip.png">

</body>

</html>
''')


# строю коммитов в гите
start = datetime.strptime("2021-01-01", '%Y-%m-%d')
end = datetime.strptime("2021-04-05", '%Y-%m-%d')
date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days)]

for date in date_generated:
    print(date.strftime('%Y-%m-%d'))

sample = dict((k.strftime('%Y-%m-%d'), 0) for k in date_generated)
print(sample)

jit = gitDate

for ch in jit:
    sample[ch] = jit[ch]

h = 0
for ch in sample:
    if sample[ch] > h:
        h = sample[ch]
    else:
        sample[ch] = h

print(sample)

a = list(sample.keys())
b = list(sample.values())
print(a)
print(b)
fig, ax = plt.subplots()
ax.plot(a, b, color='r', linewidth=3)
ax.plot(a, b)
ax.xaxis.set_major_locator(ticker.MultipleLocator(30))
plt.savefig('gitlab.png')

# разбираюсь с посещением занятий
start = datetime.strptime("2021-01-01", '%Y-%m-%d')
end = datetime.strptime("2021-04-05", '%Y-%m-%d')
date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days)]

for date in date_generated:
    print(date.strftime('%Y-%m-%d'))

sample = dict((k.strftime('%Y-%m-%d'), 0) for k in date_generated)
print(sample)

jit = jitsiDate

for ch in jit:
    sample[ch] = jit[ch]

h = 0
for ch in sample:
    if sample[ch] > h:
        h = sample[ch]
    else:
        sample[ch] = h

print(sample)

a = list(sample.keys())
b = list(sample.values())
print(a)
print(b)
fig, ax = plt.subplots()
ax.plot(a, b, color='r', linewidth=3)
ax.plot(a, b)
ax.xaxis.set_major_locator(ticker.MultipleLocator(30))
plt.savefig('classes.png')

# разбираюсь зулипом
start = datetime.strptime("2021-01-01", '%Y-%m-%d')
end = datetime.strptime("2021-04-05", '%Y-%m-%d')
date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days)]

for date in date_generated:
    print(date.strftime('%Y-%m-%d'))

sample = dict((k.strftime('%Y-%m-%d'), 0) for k in date_generated)
print(sample)

jit = zulipDate

for ch in jit:
    sample[ch] = jit[ch]

h = 0
for ch in sample:
    if sample[ch] > h:
        h = sample[ch]
    else:
        sample[ch] = h

print(sample)

a = list(sample.keys())
b = list(sample.values())
print(a)
print(b)
fig, ax = plt.subplots()
ax.plot(a, b, color='r', linewidth=3)
ax.plot(a, b)
ax.xaxis.set_major_locator(ticker.MultipleLocator(30))
plt.savefig('zulip.png')

# выведем все в html
html = template.render(email=email, gitAccount=gitAccount, commitAmount=commitAmount,
                       classesAmount=classesAmount, jitsiSessionAmount=jitsiSessionAmount, zulipAccount=zulipAccount,
                       zulipMessagesAmount=zulipMessagesAmount, mark=mark)

with open("script.html", "w") as f:
    f.write(html)
