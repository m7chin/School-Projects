package student;

import java.util.Arrays;

import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.ArrayList;

import game.GetOutState;
import game.Tile;
import game.FindState;
import game.SewerDiver;
import game.Node;
import game.NodeStatus;
import game.Edge;

public class DiverMax extends SewerDiver {

	//base dfsWalk to get to the ring
	LinkedList<Long> visited = new LinkedList<Long>();
	public void dfsWalk(FindState state) {
		long u = state.currentLocation();
		visited.add(u);
		for(NodeStatus w : state.neighbors()) {
			if(!visited.contains(w.getId())) {
				state.moveTo(w.getId());
				if(state.distanceToRing() == 0) {
					return;
				}
				else {
					dfsWalk(state);
					if(state.distanceToRing() == 0) {
						return;
					}
					state.moveTo(u);				
				}
			}		
		}
	}
	
	//A dfsWalk that chooses the next node (neighbor) which is has the lowest
	// value of distance to ring
	ArrayList<Long> list = new ArrayList<Long>();
	public void optimized(FindState state) {
		Long u = state.currentLocation();
    	list.add(u);
    	ArrayList<NodeStatus> list2 = new ArrayList<NodeStatus>();
    	for (NodeStatus n : state.neighbors()) {
    			list2.add(n);
    		
    	}
    	sort(list2);
    	for (int i = 0; i < list2.size() ; i = i + 1) {
    		if (!list.contains(list2.get(i).getId())) {
    			state.moveTo(list2.get(i).getId());
    			if(state.distanceToRing() == 0) {
    				return;
    			}
    			findRing(state);
    			if(state.distanceToRing() == 0) {
    				return;
    			}
    			state.moveTo(u);
    	}
    	}
	}
	//A insertion sort function for an Arraylist with type NodeStatus
	public static ArrayList<NodeStatus> sort(ArrayList<NodeStatus> b) {
		   //sort b[], an array of int
		   //inv: b[0...i-1] is sorted
		   for (int i =0; i < b.size(); i= i+1) {
			   //Push b[i] down to its sorted
			   //position in b[0..i]
			   int k =i;
			   while (k>0 && b.get(k).compareTo(b.get(k-1)) < 0) {
				   NodeStatus temp = b.get(k);
				   b.set(k, b.get(k-1));
				   b.set(k-1, temp);
				   k = k-1;
			   }
		   }
		   return b;
	}
	
	
    /** Get to the ring in as few steps as possible. Once you get there, 
     * you must return from this function in order to pick
     * it up. If you continue to move after finding the ring rather 
     * than returning, it will not count.
     * If you return from this function while not standing on top of the ring, 
     * it will count as a failure.
     * 
     * There is no limit to how many steps you can take, but you will receive
     * a score bonus multiplier for finding the ring in fewer steps.
     * 
     * At every step, you know only your current tile's ID and the ID of all 
     * open neighbor tiles, as well as the distance to the ring at each of these tiles
     * (ignoring walls and obstacles). 
     * 
     * In order to get information about the current state, use functions
     * currentLocation(), neighbors(), and distanceToRing() in FindState.
     * You know you are standing on the ring when distanceToRing() is 0.
     * 
     * Use function moveTo(long id) in FindState to move to a neighboring 
     * tile by its ID. Doing this will change state to reflect your new position.
     * 
     * A suggested first implementation that will always find the ring, but likely won't
     * receive a large bonus multiplier, is a depth-first walk. Some
     * modification is necessary to make the search better, in general.*/
    @Override public void findRing(FindState state) {
        //TODO : Find the ring and return.
        // DO NOT WRITE ALL THE CODE HERE. DO NOT MAKE THIS METHOD RECURSIVE.
        // Instead, write your method elsewhere, with a good specification,
        // and call it from this one.
    	optimized(state);
    	return;
    	
    	//Breadth first search: check each neighbor, find each neighbors distance to ring, move to shortest distance
        
    }


