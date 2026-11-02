# EduPilot Bénin

Architecture et feuille de route d’un SaaS scolaire multi-rôles pour les établissements du Bénin.

## Livrables

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — architecture de référence, rôles, modèle de données, sécurité, MVP et roadmap.
- [`docs/EduPilot_Benin_Architecture.pdf`](docs/EduPilot_Benin_Architecture.pdf) — rapport complet destiné au cadrage et à la présentation du projet.

## Point de départ technique

Le dépôt public [`osnyl/-jarvis-v2`](https://github.com/osnyl/-jarvis-v2) contient une base Expo/React Native + Firebase Auth + passerelle Python. Il peut fournir des briques pour le client mobile et les fonctions IA, mais EduPilot doit conserver une architecture multi-établissements séparée, sans secrets ni données d’élèves dans le dépôt public.

## Principe de livraison

1. Valider les règles scolaires avec un établissement pilote.
2. Construire le MVP administratif : élèves, classes, notes, bulletins, paiements et audit.
3. Ajouter les notifications et le portail parent/élève.
4. Ajouter l’IA et la traduction avec validation humaine.

Ce dépôt contient le cadrage ; il ne contient pas encore l’application complète.
