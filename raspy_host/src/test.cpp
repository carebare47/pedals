#include <iostream>
#include <sstream>
#include <stdexcept>
#include <stdio.h>
#include <string>
#include <ctime>
#include <chrono>


int main(int argc, char **argv)
{
	int sender = 16;
	int reciever = 20;
	int iGuitar = 3;
	int iMidi = 4;
	std::string search_term = "BOSS_RC";
	std::cout << "\n\n";
	std::string cmd = std::string("aconnect ") + std::to_string(sender) + std::string(" ") + std::to_string(reciever) + "\n";
	std::string search_string = "aconnect -l | grep \"" + search_term + "\" | grep \"client\" | awk '{print $2}' | sed -r 's/://g'";
	std::string boss_connection_search_string = "aconnect -l | grep \"Connected From\" | grep \"" + std::to_string(iMidi) + "\" | grep \"" + std::to_string(iGuitar) + "\" | wc -l";
	std::cout << cmd << "\n\n";
	std::cout << boss_connection_search_string << "\n\n";
	std::cout << search_string << "\n\n";


}
