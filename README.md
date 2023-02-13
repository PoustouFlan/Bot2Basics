## Bot2Basics

**Bot2Basics** est un bot Discord facilitant la création de
cours pour l'association BackToBasics.

 - Interface de création de cours

## Installation

### NixOS

```bash
git clone https://github.com/PoustouFlan/Bot2Basics.git
cd Bot2Basics
```
Ensuite, modifier le fichier `configuration.yaml`, qui doit
ressembler à :
```yaml
token:      "LeTokenDe.Votre.Bot_Ici"
guild_id:   123456789012345678
```
en remplaçant la valeur de `guild_id` par l'identifiant de votre serveur.

Enfin, pour lancer le bot, vous pouvez exécuter :
```bash
nix-shell --run make
```

Il sera potentiellement nécessaire d'envoyer une fois la commande
`$ sync` dans votre serveur pour activer les commandes slashs.

Le bot aura besoin des permissions pour voir les messages, envoyer les
messages et inclure des embeds. Aussi, il faut avoir actif le *Message Intent.*
