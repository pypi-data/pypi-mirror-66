*********************************************
Geographical Transctions clustering algorithm
*********************************************

Name of the module stands for geographical transactions clustering. This module is an implementation of the method, developed for the third course project in HSE University. It takes dataframe with clients transactions history of the
specified format and returns list of clusters.

For the record, it was intended to be for public usage in this form, as it is a research project seeking to find a way to deal with the described problem

Installation
############

Run the following to install:

'''python

    pip install geot_cluster'''


Usage
#####

Before using make sure, that your dataset corresponds with requirements. Csv file must contain the following columns in order to work correctly

* user_id   :   string type, example: "423156821"
* event_dt  :   string type, example: "20190312"
* event_time:   string type, example: "2019-03-12 06:24:00.279"
* lattitude :   float  type, example: 49.862621
* longtitude:   see lattitude

Workflow::


    import geot_cluster

    import markov_clustering as mc
    import matplotlib.pyplot as plt
    import networkx as nx

  
    path = [path to file with data]
    data, names = geot_cluster.data_load(path)


    %matplotlib notebook
    base = [path to the folder, where to store libs with information about clients]

    archivate = True
    libs= True
    graph_f = True
    cluster_f = True


    if(archivate):
        geot_cluster.archivate_maps(data, names, levels=4)

    if(libs):
        lib = geot_cluster.graph_preparation(data, names, base) 
        prob_lib = geot_cluster.znakomstvo_by_lib(lib,data)

    lib, prob_lib = load_libs(base = base)
    
    if(graph_f):
        graph = geot_cluster.graph_forming(lib, prob_lib, treshold=0.9)

    if(cluster_f):
        result = mc.run_mcl(graph,pruning_threshold=0.7, inflation=2,expansion=2) 
        clusters = mc.get_clusters(result)

        clust_0 = clusters_to_ids(lib=lib, prob_lib=prob_lib, clusters = clusters, number = 0)
        maps = get_cluster_maps(data = data, clust = clust_0)
        print("Number of clusters", len(clusters))

        plt.figure(figsize=(10,10))
        mc.drawing.draw_graph(result, clusters, edge_color="red",node_size=15,width = 1, with_labels=True, font_size = 8)
