#pragma once
#include <string>
#include <vector>
#include <random>

struct Location
{
	std::string mName;
	double mLatitude;
	double mLongitude;
};

struct Population
{
	std::vector<std::vector<int>> mMembers;
};

std::vector<Location> parseLocation(const char* file);
std::vector<std::vector<int>> initPop(std::mt19937& rand, size_t size, int popSize);
void outPutFile(std::fstream& outFile, int gen, std::vector<std::vector<int>>& population, std::vector<std::pair<int,double>> fitness, std::vector<std::pair<int, int>> selectionList );

double haversineDist(Location& loc1, Location& loc2);
std::vector<std::pair<int,double>> calcFitness(std::vector<std::vector<int>>& population, std::vector<Location> locations);
std::vector<double> genProbabilities(std::vector<std::pair<int,double>> fitness);
std::vector<std::pair<int, int>> selection(std::vector<std::pair<int,double>>& fitness, std::mt19937& rand);
int selectParent(std::vector<double> prob, std::mt19937& rand);

std::vector<int> mergePopulations(std::vector<int>& parentA, std::vector<int>& parentB, int crossIndex);
std::vector<std::vector<int>> crossover(std::vector<std::pair<int, int>>& parents, std::vector<std::vector<int>>& population,
                                        std::mt19937& rand, int mutationChance );

void finalOut(std::fstream& outFile, std::vector<std::vector<int>>& population, std::vector<std::pair<int,double>>& fitness, std::vector<Location>& loc);
