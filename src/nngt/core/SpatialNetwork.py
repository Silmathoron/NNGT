#!/usr/bin/env python
#-*- coding:utf-8 -*-

""" NeuralNetwork: detailed biological network """

from graph_tool import Graph

from NeuralNetwork import NeuralNetwork
from SpatialGraph import SpatialGraph
from Shape import Shape
from graph_measure import *



#
#---
# NeuralNetwork
#------------------------

class SpatialNetwork(NeuralNetwork,SpatialGraph):
    
    """
    .. py:currentmodule:: nngt.core
    
    The detailed class that inherits from :class:`GraphClass` and implements
    additional properties to describe spatially embedded networks with various
    biological functions and interact with the NEST simulator.

    :ivar shape: :class:`nngt.core.Shape`
		Shape of the neurons environment.
    :ivar positions: :class:`numpy.array`
		Positions of the neurons.
    :ivar neural_model: :class:`list`
        List of the NEST neural models for each neuron.
    :ivar syn_model: :class:`list`
        List of the NEST synaptic models for each connection.
    :ivar graph: :class:`graph_tool.Graph`
		Main attribute of the class instance.
    """

    #------------------#
    # Class attributes #
    #------------------#

    __num_networks = 0
    __max_id = 0    
    
    #----------------------------#
    # Instance-related functions #
    #----------------------------#
    
    def __init__ (self, nodes=0, name="Graph", weighted=True, directed=True,
                  shape=Shape(), positions=None, neuron_types="iaf_neuron",
                  syn_model="static_synapse"):
        '''
        Initialize GraphClass instance

        Parameters
        ----------
        nodes : int, optional (default: 0)
            Number of nodes in the graph.
        name : string, optional (default: "Graph")
            The name of this :class:`GraphClass` instance.
        weighted : bool, optional (default: True)
            Whether the graph edges have weight properties.
        directed : bool, optional (default: True)
            Whether the graph is directed or undirected.
        shape : :class:`~nngt.core.Shape`, optional (default: Shape())
            Shape of the neurons' environment
        positions : :class:`numpy.array`, optional (default: None)
            Positions of the neurons; if not specified and `nodes` != 0, then
            neurons will be reparted at random inside the
            :class:`~nngt.core.Shape` object of the instance.
        
        Returns
        -------
        self : :class:`~nggt.core.GraphClass`
        '''
        super(NeuralNetwork, self).__init__()
        super(SpatialGraph, self).__init__()
        self.__id = self.__class__.max_id
        self._shape = shape
        
        self.__class__.__num_networks += 1
        self.__class__.__max_id += 1
        self.__b_valid_properties = True

    @property
    def shape(self):
        return self._shape

    @NeuralNetwork.graph.getter
    def graph(self):
        self.__b_valid_properties = False
        warnings.warn("The 'graph' attribute should not be modified!")
        return self._graph

    @NeuralNetwork.graph.setter
    def graph(self, val):
        raise RuntimeError("The 'graph' attribute cannot be substituted after \
                            creation.")


    #--------#
    # Delete #
    #--------#

    def __del__ (self):
        super(NeuralNetwork, self).__del__()
        super(SpatialGraph, self).__del__()
        self.__class__.__num_networks -= 1
