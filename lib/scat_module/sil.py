#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The Silhouette Method

The range of the Silhouette value is between +1 and -1. A high value is desirable
and indicates that the point is placed in the correct cluster. If many points
have a negative Silhouette value, it may indicate that we have created too many
or too few clusters.
"""
import sys
import logging
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def Silhouette_score(dat, kmax=10):
	sil_scores = []
	# dissimilarity would not be defined for a single cluster, thus, minimum number of clusters should be 2
	if kmax <2:
		logging.error("kmax must >= 2")
		sys.exit(0)
	k_candidates = list(range(2, kmax+1))
	for k in k_candidates:
		kmeans = KMeans(n_clusters = k).fit(dat)
		labels = kmeans.labels_
		sil_scores.append(silhouette_score(dat, labels, metric = 'euclidean'))
	return zip(k_candidates, sil_scores)