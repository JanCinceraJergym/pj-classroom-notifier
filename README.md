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

## Automatizace
Hurá! Program funguje, ale moc jsme si nepomohli, stále je potřeba ho manuálně spouštět. Naštěstí žijeme v době mocných nástrojů, které můžeme využít k automatizaci.   
Pro automatické spuštění programu můžete využít programy jako jsou cron, nebo systemd timers. Osobně jsem se rozhodl pro druhou možnost. Nejdřív jsem vytvořil timer unit, který pravidelně každý den v 5:00 a v 19:00 spustí service unit. V service unit jsem pouze nastavil cílový program pro spuštení (tedy main.py) a jako bezpečností prvek systémového uživatele, který zajišťuje izolaci od zbytku systému.

## Odkazy
[Using OAuth 2.0 to Access Google APIs](https://developers.google.com/identity/protocols/oauth2)   
[Google API Client Library for Python Docs](https://googleapis.github.io/google-api-python-client/docs/)   
[Google Cloud Console](https://console.cloud.google.com)   
[Classroom API v1](https://googleapis.github.io/google-api-python-client/docs/dyn/classroom_v1)   
[Gmail API v1](https://googleapis.github.io/google-api-python-client/docs/dyn/gmail_v1)   
[systemd/Timers - ArchWiki](https://wiki.archlinux.org/title/Systemd/Timers)   
[man systemd.service](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html)   
