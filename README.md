# Graphes et Urbanisme

Ce dépôt contient le rapport et les scripts associés à mon stage de L3 réalisé au LAMSADE (Université Paris-Dauphine).

## Objectif
Étudier comment orienter certaines rues à sens unique dans un réseau urbain tout en préservant l’accessibilité globale de la ville et en limitant l’augmentation des temps de trajet.

## Méthodes
Le problème est modélisé par un **graphe mixte** représentant le réseau routier :
- arcs : rues déjà à sens unique
- arêtes : rues pouvant être orientées

Nous proposons :
- un **modèle d’optimisation**
- une **heuristique** permettant de trouver rapidement des solutions

## Contenu
- [rapport](Rapport.pdf)
- scripts d’expérimentation

## Contexte
Stage de recherche encadré au **LAMSADE (Université Paris-Dauphine)** en théorie des graphes et recherche opérationnelle.

## Technologies
Python, optimisation combinatoire, théorie des graphes


# Street Orientation Optimization – Graph Theory Project

This repository contains the report and scripts associated with my undergraduate research internship carried out at **LAMSADE (Paris-Dauphine University)**.

The project focuses on modeling and solving an urban traffic planning problem using **graph theory and optimization methods**.

## Problem

With the ecological transition and the growing number of cyclists and pedestrians, cities increasingly convert certain streets into **one-way streets** in order to free space for other uses (bike lanes, pedestrian areas, greenery).

However, these local modifications can negatively affect the **global accessibility of the city**. The challenge is therefore to determine orientations for streets while ensuring that all locations remain reachable and that detours remain limited.

## Modeling

The road network is modeled as a **mixed graph**:

- **Arcs** represent streets already constrained to one-way traffic.
- **Edges** represent streets that can still be oriented.

The objective is to determine an orientation for the undirected edges while preserving the overall accessibility of the network and limiting travel time increases.

## Methods

To address this problem, the project includes:

- a **mathematical optimization model**
- a **heuristic algorithm** to quickly compute feasible solutions
- experimental evaluation of the proposed methods

## Repository Structure

- `report/` – internship report describing the model, algorithms, and results  
- `scripts/` – Python scripts used for experimentation  

## Technologies

- Python  
- Graph theory  
- Combinatorial optimization  
- Experimental evaluation

## Context

Research internship in **Graph Theory and Operations Research**, conducted at **LAMSADE (Paris-Dauphine University)**.

Supervised by **Virginie Gabrel** and **Cécile Murat**.
