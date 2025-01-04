# WoningNet-Auto
Dit is een applicatie om automatisch in te schrijven voor WoningNet. Het is ideaal om je inschrijvpunten te halen of te behouden. Je moet namelijk op 4 woningen per maand reageren om 1 zoekpunt te verdienen. Als je minder dan 1 keer per maand op een woning reageert, verlies je 1 zoekpunt. Je kan de applicatie ook gebruiken om je simpelweg in te schrijven voor een woning. Omdat je altijd de woning mag weigeren, kan je je kans hiermee vergroten op een woning. Dit is getest op ```https://www.studentenwoningweb.nl``` en op ```https://amsterdam.mijndak.nl/```. Het werkt hoogstwaarschijnlijk ook op andere varianten. Je hebt Python en Firefox nodig. Nadat de applicatie succesvol de inschrijvingen heeft gedaan, krijg je een notificatie. Enjoy! 🚀

## Setup

1. Installeer de vereisten:
    ```sh
    pip install -r requirements.txt
    ```

2. Configureer het `env.txt` bestand correct. `max_inschrijvingen` moet gelijk zijn aan hoeveel inschrijvingen je tegelijk mag.

3. Run het `index.py` bestand:
    ```sh
    py index.py
    ```

Ik raad het sterk aan om na de configuratie een Windows Scheduler of vergelijkbare functie op Mac in te stellen zodat het script elke paar weken wordt uitgevoerd.