#include <iostream>
#include <random>
#include "TSP.h"
#include <fstream>
#include <algorithm>
#include <sstream>
#include <string>


/*This program is to use a genetic algorithm to solve a traveling sales
The arguments are as follows

    std::fstream inputFile(argv[1]); This should be path to the file in the folder locations.txt (make sure it is the whole or relative path)
    auto popSize     = atoi(argv[2]); This is the inital population size :: 10 is a good value
    auto generations = atoi(argv[3]); This is the number of generations to run the algorithm for. try 10
    auto mutationsChance   = atoi(argv[4]); This is the percent chance of a mutation occuring (0-100) %.  try 30
    auto random seed = atoi(argv[5]); This the seed for the random number generator pick whatever you want. try 40
 

 The resaults of the algorithm are written to log.txt
 */
int main(int argc, const char* argv[])
{
    // parse the command line argument

    
    auto generation = 0 ;
    std::mt19937 randGen(atoi(argv[5]));
    auto locations = parseLocation(argv[1]);
    auto population = initPop(randGen, locations.size(), atoi(argv[2]));
    
    // output inital population
    std::fstream outFile(argv[6], std::fstream::out);
    outFile << "INITIAL POPULATION:" << std::endl;
    for (auto& list : population)
    {
        for (auto& element : list)
        {
            outFile << element  ;
            if (element != list.back())
            {
                outFile << ",";
            }
        }
        outFile << std::endl;
    }
    
   
    while (generation < atoi(argv[3]))
    {
        generation++ ;
        auto fitness = calcFitness(population, locations);
        
        auto parentPairs = selection(fitness, randGen);
        
        population = crossover(parentPairs, population, randGen, atoi(argv[4]));
        
        outPutFile(outFile, generation, population, fitness, parentPairs);
    }
    
    auto fitness = calcFitness(population, locations);
    finalOut(outFile, population, fitness, locations);
    
    
	return 0;
}

// print out the last fitness and the solution
void finalOut(std::fstream& outFile, std::vector<std::vector<int>>& population, std::vector<std::pair<int,double>>& fitness, std::vector<Location>& loc)
{
    
    outFile <<"FITNESS:" << std::endl;
    for (auto& pop: fitness)
    {
        outFile << pop.first << ":" << pop.second ;
        outFile << std::endl;
    }
    
    outFile << "SOLUTION:" << std::endl;
    std::cout << "SOLUTION:" << std::endl;
    std::sort(fitness.begin(), fitness.end(),
              [](std::pair<int,double>& a, std::pair<int,double>& b) { return a.second < b.second;});
    for ( auto& bestPop : population[fitness[0].first])
    {
        outFile << loc[bestPop].mName << std::endl;
        std::cout << loc[bestPop].mName << std::endl;
    }
    
    outFile << loc[0].mName << std::endl;
    std::cout << loc[0].mName << std::endl;
    outFile << "DISTANCE: " << fitness[0].second <<  " miles";
    std::cout << "DISTANCE: " << fitness[0].second <<  " miles" << std::endl;

    
    
    
}

//preforms the crossover and the creation of another generation
std::vector<std::vector<int>> crossover(std::vector<std::pair<int, int>>& parents, std::vector<std::vector<int>>& population,
                                        std::mt19937& rand, int mutationChance )
{
    
    std::vector<std::vector<int>> newPopulation;
    
    // lambda function for handling the cross over
    // orinially had it seperated into mutliple functions but the random order got out of control
    auto merging = [&newPopulation, &population, &rand, &mutationChance]
    (std::pair<int, int>& a)
    {
        std::vector<int> parentA, parentB;
        std::uniform_int_distribution<int> crossIndexGen(1,static_cast<int>(population[0].size()-2));
        auto crossIndex = crossIndexGen(rand);
        std::uniform_int_distribution<int> parentGen(0,1);
        auto value = parentGen(rand);
        std::uniform_real_distribution<double> mutationGen(0,1);
        double mutate = mutationGen(rand);
       
        // select the parents
        if ( value == 1)
        {
            parentA = population[a.first];
            parentB = population[a.second];
        }
        else
        {
            parentA = population[a.second];
            parentB = population[a.first];
        }
        
        // merge parents
        auto element = mergePopulations(parentA, parentB, crossIndex);
        
        // handle the mutation
        if ( mutate <= static_cast<double>(mutationChance)/100.0)
        {
            std::uniform_int_distribution<int> indexGen(1,static_cast<int>(population[0].size())-1);

            std::swap(element[indexGen(rand)], element[indexGen(rand)]);
        }
        
        return element;
    };
    

    std::transform(parents.begin(), parents.end(), std::back_inserter(newPopulation),merging);

    
    return newPopulation;
}



// this handle the cross over element
std::vector<int> mergePopulations(std::vector<int>& parentA, std::vector<int>& parentB, int crossIndex)
{
    
    std::vector<int> retVal;
    // copy the front part
    std::copy_n(parentA.begin(), crossIndex+1 ,std::back_inserter(retVal));
    
    std::copy_if(parentB.begin(), parentB.end(), std::back_inserter(retVal),
                 [&retVal](int a){
                     return (std::find(retVal.begin(), retVal.end(), a) == retVal.end());
                 });
    
    return retVal;
}


// top level function for creating parents list
std::vector<std::pair<int, int>> selection(std::vector<std::pair<int,double>>& fitness, std::mt19937& rand)
{
    std::vector<std::pair<int, int>> selectionList(fitness.size());
    auto probList = genProbabilities(fitness);
    std::generate(selectionList.begin(), selectionList.end(),
                  [&probList, &rand](){ return std::make_pair(selectParent(probList, rand), selectParent(probList, rand));});
    
    return selectionList;
}