    /** Get out of the sewer system before the steps are all used, trying to collect
     * as many coins as possible along the way. Your solution must ALWAYS get out
     * before the steps are all used, and this should be prioritized above
     * collecting coins.
     * 
     * You now have access to the entire underlying graph, which can be accessed
     * through GetOutState. currentNode() and getExit() will return Node objects
     * of interest, and getNodes() will return a collection of all nodes on the graph. 
     * 
     * You have to get out of the sewer system in the number of steps given by
     * getStepsRemaining(); for each move along an edge, this number is decremented
     * by the weight of the edge taken.
     * 
     * Use moveTo(n) to move to a node n that is adjacent to the current node.
     * When n is moved-to, coins on node n are automatically picked up.
     * 
     * You must return from this function while standing at the exit. Failing to
     * do so before steps run out or returning from the wrong node will be
     * considered a failed run.
     * 
     * Initially, there are enough steps to get from the starting point to the
     * exit using the shortest path, although this will not collect many coins.
     * For this reason, a good starting solution is to use the shortest path to
     * the exit. */
    @Override public void getOut(GetOutState state) {
        //TODO: Get out of the sewer system before the steps are used up.
        // DO NOT WRITE ALL THE CODE HERE. Instead, write your method elsewhere,
        //with a good specification, and call it from this one.
    	List<Node> coins = findCoins(state);
    	List<Node> sorted = sortList(coins,state);
    	while(sorted.size() != 0 && getShortestPath(state) < state.stepsLeft() - 31) {
    		goToCoins(sorted.get(0),state);
    		sorted.remove(sorted.get(0));
    		sorted = sortList(sorted,state);
    	}
    	escape(state);
    }
    
    //Method that uses shortest path algorithm to get to the exit
    public void escape(GetOutState state){
    	Node start = state.currentNode();
    	Node end = state.getExit();
    	List<Node>shortPath = Paths.shortestPath(start, end);
    	for(int i = 1; i < shortPath.size(); i++) {
    		state.moveTo(shortPath.get(i));
    	}
    	return;
    }
    
    //Creates a linked list of all the coins on the map
    public List<Node> findCoins(GetOutState state) {
    	Collection<Node> map = state.allNodes();
    	LinkedList<Node> coins = new LinkedList<Node>();
    	for(Node w: map) {
    		if(w.getTile().coins() != 0) {
    			coins.add(w);
    		}
    	}
    	return coins;
    }
    
    //finds the closest coin to Max at his current location
    public Node findClosestCoin(List<Node> coins, GetOutState state){
    	Node closest = coins.get(0);
    	int closestDist = distanceToCoin(closest, state);
    	int index = 0;
    	for( Node w :coins) {
    		if(distanceToCoin(w, state) < closestDist) {
    			closestDist = distanceToCoin(w, state);
    			closest = w;
    			index = coins.indexOf(w);
    		}
    	}
    	coins.remove(index);
    	return closest;
    }
    
    //Uses findClosestCoin and findCoins to create a linked list of coins sorted by the closest coins
    public List<Node> sortList(List<Node> coins, GetOutState state){
    	List<Node> sorted = new LinkedList<Node>();
    	while(coins.size() > 0) {
    		sorted.add(findClosestCoin(coins,state));
    	}
    	return sorted;
    }
    
    //finds the shortest path distance to a certain coin
    public int distanceToCoin(Node coin, GetOutState state) {
    	Node start = state.currentNode();
    	Node end = coin;
    	List<Node> path = Paths.shortestPath(start, end);
    	int distance = 0;
    	for( int i = 0; i < path.size()-1; i++) {
    		Node next = path.get(i+1);
    		Node current = path.get(i);
    		distance = distance + current.getEdge(next).length();
    	}
    	return distance;
    }
    
    //moves Max to a certain coin
    public void goToCoins(Node coin, GetOutState state){
    	Node start = state.currentNode();
    	Node end = coin;
    	List<Node>coinPath = Paths.shortestPath(start, end);
    	for(int i = 1; i < coinPath.size(); i++) {
    		if(getShortestPath(state) < state.stepsLeft() - 31) {
            	state.moveTo(coinPath.get(i));	
    		}
        }    	
    }
    
    //gets the shortest path distance to the exit node
    public int getShortestPath(GetOutState state) {
    	Node start = state.currentNode();
    	Node end = state.getExit();
    	List<Node>shortPath = Paths.shortestPath(start, end);
    	int distance = 0;
    	for( int i = 0; i < shortPath.size()-1; i++) {
    		Node next = shortPath.get(i+1);
    		Node current = shortPath.get(i);
    		distance = distance + current.getEdge(next).length();
    	}
    	return distance;
    }
}











