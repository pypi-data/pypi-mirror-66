# vim: set fileencoding=<utf-8> :
# Copyright 2018-2020 John Lees and Nick Croucher

'''Network functions'''

# universal
import os
import sys
import re
# additional
import glob
import operator
import shutil
import subprocess
import networkx as nx
import numpy as np
import pandas as pd
from tempfile import mkstemp, mkdtemp
from collections import defaultdict, Counter

from .utils import iterDistRows
from .utils import readClusters
from .utils import readExternalClusters
from .utils import readRfile

def fetchNetwork(network_dir, model, refList,
                  core_only = False, accessory_only = False):
    """Load the network based on input options

       Returns the network as a networkx, and sets the slope parameter of
       the passed model object.

       Args:
            network_dir (str)
                A network used to define clusters from :func:`~constructNetwork`
            model (ClusterFit)
                A fitted model object
            refList (list)
                Names of references that should be in the network
            core_only (bool)
                Return the network created using only core distances

                [default = False]
            accessory_only (bool)
                Return the network created using only accessory distances

                [default = False]

       Returns:
            genomeNetwork (nx.Graph)
                The loaded network
            cluster_file (str)
                The CSV of cluster assignments corresponding to this network
    """
    # If a refined fit, may use just core or accessory distances
    if core_only and model.type == 'refine':
        model.slope = 0
        network_file = network_dir + "/" + os.path.basename(network_dir) + '_core_graph.gpickle'
        cluster_file = network_dir + "/" + os.path.basename(network_dir) + '_core_clusters.csv'
    elif accessory_only and model.type == 'refine':
        model.slope = 1
        network_file = network_dir + "/" + os.path.basename(network_dir) + '_accessory_graph.gpickle'
        cluster_file = network_dir + "/" + os.path.basename(network_dir) + '_accessory_clusters.csv'
    else:
        network_file = network_dir + "/" + os.path.basename(network_dir) + '_graph.gpickle'
        cluster_file = network_dir + "/" + os.path.basename(network_dir) + '_clusters.csv'
        if core_only or accessory_only:
            sys.stderr.write("Can only do --core-only or --accessory-only fits from "
                             "a refined fit. Using the combined distances.\n")

    genomeNetwork = nx.read_gpickle(network_file)
    sys.stderr.write("Network loaded: " + str(genomeNetwork.number_of_nodes()) + " samples\n")

    # Ensure all in dists are in final network
    networkMissing = set(refList).difference(list(genomeNetwork.nodes()))
    if len(networkMissing) > 0:
        sys.stderr.write("WARNING: Samples " + ",".join(networkMissing) + " are missing from the final network\n")

    return (genomeNetwork, cluster_file)


def extractReferences(G, mashOrder, outPrefix, existingRefs = None):
    """Extract references for each cluster based on cliques

       Writes chosen references to file by calling :func:`~writeReferences`

       Args:
           G (networkx.Graph)
               A network used to define clusters from :func:`~constructNetwork`
           mashOrder (list)
               The order of files in the sketches, so returned references are in the same order
           outPrefix (str)
               Prefix for output file (.refs will be appended)
           existingRefs (list)
               References that should be used for each clique

       Returns:
           refFileName (str)
               The name of the file references were written to
           references (list)
               An updated list of the reference names
    """
    if existingRefs == None:
        references = set()
    else:
        references = set(existingRefs)

    # extract cliques from network
    cliques = list(nx.find_cliques(G))
    # order list by size of clique
    cliques.sort(key = len, reverse=True)
    # iterate through cliques
    for clique in cliques:
        alreadyRepresented = 0
        for node in clique:
            if node in references:
                alreadyRepresented = 1
                break
        if alreadyRepresented == 0:
            references.add(clique[0])

    # Find any clusters which are represented by multiple references
    clusters = printClusters(G, printCSV=False)
    ref_clusters = set()
    multi_ref_clusters = set()
    for reference in references:
        if clusters[reference] in ref_clusters:
            multi_ref_clusters.add(clusters[reference])
        else:
            ref_clusters.add(clusters[reference])

    # Check if these multi reference components have been split
    if len(multi_ref_clusters) > 0:
        # Initial reference graph
        ref_G = G.copy()
        ref_G.remove_nodes_from(set(ref_G.nodes).difference(references))

        for multi_ref_cluster in multi_ref_clusters:
            # Get a list of nodes that need to be in the same component
            check = []
            for reference in references:
                if clusters[reference] == multi_ref_cluster:
                    check.append(reference)

            # Pairwise check that nodes are in same component
            for i in range(len(check)):
                component = nx.node_connected_component(ref_G, check[i])
                for j in range(i, len(check)):
                    # Add intermediate nodes
                    if check[j] not in component:
                        new_path = nx.shortest_path(G, check[i], check[j])
                        for node in new_path:
                            references.add(node)

    # Order found references as in mash sketch files
    references = [x for x in mashOrder if x in references]
    refFileName = writeReferences(references, outPrefix)
    return references, refFileName

