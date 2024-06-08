# Plik z wysylaniem maila przez GMAIL

from email.message import EmailMessage
import ssl
import smtplib
import mimetypes
import os

def content_builder(start_date,end_date,max_price_time_value,min_price_time_value,max_price_time_city, min_price_time_city, most_pop_city,av_price, most_pop_airline, city):
    body = f"""
    Cześć, widzę, że wyszukiwałeś loty z miasta: {city} w dniu {start_date}. Jeżeli możesz pozwolić sobie na elastyczność, poniżej przedstawiamy szczegółowy raport na temat lotów w tym i trzech kolejnych dniach!

    \nNajpopularniejszym kierunkiem w dniach od {start_date} do {end_date} jest: {most_pop_city},
    Najmniej kosztuje minuta lotu do: {min_price_time_city} i wynosi ona: {min_price_time_value} zł,
    Najwięcej kosztuje minuta lotu do: {max_price_time_city} i wynosi ona: {max_price_time_value} zł,
    Średnia cena biletu lotniczego w tych dniach (niezależnie od kierunku) wynosi: {av_price} zł,
    Najwięcej tanich biletów oferuje linia: {most_pop_airline}
    
    \nPozdrawiamy, 
    Zespół Cheap Sky 
    """
    return body
                              
def mail_creator(receiver, content, attachment_paths):
    email_sender = 'cheapskyscraper@gmail.com'
    email_password = 'wlrx vjsv ppxy jsna'
    subject = 'Szukasz tanich lotów?'


    #body = content
    body = content

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(body)

    for attachment_path in attachment_paths:
            if attachment_path:
                # Określenie typu pliku
                mime_type, _ = mimetypes.guess_type(attachment_path)
                mime_type, mime_subtype = mime_type.split('/')

                with open(attachment_path, 'rb') as attachment:
                    em.add_attachment(attachment.read(),
                                    maintype=mime_type,
                                    subtype=mime_subtype,
                                    filename=os.path.basename(attachment_path))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, receiver, em.as_string())

