# SottoMonte Framework

Il **SottoMonte Framework** è una piattaforma modulare e flessibile progettata per la creazione rapida di applicazioni web. Sfrutta Python, Jinja2 e Supabase per offrire un'esperienza di sviluppo moderna e scalabile.

## 🚀 Caratteristiche Principali

* **Modularità Avanzata**: Supporta il caricamento dinamico dei moduli, facilitando l'estensibilità e la manutenzione del codice.
* **Internazionalizzazione**: Gestione multi-lingua integrata per applicazioni globali.
* **Frontend Dinamico**: Utilizzo di Jinja2 per il rendering dinamico e supporto per TypeScript nella zona applicativa.
* **Persistenza con Supabase**: Integrazione con Supabase per la gestione dei dati e autenticazione.
* **DevOps Integrato**: Strumenti per la gestione e il deployment continuo delle applicazioni.

---

### 🧩 Architettura Modulare e Dinamica

SottoMonte adotta un'architettura modulare, con una struttura ben organizzata delle cartelle e dei file. La directory principale `/src/` contiene sottocartelle come `core/`, `models/`, `services/` e `controllers/`, ciascuna con responsabilità specifiche. Questa separazione dei compiti facilita la manutenzione e l'estensibilità del codice.

---

### 🌐 Supporto Multilingua

Il framework prevede il supporto per applicazioni multilingua, come indicato nei commenti del codice. Questo consente di sviluppare applicazioni che possono essere facilmente adattate a diverse lingue e regioni, migliorando l'accessibilità e l'usabilità a livello globale.

---

### ⚙️ Caricamento Dinamico dei Moduli

Una delle caratteristiche distintive di SottoMonte è la capacità di caricare dinamicamente i moduli. Questo approccio consente di aggiungere o modificare funzionalità senza dover riavviare l'intera applicazione, migliorando la flessibilità e la scalabilità del sistema.

---

### 🧠 Gestione Automatica delle Dipendenze

Il framework è progettato per comprendere automaticamente il ciclo delle dipendenze tra i moduli. Questo significa che può determinare l'ordine corretto di caricamento e inizializzazione dei componenti, riducendo gli errori e semplificando lo sviluppo.

---

### 📦 Integrazione con Supabase per la Persistenza

SottoMonte integra Supabase come soluzione per la persistenza dei dati. Supabase è una piattaforma open-source che offre funzionalità simili a Firebase, come database in tempo reale, autenticazione e storage. Questa integrazione consente di gestire facilmente i dati dell'applicazione in modo scalabile e sicuro.

---

### 🧪 Utilizzo di WebAssembly (WASM) per la Presentazione

Il framework prevede l'uso di WebAssembly (WASM) per migliorare le prestazioni della presentazione dell'applicazione. WASM consente di eseguire codice ad alte prestazioni nel browser, offrendo un'esperienza utente più fluida e reattiva.

---

### 🛠️ DevOps e Automazione

SottoMonte include strumenti per facilitare le pratiche DevOps, come l'automazione del ciclo di vita dell'applicazione e la gestione delle configurazioni. Questo permette di implementare rapidamente nuove funzionalità e di mantenere l'applicazione aggiornata con maggiore efficienza.

---

### 📊 Binding dei Dati e Logging Avanzato

Il framework offre meccanismi avanzati per il binding dei dati tra il frontend e il backend, migliorando la sincronizzazione delle informazioni. Inoltre, include un sistema di logging e messaggistica potenziato, utile per il monitoraggio e il debug dell'applicazione.

---

### 🚀 Integrazione con TypeScript

SottoMonte prevede l'uso di TypeScript per lo sviluppo del frontend, sfruttando i vantaggi del tipaggio statico e delle funzionalità avanzate del linguaggio. Questo contribuisce a scrivere codice più robusto e manutenibile.

---

## 🛠️ Installazione

1. **Clona la repository**:

   ```bash
   git clone https://github.com/SottoMonte/framework.git
   cd framework
   ```



2. **Crea e attiva un ambiente virtuale**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```



3. **Installa le dipendenze**:

   ```bash
   pip install -r requirements.txt
   ```



4. **Avvia l'applicazione**:

   ```bash
   python3 public/app.py
   ```



## 📁 Struttura del Progetto

* `src/`: Contiene il codice sorgente principale del framework.
* `public/`: File pubblici e punto di ingresso dell'applicazione (`app.py`).
* `doc/`: Documentazione e risorse aggiuntive.
* `Dockerfile`: Configurazione per la containerizzazione dell'applicazione.
* `Procfile`: Specifiche per il deployment su piattaforme come Heroku.
* `requirements.txt`: Elenco delle dipendenze Python necessarie.

## 📌 Roadmap e TODO

* [ ] Rifattorizzare il loader dei moduli per una maggiore efficienza.
* [ ] Implementare il supporto multi-lingua completo.
* [ ] Aggiungere un sistema di caricamento dinamico con attesa tramite Jinja2.
* [ ] Creare un prodotto minimale per il rilascio iniziale.
* [ ] Integrare un sistema di iniezione delle dipendenze.
* [ ] Sviluppare pipeline DevOps per il deployment continuo.
* [ ] Migliorare il sistema di log e messaggistica.
* [ ] Implementare il binding dei dati tra frontend e backend.
* [ ] Creare e gestire progetti tramite una piattaforma dedicata.
* [ ] Utilizzare TypeScript per la zona applicativa.
* [ ] Trasformare il codice JavaScript in moduli utilizzabili in Python per la persistenza con Supabase.

## 📄 Licenza

Questo progetto è distribuito sotto la licenza MIT.

## 🤝 Contribuire

Contributi, segnalazioni di bug e suggerimenti sono benvenuti! Sentiti libero di aprire issue o pull request.

---

Per ulteriori dettagli e aggiornamenti, visita la [repository ufficiale](https://github.com/SottoMonte/framework/tree/main).