def writeReferences(refList, outPrefix):
    """Writes chosen references to file

    Args:
        refList (list)
            Reference names to write
        outPrefix (str)
            Prefix for output file (.refs will be appended)

    Returns:
        refFileName (str)
            The name of the file references were written to
    """
    # write references to file
    refFileName = outPrefix + "/" + os.path.basename(outPrefix) + ".refs"
    with open(refFileName, 'w') as rFile:
        for ref in refList:
            rFile.write(ref + '\n')

    return refFileName

def writeDummyReferences(refList, outPrefix):
    """Writes chosen references to file, for use with mash
    Gives sequence name twice

    Args:
        refList (list)
            Reference names to write
        outPrefix (str)
            Prefix for output file (.refs will be appended)

    Returns:
        refFileName (str)
            The name of the file references were written to
    """
    # write references to file
    refFileName = outPrefix + "/" + os.path.basename(outPrefix) + ".mash.refs"
    with open(refFileName, 'w') as rFile:
        for ref in refList:
            rFile.write("\t".join([ref, ref]) + '\n')

    return refFileName

def constructNetwork(rlist, qlist, assignments, within_label, summarise = True):
    """Construct an unweighted, undirected network without self-loops.
    Nodes are samples and edges where samples are within the same cluster

    Will print summary statistics about the network to ``STDERR``

    Args:
        rlist (list)
            List of reference sequence labels
        qlist (list)
            List of query sequence labels
        assignments (numpy.array)
            Labels of most likely cluster assignment from :func:`~PopPUNK.bgmm.assign_samples`
        within_label (int)
            The label for the cluster representing within-strain distances
            from :func:`~PopPUNK.bgmm.findWithinLabel`
        summarise (bool)
            Whether to calculate and print network summaries with :func:`~networkSummary`

            (default = True)

    Returns:
        G (networkx.Graph)
            The resulting network
    """
    connections = []
    for assignment, (ref, query) in zip(assignments, iterDistRows(rlist, qlist, self=True)):
        if assignment == within_label:
            connections.append((ref, query))

    density_proportion = len(connections) / (0.5 * (len(rlist) * (len(rlist) + 1)))
    if density_proportion > 0.4 or len(connections) > 500000:
        sys.stderr.write("Warning: trying to create very dense network\n")

    # build the graph
    G = nx.Graph()
    G.add_nodes_from(rlist)
    for connection in connections:
        G.add_edge(*connection)

    # give some summaries
    if summarise:
        (components, density, transitivity, score) = networkSummary(G)
        sys.stderr.write("Network summary:\n" + "\n".join(["\tComponents\t" + str(components),
                                                       "\tDensity\t" + "{:.4f}".format(density),
                                                       "\tTransitivity\t" + "{:.4f}".format(transitivity),
                                                       "\tScore\t" + "{:.4f}".format(score)])
                                                       + "\n")

    return G

