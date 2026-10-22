# EduPilot Bénin — architecture de référence

## 1. Positionnement

EduPilot est un SaaS scolaire multi-établissements pour le Bénin. Il couvre les élèves, classes, matières, notes, bulletins, paiements, notifications et assistants IA pédagogiques.

Le dépôt `osnyl/-jarvis-v2` contient une base personnelle Expo/React Native + Firebase Auth + passerelle Python. Cette base peut fournir des briques réutilisables, mais le produit scolaire doit vivre dans un dépôt séparé et multi-tenant.

## 2. Rôles

- **Directeur** : pilotage, validation finale, utilisateurs, indicateurs.
- **Secrétaire** : inscriptions, dossiers, paiements, reçus, communications.
- **Censeur** : classes, notes, absences, bulletins, suivi pédagogique.
- **Enseignant** : saisie des évaluations de ses classes et matières.
- **Élève / parent** : consultation de ses propres résultats, échéances et recommandations.

## 3. Architecture logique

```text
Web / mobile
    -> API HTTPS + identité
    -> services métier : identité, élèves, notes, bulletins, paiements,
       notifications, documents, IA
    -> PostgreSQL + stockage objet + file de tâches + audit
```

Toutes les données portent un `school_id`. Les droits sont contrôlés côté serveur avec RBAC et, si nécessaire, ABAC par établissement, classe et période.

## 4. Entités

`School`, `User`, `Student`, `Classroom`, `Subject`, `Assessment`, `Grade`, `ReportCard`, `Invoice`, `Payment`, `Receipt`, `Notification`, `AiJob`, `AuditEvent`.

Une note publiée ne doit pas être écrasée silencieusement : toute correction crée une version ou un événement d’audit.

## 5. MVP recommandé

1. Authentification et rôles.
2. Établissement, année, niveaux, classes, matières.
3. Élèves et responsables.
4. Saisie/import de notes et calcul de moyennes.
5. Validation et génération de bulletins PDF.
6. Paiements enregistrés et reçus.
7. Notifications in-app/e-mail/SMS.
8. Audit, sauvegardes et exports.

L’IA et le Mobile Money viennent ensuite, après validation du MVP.

## 6. IA et traduction

Les fonctions IA sont des services contrôlés : résumé de cours, fiches de révision, analyse des tendances, priorités de travail et traduction. L’IA ne modifie jamais une note et ne décide jamais seule d’une sanction ou d’une admission. Les sorties sensibles sont validées par un humain et l’original du bulletin est conservé.

## 7. Sécurité

- HTTPS, secrets dans le gestionnaire de secrets.
- MFA pour les comptes sensibles.
- Chiffrement des documents et sauvegardes.
- Journal d’audit append-only.
- Limites d’accès par établissement et par rôle.
- Environnements dev/test/prod séparés.
- Sauvegarde quotidienne et test de restauration mensuel.

## 8. Adaptation de Jarvis

Le code actuel utilise Firebase Auth et une passerelle WSGI personnelle avec liste blanche d’un seul utilisateur. Pour EduPilot, remplacer cette liste blanche par un contrôle `school_id` + rôles persistés en base ; séparer les endpoints personnels de Jarvis de l’API scolaire ; ne jamais mettre de secrets ou de données élèves dans un dépôt public.

## 9. Roadmap

- **Phase 0** : cadrage avec un établissement pilote et collecte de bulletins anonymisés.
- **Phase 1** : MVP administratif.
- **Phase 2** : notifications, portail parent/élève, imports.
- **Phase 3** : IA et traduction avec validation humaine.
- **Phase 4** : Mobile Money, mode faible connectivité, multi-campus et industrialisation.
