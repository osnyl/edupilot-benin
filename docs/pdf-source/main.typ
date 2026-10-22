#import "report-theme.typ": report-accent, report-theme

#show: report-theme.with(
  title: "EduPilot Bénin",
  author: "Manus — dossier de conception",
  rhythm: "report",
  running-header: true,
)

#let card(title, body) = block(
  fill: luma(246),
  stroke: (left: 3pt + report-accent),
  radius: 5pt,
  inset: 10pt,
  width: 100%,
)[
  #text(weight: "bold", fill: report-accent)[#title]\
  #v(0.35em)
  #body
]

#let tag(text) = box(fill: rgb("e8f1ff"), radius: 3pt, inset: (x: 5pt, y: 2pt))[#text]

// ---------- Page de titre ----------
#page(margin: (top: 30%, x: 2.2cm), numbering: none, header: none)[
  #set par(first-line-indent: 0em)
  #align(center)[
    #text(size: 27pt, weight: "bold", fill: report-accent)[EduPilot Bénin]
    #v(0.6em)
    #text(size: 15pt, fill: luma(75))[Architecture et feuille de route d’un SaaS scolaire multi-rôles]
    #v(2em)
    #line(length: 42%, stroke: 0.6pt + luma(160))
    #v(2em)
    #text(size: 11pt)[
      Dossier de cadrage fonctionnel et technique \
      Version 1.0 — 22 octobre 2026 \
      Préparé pour le projet d’un établissement scolaire au Bénin
    ]
    #v(3em)
    #card([Décision de conception], [Commencer par un MVP fiable de gestion scolaire, puis ajouter l’IA et la traduction comme services contrôlés, jamais comme source unique de décision.])
  ]
]

// ---------- Sommaire ----------
#page(numbering: none, header: none)[
  #outline(title: [Sommaire], indent: 1.5em)
]
#counter(page).update(1)

= Résumé exécutif

EduPilot est une plateforme web et mobile destinée aux établissements scolaires de Porto-Novo et, plus largement, du Bénin. Elle centralise les élèves, classes, matières, notes, bulletins, paiements et communications, avec trois rôles de départ : directeur, secrétaire et censeur. Les élèves et leurs parents peuvent ensuite disposer d’un accès limité pour consulter les résultats, les échéances et les recommandations pédagogiques.

Le projet répond à un problème concret : les informations scolaires sont souvent réparties entre cahiers, fichiers Excel, messages WhatsApp et documents papier. L’objectif n’est donc pas seulement de « faire une application », mais de créer une source officielle, traçable et compréhensible pour l’établissement.

#card([Recommandation principale], [Ne pas transformer immédiatement le projet en une grande plateforme « tout-en-un ». Livrer d’abord : #strong[élèves + classes + notes + bulletins + paiements + notifications + droits d’accès]. L’IA vient après la qualité des données.])

= Vision, utilisateurs et valeur

== Vision produit

Faire gagner du temps à l’administration, réduire les erreurs de report de notes, donner aux familles une visibilité claire sur la scolarité et aider chaque élève à comprendre ses points forts et ses priorités de travail.

== Utilisateurs cibles

#table(
  columns: (1.2fr, 2.5fr, 2.5fr),
  inset: 6pt,
  align: (left, left, left),
  fill: luma(248),
  table.header([*Rôle*], [*Besoins principaux*], [*Droits recommandés*]),
  [Directeur], [Pilotage global, indicateurs, validation, sécurité, paiements], [Lecture globale, validation des bulletins, gestion des utilisateurs et paramètres]),
  [Secrétaire], [Inscription, dossiers, paiements, reçus, communications], [Gestion administrative ; pas de modification libre des notes]),
  [Censeur], [Classes, absences, notes, bulletins, suivi disciplinaire], [Saisie et contrôle pédagogique ; publication après validation]),
  [Enseignant], [Saisie des évaluations et appréciations], [Accès uniquement à ses classes et matières]),
  [Élève / parent], [Consultation et compréhension des résultats], [Lecture de ses propres données, notifications et recommandations]),
)

== Proposition de valeur

- Un tableau de bord par rôle, simple et adapté au mobile.
- Une fiche élève unique : identité, classe, responsables, notes, absences, paiements et bulletins.
- Une traçabilité : qui a modifié quoi, quand et pourquoi.
- Des bulletins générés automatiquement, exportables en PDF et traduisibles avec relecture humaine.
- Des alertes utiles : paiement à venir, retard, note manquante, bulletin prêt, progression inhabituelle.
- Une IA pédagogique qui explique les tendances sans remplacer le professeur.

