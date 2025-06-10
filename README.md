# VagrantPronto

VagrantPronto è un'applicazione web Flask che permette di generare automaticamente:
- un file `Vagrantfile`
- un playbook Ansible (opzionale)
- uno script `.sh` di provisioning

Il tutto è esportabile in un archivio `.zip`.

---

## Funzionalità principali

- Selezione del sistema operativo (Ubuntu 20.04 o 22.04)
- Configurazione rete (DHCP o IP statico)
- CPU, RAM e porta SSH configurabili
- Provisioning opzionale con `apt update/upgrade`
- Scelta di strumenti DevOps da installare (Git, Docker, Jenkins, Ansible, ecc.)
- Esportazione Vagrantfile + Playbook + Script in un archivio ZIP
- Interfaccia responsive in modalità dark

---

## Esecuzione via Docker

### Build dell'immagine
```bash
docker build -t vagrantpronto .
```

### Avvio su porta libera (es: 5050)
```bash
docker run -e PORT=5000 -p 5050:5000 vagrantpronto
```

Poi apri il browser su [http://localhost:5050](http://localhost:5050)

---

## Struttura del progetto

```
progetto/
├── app.py                  # App Flask
├── script.sh               # Script shell incluso nello ZIP
├── templates/              # Pagine
│   └── index.html          # Interfaccia utente
├── playbook_builder/       # Generatore di playbook
│   ├── __init__.py         # Serve. Questo perche se non c'è, nel app.py non viene riconosciuto come modulo 
│   └── generator.py        # Generatore del playbook Ansible
├── generated/              # Output dei file generati

```

---

## Requisiti

- Python 3.8+
- Flask
- (opzionale) Docker 

---

## Esempio di output

- `Vagrantfile`
- `playbook.yml`
- `script.sh`
- `zip` pronto da scaricare

---

Realizzato da freddo18  
Docker Hub: [freddo18/vagrantpronto](https://hub.docker.com/r/freddo18/vagrantpronto)

---

## Sviluppi futuri

Questo progetto rappresenta solo la base di partenza per un sistema più completo e versatile.

Sono previsti aggiornamenti futuri che includeranno:

- Deploy online su un server pubblico con dominio accessibile da qualsiasi dispositivo, senza necessità di esecuzione locale
- Supporto per nuove distribuzioni oltre Ubuntu, come Debian, CentOS e Rocky Linux
- Rework completo del codice sorgente per una struttura più modulare e scalabile, con il supporto a diverse architetture operative
- Sistema di gestione delle utenze, con salvataggio e recupero dei progetti generati
- Integrazione di funzionalità avanzate per il provisioning e il controllo dei workflow DevOps

Lo sviluppo è attivo e aperto a suggerimenti, contributi o segnalazioni.