// low level function for selecting a parent
int selectParent(std::vector<double> prob, std::mt19937& rand)
{
    std::uniform_real_distribution<double> dis(0,1);
    auto value = dis(rand);
    double sum = 0 ;
    for (int i = 0 ; i < prob.size() ; i++)
    {
        sum += prob[i];
        if (sum >= value)
        {
            return i ;
        }
    }
    return 0; //should never get to this
}

// low level function for generating the probabilities based off the fitness function
std::vector<double> genProbabilities(std::vector<std::pair<int,double>> fitness)
{
    std::vector<double> probabilities(fitness.size());
    
    // sort the fitness
    std::sort(fitness.begin(), fitness.end(),
              [](std::pair<int,double>& a, std::pair<int,double>& b) { return a.second < b.second;});
    
    // generate probabiilities
    std::generate(probabilities.begin(), probabilities.end(), [&fitness]() { return 1.0/fitness.size();});
    
    // multiple the top fitest by 6
    probabilities[fitness[0].first] *= 6.0 ;
    probabilities[fitness[1].first] *= 6.0 ;
    
    // multiply the remaing of the top half by 3.0
    std::for_each(fitness.begin()+2, fitness.begin()+((fitness.size()/2)),
                  [&probabilities](std::pair<int,double>& a) { probabilities[a.first] *= 3.0;});
    
    // normalize probabilities
    auto totalProb = std::accumulate(probabilities.begin(), probabilities.end(), 0.0, [](const double& a, const double& b) {return a+b;});
    std::for_each(probabilities.begin(), probabilities.end(), [&totalProb](double& a){ a /= totalProb;});
    
    
    return probabilities;
    
    
}

// high level function for generating the fitness level of the populations
std::vector<std::pair<int,double>> calcFitness(std::vector<std::vector<int>>& population, std::vector<Location> locations)
{
    std::vector<std::pair<int,double>> retVal;
    
    int i = 0;
    std::transform(population.begin(), population.end(), std::back_inserter(retVal),
                   [&locations, &i](const std::vector<int>& list) { std::vector<double> distList;
                       std::adjacent_difference(list.begin(), list.end(), std::back_inserter(distList), [&locations](const int a, const int b){ return haversineDist(locations[a], locations[b]);} );
                       distList.push_back(haversineDist(locations[list.back()], locations[0]));
                       auto distTotal = std::accumulate(distList.begin(), distList.end(), 0.0, [](const double& a, const double& b) {return a+b;});
                       return std::make_pair(i++,distTotal);
                        });
    
    return retVal;
}

// low level function for calculating the distence between two GPS coordinates
double haversineDist(Location& loc1, Location& loc2)
{
    double dlon = (loc2.mLongitude - loc1.mLongitude)*0.0174533;

    double dlat = (loc2.mLatitude - loc1.mLatitude)*0.0174533;
    
    double a = pow(sin((dlat)/2),2) + cos(loc1.mLatitude*0.0174533)*cos(loc2.mLatitude*0.0174533)*pow(sin((dlon)/2),2);
    double c =  2* atan2(sqrt(a), sqrt(1-a));
    double distence = 3961*c ;
    
    return distence;
}

// high level function for outputting the information
void outPutFile(std::fstream& outFile, int gen, std::vector<std::vector<int>>& population, std::vector<std::pair<int,double>> fitness, std::vector<std::pair<int, int>> selectionList )
{
//    std::fstream outFile("log.txt", std::fstream::out);
    
    
    outFile <<"FITNESS:" << std::endl;
    for (auto& pop: fitness)
    {
        outFile << pop.first << ":" << pop.second ;
        outFile << std::endl;
    }
    
    outFile << "SELECTED PAIRS:" << std::endl;
    for (auto& pair : selectionList)
    {
        outFile << "(" << pair.first << "," << pair.second << ")" << std::endl;
    }
    
    outFile << "GENERATION: " << gen << std::endl;
    for (auto& list : population)
    {
        for (auto& element : list)
        {
            outFile << element  ;
            if (element != list.back())
            {
                outFile << ",";
            }
        }
        outFile << std::endl;
    }
}



// high level function for initalizing the population
std::vector<std::vector<int>> initPop(std::mt19937& rand, size_t size, int popSize)
{
    
    // generate the ordered population
    std::vector<std::vector<int>> retVal(popSize);
    std::generate(retVal.begin(), retVal.end(),[&size, &rand]() { int i = 0;
        std::vector<int> v(size);
        std::generate(v.begin(), v.end(), [&i]() { return i++; });
        shuffle(v.begin()+1,v.end(),rand);
        return v;}) ;
    
    return retVal;
}

//high level function for parsing the location file
std::vector<Location> parseLocation(const char* file)
{
    std::fstream inFile(file);
    std::string line,element;
    std::string subString;
    std::vector<Location> retValue;
    std::vector<std::string> parseValues;
    
    while ( !inFile.eof())
    {
        std::getline(inFile,line);
        std::getline(inFile,line);
        std::getline(inFile,line);
        std::stringstream ss(line);

        while (std::getline(ss,element,','))
        {
            parseValues.push_back(element);
//            std::cout << element << std::endl;
        }
        
        Location loc = {parseValues[0],stod(parseValues[1]),stod(parseValues[2])};
        retValue.push_back(loc);
        parseValues.clear();
//        parseValues.empty();
        
    }
    return retValue;
    
}
