# PJ Classroom Notifier
Nikomu se nechce každý den kontrolovat Google učebna fyziky, jestli náhodou PJ nepřidal nové úlohy do jeho materiálu pro výuku. Při přidání přílohy do materiálu se totiž nepošle automatické upozornění e-mailem. PJ Classroom Notifier je malý projekt využívající Google API k přesně tomuto účelu - automatické kontrole změny výukového materiálu.

## Jak spustit
Pozor! Tento projekt není myšlen aby ho používal kdokoliv jiný než já, následující postup je pouze orientační. Pokud chcete tento program využít pro jiné materiály v jiných Google učebnách, budete muset jeho kód upravit.

**Prerekvizity pro spuštění**:
- účet Google ve stejné doméně jako cílová učebna Google
- projekt v Google cloud s platnými OAUTH2 klíči pro desktop
- povolené scopes pro classroom a gmail API
- počítač s Linuxem, na něm python3 s modulem venv

1. **setup.sh**
Spusťte `setup.sh` pro inicializaci venv a nainstalování potřebných knihoven.

2. **Google OAUTH2**
Údaje pro OAUTH2 desktop auth flow stáhněte do souboru `credentials.json`.
Pomocí `export PJNOTIFIER_SENDER_ADDRESS=` nastavte e-mailovou adresu odesílatele, tu, pro kterou máte OAUTH2 údaje.
Spusťte `main.py`, automaticky se otevře prohlížeč s autorizačním oknem, povolte všechno a program by měl fungovat.