def networkSummary(G):
    """Provides summary values about the network

    Args:
        G (networkx.Graph)
            The network of strains from :func:`~constructNetwork`

    Returns:
        components (int)
            The number of connected components (and clusters)
        density (float)
            The proportion of possible edges used
        transitivity (float)
            Network transitivity (triads/triangles)
        score (float)
            A score of network fit, given by :math:`\mathrm{transitivity} * (1-\mathrm{density})`
    """
    components = nx.number_connected_components(G)
    density = nx.density(G)
    transitivity = nx.transitivity(G)
    score = transitivity * (1-density)

    return(components, density, transitivity, score)

def addQueryToNetwork(dbFuncs, rlist, qfile, G, kmers, estimated_length,
                        assignments, model, queryDB, queryQuery = False,
                        use_mash = False, threads = 1):
    """Finds edges between queries and items in the reference database,
    and modifies the network to include them.

    Args:
        dbFuncs (list)
            List of backend functions from :func:`~PopPUNK.utils.setupDBFuncs`
        rlist (list)
            List of reference names
        qfile (str)
            File containing queries
        G (networkx.Graph)
            Network to add to (mutated)
        kmers (list)
            List of k-mer sizes
        estimated_length (int)
            Estimated length of genome, if not calculated from data
        assignments (numpy.array)
            Cluster assignment of items in qlist
        model (ClusterModel)
            Model fitted to reference database
        queryDB (str)
            Query database location
        queryQuery (bool)
            Add in all query-query distances

            (default = False)
        use_mash (bool)
            Use the mash backend
        no_stream (bool)
            Don't stream mash output

            (default = False)
        threads (int)
            Number of threads to use if new db created

            (default = 1)
    Returns:
        qlist1 (list)
            Ordered list of queries
        distMat (numpy.array)
            Query-query distances
    """
    constructDatabase = dbFuncs['constructDatabase']
    queryDatabase = dbFuncs['queryDatabase']
    readDBParams = dbFuncs['readDBParams']

    # initialise links data structure
    new_edges = []
    assigned = set()
    # These are returned
    qlist1 = None
    distMat = None

    # Set up query names
    qList, qSeqs = readRfile(qfile, oneSeq = use_mash)
    queryFiles = dict(zip(qList, qSeqs))
    if use_mash == True:
        rNames = None
        qNames = qSeqs
    else:
        rNames = qList 
        qNames = rNames

    # store links for each query in a list of edge tuples
    for assignment, (ref, query) in zip(assignments, iterDistRows(rlist, qList, self=False)):
        if assignment == model.within_label:
            new_edges.append((ref, query))
            assigned.add(query)

    # Calculate all query-query distances too, if updating database
    if queryQuery:
        sys.stderr.write("Calculating all query-query distances\n")

        qlist1, qlist2, distMat = queryDatabase(rNames = rNames,
                                                qNames = qNames, 
                                                dbPrefix = queryDB, 
                                                queryPrefix = queryDB, 
                                                klist = kmers,
                                                self = True, 
                                                number_plot_fits = 0, 
                                                threads=threads)
        queryAssignation = model.assign(distMat)
        for assignment, (ref, query) in zip(queryAssignation, iterDistRows(qlist1, qlist2, self=True)):
            if assignment == model.within_label:
                new_edges.append((ref, query))

    # Otherwise only calculate query-query distances for new clusters
    else:
        # identify potentially new lineages in list: unassigned is a list of queries with no hits
        unassigned = set(qNames).difference(assigned)

        # process unassigned query sequences, if there are any
        if len(unassigned) > 1:
            sys.stderr.write("Found novel query clusters. Calculating distances between them:\n")

            # write unassigned queries to file as if a list of references
            tmpDirName = mkdtemp(prefix=os.path.basename(queryDB), suffix="_tmp", dir="./")
            tmpHandle, tmpFile = mkstemp(prefix=os.path.basename(queryDB), suffix="_tmp", dir=tmpDirName)
            with open(tmpFile, 'w') as tFile:
                for query in unassigned:
                    if isinstance(queryFiles[query], list):
                        seqFiles = "\t".join(queryFiles[query])
                    elif isinstance(queryFiles[query], str):
                        seqFiles = queryFiles[query]
                    else:
                        raise RuntimeError("Error with formatting of q-file")
                    tFile.write(query + '\t' + seqFiles + '\n')

            # use database construction methods to find links between unassigned queries
            sketchSize = readDBParams(queryDB, kmers, None)[1]

            constructDatabase(tmpFile, kmers, sketchSize, tmpDirName, estimated_length, True, threads, False)
            qlist1, qlist2, distMat = queryDatabase(rNames = list(unassigned),
                                                    qNames = list(unassigned), 
                                                    dbPrefix = tmpDirName,
                                                    queryPrefix = tmpDirName,
                                                    klist = kmers,
                                                    self = True,
                                                    number_plot_fits = 0,
                                                    threads = threads)
            queryAssignation = model.assign(distMat)

            # identify any links between queries and store in the same links dict
            # links dict now contains lists of links both to original database and new queries
            for assignment, (query1, query2) in zip(queryAssignation, iterDistRows(qlist1, qlist2, self=True)):
                if assignment == model.within_label:
                    new_edges.append((query1, query2))

            # remove directory
            shutil.rmtree(tmpDirName)

    # finish by updating the network
    G.add_nodes_from(qNames)
    G.add_edges_from(new_edges)

    return qlist1, distMat