= Périmètre fonctionnel

== Socle administratif

#enum(
  [Créer l’année scolaire, les niveaux, les classes, les matières et les coefficients.],
  [Importer ou enregistrer les élèves avec identifiant interne, contacts et responsables.],
  [Affecter un élève à une classe et conserver l’historique des changements.],
  [Gérer les comptes utilisateurs, leurs rôles et leur établissement.],
  [Rechercher rapidement un élève, une classe ou une opération.],
)

== Notes et progression

Chaque évaluation doit être enregistrée avec la matière, le type d’épreuve, la date, le barème, la note, le coefficient, l’auteur et l’état de validation. Le système calcule les moyennes avec des règles configurables ; il ne doit pas écraser les données originales.

#card([Règle importante], [Une note corrigée doit produire une nouvelle version ou un journal de modification. Il faut pouvoir retrouver l’ancienne valeur, l’auteur de la correction et le motif.])

Fonctions prévues : saisie individuelle ou par grille, import CSV/Excel, contrôles de cohérence, calcul de moyennes, classement si l’établissement l’autorise, comparaison période précédente, détection de notes absentes et verrouillage après publication.

== Bulletins et traduction

Le moteur de bulletin assemble les informations validées : identité, période, matières, notes, moyennes, appréciations, absences, décision et signatures. Il produit un PDF avec un numéro de version et un QR code de vérification.

La traduction doit créer une copie clairement identifiée comme « traduction », conserver le bulletin original et afficher la langue cible. Pour les appréciations sensibles, l’IA propose une traduction ; le censeur ou le directeur valide avant publication.

== Paiements et scolarité

Le module doit suivre : montant attendu, échéances, versements, reste à payer, remise éventuelle, reçu, canal de paiement et auteur de l’opération. Il peut envoyer une notification avant échéance, à l’échéance et en cas de retard.

Au démarrage, il est plus prudent de gérer les paiements comme des enregistrements validés par le secrétariat. L’intégration Mobile Money peut venir ensuite, avec un prestataire local et des webhooks idempotents ; aucune confirmation ne doit reposer uniquement sur une capture d’écran.

== Notifications

Canaux possibles : notification dans l’application, e-mail, SMS et WhatsApp via un fournisseur autorisé. Chaque notification possède un modèle, une langue, une date d’envoi, un statut et une trace d’erreur. Les utilisateurs doivent pouvoir choisir leurs préférences.

= IA pédagogique

== Cas d’usage

- Résumer un cours fourni par l’enseignant ou l’élève.
- Générer des fiches de révision et des questions d’entraînement.
- Analyser les notes par matière, période et compétence.
- Repérer les matières prioritaires selon la progression et les coefficients.
- Suggérer un plan de travail hebdomadaire.
- Aider les candidats au bac à visualiser les matières à fort enjeu.
- Traduire un bulletin ou une appréciation avec conservation de l’original.
- Répondre à des questions sur les règles internes, à partir de documents validés.

== Garde-fous

L’IA ne doit jamais modifier une note, déclarer un élève admis ou exclu, ni remplacer la validation du personnel. Les recommandations doivent afficher leur période d’analyse et indiquer quand les données sont insuffisantes. Les documents envoyés à un modèle doivent être minimisés et protégés ; les données d’un établissement ne doivent pas être utilisées pour entraîner un modèle sans accord explicite.

== Exemple de recommandation

#card([Sortie attendue], [« Sur les deux dernières périodes, la moyenne en mathématiques baisse de 12,4 à 9,8. Les thèmes les plus fragiles semblent être les fonctions et la résolution d’équations. Priorité suggérée : deux séances de 30 minutes par semaine, puis une évaluation courte. Cette suggestion doit être vérifiée par l’enseignant.])

= Architecture cible

== Principe général

L’architecture doit être multi-tenant : un même système peut héberger plusieurs établissements, mais chaque donnée est rattachée à un `school_id`. Le serveur vérifie l’établissement et le rôle à chaque requête ; l’interface ne suffit jamais pour protéger une donnée.

