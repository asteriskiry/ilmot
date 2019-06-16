# Automatic seat arrangement system for event signup.
# Original development by Roosa Virta & Daniel Sundholm
# Additional development and integration: Juhani Vähä-Mäkilä

import random
from numpy import reshape
from datetime import datetime

# Kohta kertoo missä ollaan lajittelemattomien listalla
index = 0


def istumaan(participant, table=None, participants=None):
    global index
    n = len(participants)

    if participant:
        if participant.gender == "woman" and participant in participants:

            if index % 2 != 0:
                temp = index
                while temp < n:
                    if table[temp] is None:
                        table[temp] = participant
                        break
                    temp += 2

            elif index + 1 < round(n):
                temp = index + 1
                while temp < n:
                    if table[temp] is None:
                        table[temp] = participant
                        break
                    temp += 2

            else:
                if index + 1 >= n:
                    index = 0

                if table[index] is None:
                    table[index] = participant

                else:
                    for i in range(n):
                        if table[i] is None:
                            table[i] = participant
                            break
            if index + 1 >= n:
                index = 0

            else:
                index += 1

            participants[participants.index(participant)] = None

        elif participant.gender == "man" and participant in participants:
            if index % 2 != 1:
                temp = index
                while temp < n:
                    if table[temp] is None:
                        table[temp] = participant
                        break
                    temp += 2

            elif index + 1 < n:
                temp = index + 1
                while temp < n:
                    if table[temp] is None:
                        table[temp] = participant
                        break
                    temp += 2

            else:
                if index + 1 >= n:
                    index = 0

                if table[index] is None:
                    table[index] = participant

                else:
                    for i in range(n):
                        if table[i] is None:
                            table[i] = participant
                            break
            if index + 1 >= n:
                index = 0

            else:
                index += 1

            participants[participants.index(participant)] = None

        else:
            if participant in participants:
                for i in range(n):
                    if table[i] is None:
                        table[i] = participant
                        break
                participants[participants.index(participant)] = None


def poytaseurueistumaan(participant):
    if participant:
        friends = participant.plaseeraus.split(",")
        if friends:
            for person in friends:
                istumaan(person)


def vaihda(table):
    for i in range(len(table)):
        if i % 2 == 0 and i % 4 != 0:
            temp = table[i]
            table[i] = table[i + 1]
            table[i + 1] = temp


def plaseeraus(participants, table):
    paikka = 0
    i = 0
    while paikka < len(participants):
        istumaan(participants[paikka], None, participants)
        while i < len(table) and table[i]:
            poytaseurueistumaan(table[i])
            i += 1
        paikka += 1
    vaihda(table)
    if None in table:
        table.remove(None)
    tarkista = list(participants)
    for i in range(len(tarkista)):
        if tarkista[i] not in table:
            table.append(tarkista[i])
    return table


def matriisi(lista):
    from omat.helpers import genNullParticipant
    shape = (round(len(lista) / 2), 2)
    if len(lista) % 2 != 0:
        tyhja = genNullParticipant()
        lista.append(tyhja)
    lista = reshape(lista, shape)
    return lista


def excel(food, drink, poytienmaara, uusipoyta, event=None):
    import xlsxwriter
    # Koodi exceliin
    today = datetime.today().date()
    filename = 'Plaseeraus_'+str(event.name).replace(' ', '_')+'_'+today.isoformat()+'.xlsx'
    matrix = matriisi(uusipoyta)
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet('Plaseeraus '+str(event.name))
    erow = 1
    ecol = 0
    row = 0
    col = 0
    rivit = round(len(uusipoyta) / 2)
    poytaosallistujat = int(len(uusipoyta)/int(poytienmaara))
    istutettu = 0
    poytanro = 1

    if not food and not drink:
        worksheet.write(erow - 1, ecol, 'Poytänro ' + str(poytanro))
        while row < rivit:
            if istutettu == poytaosallistujat:
                istutettu = 0
                erow = 1
                ecol += 3
                poytanro += 1
                worksheet.write(erow - 1, ecol, 'Poytänro ' + str(poytanro))
            worksheet.write(erow, ecol, matrix[row][col].name)
            istutettu += 1
            worksheet.write(erow, ecol + 1, matrix[row][col + 1].name)
            istutettu += 1
            row += 1
            erow += 1

    elif not food and drink:
        worksheet.write(erow - 1, ecol, 'Poytänro ' + str(poytanro))
        while row < rivit:
            if istutettu == poytaosallistujat:
                istutettu = 0
                erow = 1
                ecol += 3
                poytanro += 1
                worksheet.write(erow - 1, ecol, 'Poytänro ' + str(poytanro))
            worksheet.write(erow, ecol, matrix[row][col].name + ', ' + matrix[row][col].holiton)
            istutettu += 1
            worksheet.write(erow, ecol + 1, matrix[row][col + 1].name + ', ' + matrix[row][col + 1].holiton)
            istutettu += 1
            row += 1
            erow += 1

    elif food and not drink:
        worksheet.write(erow - 1, ecol, 'Poytänro ' + str(poytanro))
        while row < rivit:
            if istutettu == poytaosallistujat:
                istutettu = 0
                erow = 1
                ecol += 3
                poytanro += 1
                worksheet.write(erow - 1, ecol, 'Poytänro ' + str(poytanro))
            worksheet.write(erow, ecol, matrix[row][col].name + ', ' + matrix[row][col].lihaton)
            istutettu += 1
            worksheet.write(erow, ecol + 1, matrix[row][col + 1].name + ', ' + matrix[row][col + 1].lihaton)
            istutettu += 1
            row += 1
            erow += 1

    elif food and drink:
        worksheet.write(erow - 1, ecol, 'Poytänro ' + str(poytanro))
        while row < rivit:
            if istutettu == poytaosallistujat:
                istutettu = 0
                erow = 1
                ecol += 3
                poytanro += 1
                worksheet.write(erow - 1, ecol, 'Poytänro ' + str(poytanro))
            worksheet.write(erow, ecol,
                            matrix[row][col].name + ', ' + matrix[row][col].holiton + ', ' + matrix[row][col].lihaton)
            istutettu += 1
            worksheet.write(erow, ecol + 1,
                            matrix[row][col + 1].name + ', ' + matrix[row][col + 1].holiton + ', ' + matrix[row][
                                col + 1].lihaton)
            istutettu += 1
            row += 1
            erow += 1

    workbook.close()
    return filename


# Entry point to the seating generator
def makeSeating(event, participants, numOfTables):
    random.shuffle(participants)
    table = [None] * len(participants)
    table = plaseeraus(participants, table)
    filename = excel(True, True, numOfTables, table, event)
    return filename
