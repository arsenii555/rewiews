import smtplib
from email.mime.text import MIMEText
import datetime as dt
import pandas as pd
from time import sleep
import test


def send_email(message, getter):
    sender = "arsenij.evdokimov2@gmail.com"
    password = "slgmkjtpgxxgzjjj"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg["SUBJECT"] = "Отзыв о клинике"
        server.sendmail(sender, getter, msg.as_string())

        return "Сообщение успешно отправлено"
    except Exception as _ex:
        return f"{_ex}\nПроверьте логин и пароль"

def main():
    while True:
        test.funct()
        df = pd.read_csv('clients_and_emails.csv', header=None)
        dates = []
        column_arrays = list(df._iter_column_arrays())
        sent_messages = list(column_arrays[3])
        length = 0
        for i in column_arrays[0]:
            date, time = i.split()
            day, month, year = map(int, date.split('.'))
            hour, minute, second = map(int, time.split(':'))
            dates.append(dt.datetime(year, month, day, hour, minute, second))
            length += 1
        now = dt.datetime.now()
        for i in range(length):
            if now - dates[i] >= dt.timedelta(minutes=1) and not sent_messages[i]:
                sent_messages[i] = True
                user = df[1][i]
                address = df[2][i]
                message = f"Здравствуйте, {user}. Недавно Вы посетили стоматологическую клинику доктора Павлова. " \
                          f"Мы хотим попросить Вас оставить отзыв о нашей клинике. Для этого необходимо перейти по ссылке ниже " \
                          f"и заполнить небольшую форму. " \
                          f"\nhttps://forms.gle/nYavKA5o2QUdeGAy8" \
                          f"\n\n\nБлагодарим Вас за отзыв."
                print(send_email(message=message, getter=address))
        df.drop(3, inplace=True, axis=1)
        df[3] = sent_messages
        df.to_csv('clients_and_emails.csv', header=False, index=False)
        sleep(30)

if __name__ == "__main__":
    main()