```text
Application web / mobile
          |
     API HTTPS + authentification
          |
  Services métier : identité | notes | bulletins | paiements | notifications | IA
          |
Base relationnelle   Stockage documents   File de tâches   Journal d’audit
          |                 |                 |                  |
   sauvegardes       PDF/originaux       SMS/e-mail       alertes sécurité
```

== Composants proposés

#table(
  columns: (1.7fr, 2.6fr, 2.2fr),
  inset: 6pt,
  fill: luma(248),
  table.header([*Composant*], [*Responsabilité*], [*Choix initial*]),
  [Client web], [Portail directeur, secrétaire, censeur et enseignants], [React/Next.js ou équivalent]),
  [Client mobile], [Consultation élève/parent, notifications et accès terrain], [Expo/React Native ; le dépôt Jarvis fournit déjà une base]),
  [API], [Règles métier, contrôle d’accès, validation et agrégation], [Python FastAPI ou Flask structuré]),
  [Identité], [Connexion, MFA optionnelle, rôles et sessions], [Firebase Auth au départ ou fournisseur OIDC]),
  [Base de données], [Élèves, notes, paiements, permissions, journaux], [PostgreSQL]),
  [Documents], [Bulletins PDF, pièces justificatives, cours], [Stockage objet compatible S3]),
  [Tâches], [PDF, traduction, notifications, analyses IA], [Redis + worker ou file managée]),
  [Observabilité], [Logs, erreurs, métriques, audit], [Sentry + journaux structurés]),
)

== Entités principales

- `School` : établissement, année active, paramètres et langues.
- `User` : compte, identité, statut, établissement(s), rôle(s).
- `Student` : élève, matricule, responsables, classe et historique.
- `Classroom` : niveau, série, classe, année scolaire.
- `Subject` et `Assessment` : matière, épreuve, barème, coefficient, période.
- `Grade` : note originale, note publiée, auteur, statut et version.
- `ReportCard` : bulletin, période, langue, version et validation.
- `Invoice`, `Payment`, `Receipt` : dette, versement, reçu et rapprochement.
- `Notification` : modèle, destinataire, canal, statut et horodatage.
- `AiJob` : type d’analyse, entrée, résultat, coût, modèle, validation humaine.
- `AuditEvent` : action, acteur, ressource, ancienne valeur, nouvelle valeur.

== Flux critique : publication d’un bulletin

1. Le censeur clôt la période et contrôle les notes manquantes.
2. Le serveur calcule les moyennes à partir des notes validées.
3. Un bulletin brouillon est généré et contrôlé.
4. Le censeur le soumet au directeur.
5. Le directeur valide ; la version devient immuable.
6. Le PDF original est stocké et une traduction peut être demandée.
7. Une notification est envoyée aux destinataires autorisés.

= Sécurité, confidentialité et continuité

== Contrôle d’accès

Utiliser RBAC pour les rôles et, si nécessaire, ABAC pour les limites de classe, campus ou période. Le directeur peut voir les indicateurs de son établissement ; le secrétaire voit les données administratives ; le censeur voit le pédagogique ; l’élève ne voit que son dossier.

== Mesures minimales

- HTTPS partout, secrets hors du dépôt et rotation des clés.
- Mots de passe gérés par un fournisseur d’identité ; MFA pour les comptes sensibles.
- Chiffrement au repos des documents et sauvegardes chiffrées.
- Journal d’audit non modifiable par les utilisateurs ordinaires.
- Export et suppression contrôlés, avec conservation légale à définir.
- Limitation des téléchargements et protection contre les fichiers malveillants.
- Sauvegarde quotidienne, test de restauration mensuel et plan de reprise.
- Environnement séparé pour développement, test et production.

= Adaptation au dépôt Jarvis existant

Le dépôt `osnyl/-jarvis-v2` contient une application Expo/React Native, Firebase Auth, un client API et une passerelle Python WSGI qui vérifie un token Firebase avant d’appeler un backend personnel. C’est une base réutilisable pour l’authentification mobile et certaines fonctions IA.

Cependant, la passerelle actuelle est explicitement personnelle : elle utilise une liste blanche d’un seul UID ou e-mail (`JARVIS_ALLOWED_UID` / `JARVIS_ALLOWED_EMAIL`) et transmet une clé interne. Pour EduPilot, il faudra remplacer cette logique par :

- un `school_id` vérifié côté serveur ;
- des rôles et permissions persistés en base ;
- des règles d’accès par élève, classe et établissement ;
- un audit de toutes les écritures ;
- une API séparée des endpoints personnels de Jarvis.