def printClusters(G, outPrefix = "_clusters.csv", oldClusterFile = None,
                  externalClusterCSV = None, printRef = True, printCSV = True):
    """Get cluster assignments

    Also writes assignments to a CSV file

    Args:
        G (networkx.Graph)
            Network used to define clusters (from :func:`~constructNetwork` or
            :func:`~addQueryToNetwork`)
        outPrefix (str)
            Prefix for output CSV

            Default = "_clusters.csv"
        oldClusterFile (str)
            CSV with previous cluster assignments.
            Pass to ensure consistency in cluster assignment name.

            Default = None
        externalClusterCSV (str)
            CSV with cluster assignments from any source. Will print a file
            relating these to new cluster assignments

            Default = None
        printRef (bool)
            If false, print only query sequences in the output

            Default = True
        printCSV (bool)
            Print results to file

            Default = True

    Returns:
        clustering (dict)
            Dictionary of cluster assignments (keys are sequence names)

    """
    if oldClusterFile == None and printRef == False:
        raise RuntimeError("Trying to print query clusters with no query sequences")

    newClusters = sorted(nx.connected_components(G), key=len, reverse=True)
    oldNames = set()

    if oldClusterFile != None:
        oldClusters = readClusters(oldClusterFile)
        new_id = len(oldClusters) + 1 # 1-indexed
        while new_id in oldClusters:
            new_id += 1 # in case clusters have been merged

        # Samples in previous clustering
        for prev_cluster in oldClusters.values():
            for prev_sample in prev_cluster:
                oldNames.add(prev_sample)

    # Assign each cluster a name
    clustering = {}
    foundOldClusters = []

    for newClsIdx, newCluster in enumerate(newClusters):

        # Ensure consistency with previous labelling
        if oldClusterFile != None:
            merge = False
            cls_id = None

            # Samples in this cluster that are not queries
            ref_only = oldNames.intersection(newCluster)

            # A cluster with no previous observations
            if len(ref_only) == 0:
                cls_id = str(new_id)    # harmonise data types; string flexibility helpful
                new_id += 1
            else:
                # Search through old cluster IDs to find a match
                for oldClusterName, oldClusterMembers in oldClusters.items():
                    join = ref_only.intersection(oldClusterMembers)
                    if len(join) > 0:
                        # Check cluster is consistent with previous definitions
                        if oldClusterName in foundOldClusters:
                            sys.stderr.write("WARNING: Old cluster " + oldClusterName + " split"
                                             " across multiple new clusters\n")
                        else:
                            foundOldClusters.append(oldClusterName)

                        # Query has merged clusters
                        if len(join) < len(ref_only):
                            merge = True
                            if cls_id == None:
                                cls_id = oldClusterName
                            else:
                                cls_id += "_" + oldClusterName
                        # Exact match -> same name as before
                        elif len(join) == len(ref_only):
                            assert merge == False # should not have already been part of a merge
                            cls_id = oldClusterName
                            break

            # Report merges
            if merge:
                merged_ids = cls_id.split("_")
                sys.stderr.write("Clusters " + ",".join(merged_ids) + " have merged into " + cls_id + "\n")

        # Otherwise just number sequentially starting from 1
        else:
            cls_id = newClsIdx + 1

        for cluster_member in newCluster:
            clustering[cluster_member] = cls_id

    # print clustering to file
    if printCSV:
        outFileName = outPrefix + "_clusters.csv"
        with open(outFileName, 'w') as cluster_file:
            cluster_file.write("Taxon,Cluster\n")

            # sort the clusters by frequency - define a list with a custom sort order
            # first line gives tuples e.g. (1, 28), (2, 17) - cluster 1 has 28 members, cluster 2 has 17 members
            # second line takes first element - the cluster IDs sorted by frequency
            freq_order = sorted(dict(Counter(clustering.values())).items(), key=operator.itemgetter(1), reverse=True)
            freq_order = [x[0] for x in freq_order]

            # iterate through cluster dictionary sorting by value using above custom sort order
            for cluster_member, cluster_name in sorted(clustering.items(), key=lambda i:freq_order.index(i[1])):
                if printRef or cluster_member not in oldNames:
                    cluster_file.write(",".join((cluster_member, str(cluster_name))) + "\n")

        if externalClusterCSV is not None:
            printExternalClusters(newClusters, externalClusterCSV, outPrefix, oldNames, printRef)

    return(clustering)

