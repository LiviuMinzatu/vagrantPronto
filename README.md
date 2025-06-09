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
├── templates/
│   └── index.html          # Interfaccia utente
├── playbook_builder/
│   ├── __init__.py
│   └── generator.py        # Generatore del playbook Ansible
├── generated/              # Output dei file generati
├── Dockerfile              # (opzionale) per containerizzazione
└── requirements.txt        # (opzionale) per gestione dipendenze
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