La bonne stratégie est donc de conserver Jarvis comme brique IA ou prototype mobile, mais de créer un dépôt privé propre pour le produit scolaire, afin de ne pas mélanger données personnelles et produit multi-établissements.

= MVP et feuille de route

== Phase 0 — cadrage (1 à 2 semaines)

Valider avec un directeur, un secrétaire, un censeur et deux enseignants les écrans, les règles de calcul, les formats de bulletins, les langues utiles et les canaux de notification. Collecter des exemples anonymisés de bulletins et de reçus.

== Phase 1 — MVP administratif (4 à 8 semaines)

Authentification, établissement, utilisateurs, élèves, classes, matières, notes, moyennes, bulletins PDF, paiements enregistrés, reçus, tableau de bord et audit. Cette phase doit être utilisable même sans IA.

== Phase 2 — communication (2 à 4 semaines)

Notifications in-app, e-mail ou SMS, rappels d’échéance, espace parent/élève et imports Excel/CSV contrôlés.

== Phase 3 — IA contrôlée (3 à 6 semaines)

Résumé de cours, recommandations de travail, analyse de progression, traduction avec validation, suivi du coût et des erreurs du modèle.

== Phase 4 — industrialisation

Mobile Money, multi-campus, tableaux de bord avancés, mode faible connectivité, synchronisation différée, intégration avec partenaires et rapports anonymisés.

= Modèle économique possible

- Abonnement mensuel par établissement, avec paliers selon le nombre d’élèves.
- Frais d’installation et de formation.
- Modules optionnels : SMS, Mobile Money, traduction avancée, IA et archivage.
- Offre pilote gratuite limitée pour recueillir les retours d’un établissement.

Éviter de facturer l’élève individuellement pour les fonctions essentielles. La décision d’achat appartient généralement à la direction, tandis que la valeur est ressentie par le secrétariat, le censeur, les enseignants et les familles.

= Risques et décisions à prendre

#table(
  columns: (2.2fr, 2.7fr, 2.2fr),
  inset: 6pt,
  fill: luma(248),
  table.header([*Risque*], [*Impact*], [*Réponse*]),
  [Données incorrectes], [Bulletin ou paiement erroné], [Validation, historique, imports contrôlés et sauvegardes]),
  [Mauvaise connexion], [Service inutilisable sur le terrain], [Interface légère, cache de lecture, reprise des envois]),
  [Abus de privilèges], [Accès aux dossiers d’un autre élève], [RBAC + contrôles serveur + audit]),
  [IA trop confiante], [Mauvais conseil pédagogique], [Sources, limites, validation humaine]),
  [Dépendance fournisseur], [Blocage SMS, cloud ou IA], [Abstractions, export des données, solution de secours]),
  [Adoption faible], [Le personnel continue sur papier], [Formation, écrans simples, pilote avec un établissement]),
)

#card([Décisions prioritaires], [1. Nom du produit et établissement pilote.  2. Règles officielles de calcul.  3. Modèle de bulletin.  4. Langues à supporter.  5. Canal de notification.  6. Hébergement et responsable des données.  7. Budget mensuel acceptable.])

= Conclusion

EduPilot est une idée réaliste si elle est traitée comme un produit de gestion scolaire avant d’être traitée comme un produit d’IA. La valeur initiale vient de données propres, de bulletins fiables, de paiements traçables et d’un accès par rôle. L’IA peut ensuite rendre ces données plus utiles : expliquer une progression, proposer une révision et traduire un document, avec validation humaine.

Le dépôt privé associé doit rester le lieu du cadrage, des décisions et du code du produit scolaire. Le dépôt Jarvis public ne doit pas recevoir de secrets, de données d’élèves ou de logique spécifique à un établissement.

#pagebreak()
= Annexe — lexique rapide

- *RBAC* : contrôle d’accès basé sur les rôles.
- *ABAC* : contrôle d’accès basé sur des attributs comme l’établissement ou la classe.
- *MVP* : première version utile, limitée au périmètre essentiel.
- *Multi-tenant* : plusieurs établissements isolés dans la même plateforme.
- *Webhook* : notification automatique envoyée par un service à un autre.
- *Idempotence* : possibilité de rejouer une opération sans créer un doublon.
- *Audit* : historique des actions et des modifications.
- *RAG* : recherche de documents pertinents avant génération d’une réponse IA.