def printExternalClusters(newClusters, extClusterFile, outPrefix,
                          oldNames, printRef = True):
    """Prints cluster assignments with respect to previously defined
    clusters or labels.

    Args:
        newClusters (set iterable)
            The components from the graph G, defining the PopPUNK clusters
        extClusterFile (str)
            A CSV file containing definitions of the external clusters for
            each sample (does not need to contain all samples)
        outPrefix (str)
            Prefix for output CSV (_external_clusters.csv)
        oldNames (list)
            A list of the reference sequences
        printRef (bool)
            If false, print only query sequences in the output

            Default = True
    """
    # Object to store output csv datatable
    d = defaultdict(list)

    # Read in external clusters
    extClusters = readExternalClusters(extClusterFile)

    # Go through each cluster (as defined by poppunk) and find the external
    # clusters that had previously been assigned to any sample in the cluster
    for ppCluster in newClusters:
        # Store clusters as a set to avoid duplicates
        prevClusters = defaultdict(set)
        for sample in ppCluster:
            for extCluster in extClusters:
                if sample in extClusters[extCluster]:
                    prevClusters[extCluster].add(extClusters[extCluster][sample])

        # Go back through and print the samples that were found
        for sample in ppCluster:
            if printRef or sample not in oldNames:
                d['sample'].append(sample)
                for extCluster in extClusters:
                    if extCluster in prevClusters:
                        d[extCluster].append(";".join(prevClusters[extCluster]))
                    else:
                        d[extCluster].append("NA")

    pd.DataFrame(data=d).to_csv(outPrefix + "_external_clusters.csv",
                                columns = ["sample"] + list(extClusters.keys()),
                                index = False)
