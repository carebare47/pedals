#include "raspy_host.h"

void init_timers(void){
	last_time_guitar = std::chrono::high_resolution_clock::now();
	last_time_connecting = std::chrono::high_resolution_clock::now();
	last_time_midi = std::chrono::high_resolution_clock::now();
	connection_time = std::chrono::high_resolution_clock::now();
	connection_time_boss = std::chrono::high_resolution_clock::now();
}

int main(int argc, char **argv)
{

	if ( !display.init(OLED_I2C_RESET,OLED_OLED_I2C_128x32) )
		exit(EXIT_FAILURE);
	
	init_timers();
	
	display.begin();
	
	while (true) {		
		update_display();
		display.display();
		usleep(100*1000);
	}
	display.close();

}

void update_display(void){
	bool alsa_route_established;
        bool boss_detected;
	bool bool_waiting_for_midi = false;
	std::string midi_devices = exec("aconnect -l");
	display.clearDisplay();
	
	if (midi_devices.find(ACONNECT_MIDI_SEARCH_TERM_) == std::string::npos){
		waiting_for_midi();
		bool_waiting_for_midi = true;
	} else {
		show_text(76, 24, &MIDI_TEXT_[0]);
	}

	if (midi_devices.find(ACONNECT_GUITAR_SEARCH_TERM_) == std::string::npos){
		waiting_for_guitar();
	} else {
		show_guitar(0,0);
	}

	boss_detected = (midi_devices.find(ACONNECT_BOSS_SEARCH_TERM_) == std::string::npos) ? false : true;

	if (midi_devices.find(ACONNECT_CONNECTED_SEARCH_TERM_) == std::string::npos){
		alsa_route_established = false;
		if (!bool_waiting_for_midi){
			wait_for_connecting();
		}
	} else {
		alsa_route_established = true;
		std::string T2 = "CONNECTED!";		
		show_text(64, 8, &T2[0]);
	}
	
	if (!alsa_route_established && connection_timer(6000)){
		usleep(2*1000*1000);
		int iGuitar = get_device_number(ACONNECT_GUITAR_SEARCH_TERM_);
		int iMidi = get_device_number(ACONNECT_MIDI_SEARCH_TERM_);
		if ((iGuitar > 99) || (iMidi > 99)){
			connection_time = std::chrono::system_clock::from_time_t(0);
		} else {
			connect(iGuitar, iMidi);
		}
	}
/*
	if (boss_detected && ){
		int iBoss = get_device_number(ACONNECT_BOSS_SEARCH_TERM_);
		int iMidi = get_device_number(ACONNECT_MIDI_SEARCH_TERM_);
		std::string boss_connection_search_string = "aconnect -l | grep \"Connected From\" | grep \"" +
							std::to_string(iMidi) + "\" | grep \"" +
							std::to_string(iBoss) + "\" | wc -l";

		std::string resp = exec(&boss_connection_search_string[0]);
		std::string::size_type sz;   // alias of size_t
		bool boss_connected;
		try{
			boss_connected = (std::stoi(resp, &sz) > 0) ? true : false;
		}
		catch (const std::exception& e){
			        std::cout << " a standard exception was caught, with message '"
	                  << e.what() << "'\n";
			boss_connected = false;
		}
	}

	if (boss_detected && !boss_connected && connection_timer_boss(6000)){
		std::cout << "connecting boss...\n";
		usleep(2*1000*1000);
		int iBoss = get_device_number(ACONNECT_BOSS_SEARCH_TERM_);
		int iMidi = get_device_number(ACONNECT_MIDI_SEARCH_TERM_);
		if ((iBoss  > 99) || (iMidi > 99)){
			std::cout << "boss error: boss: " << iBoss << " MIDI: " << iMidi << "\n";
			connection_time_boss = std::chrono::system_clock::from_time_t(0);
		} else {
			connect(iBoss, iMidi);
		}
	}
	*/
	display.display();
}

void show_guitar(int x, int y){
	display.drawBitmap(x,y,guitar,32,32,1);
}

void show_text(int x, int y, char* text_string){
	display.setTextSize(1);
	display.setTextColor(WHITE);
	display.setCursor(x, y);
	display.print(text_string);
}

std::string exec(const char* cmd) {
    char buffer[128];
    std::string result = "";
    FILE* pipe = popen(cmd, "r");
    if (!pipe) throw std::runtime_error("popen() failed!");
    try {
        while (fgets(buffer, sizeof buffer, pipe) != NULL) {
            result += buffer;
        }
    } catch (...) {
        pclose(pipe);
        throw;
    }
    pclose(pipe);
    return result;
}

void wait_for_connecting(void){
	std::string waiting_ = "connecting\n";
	std::chrono::duration<double, std::milli> time_span = std::chrono::high_resolution_clock::now() - last_time_connecting;
	if (time_span.count() > dot_animation_timer_ms){
		last_time_connecting = std::chrono::high_resolution_clock::now();
		loop_connecting++;
	}
	if (loop_connecting == 5)
		loop_connecting = 1;
	for (int i=1; i<(loop_connecting+1); i++){
		waiting_ = waiting_ + ".";
	}
	waiting_ = waiting_ + "\n";
	show_text(64, 8, &waiting_[0]);
}
void waiting_for_midi(void){
	std::string waiting_ = "waiting\n";
	std::string for_ = "for\n";
	std::string midi_ = "midi\n";
	show_text(64, 0, &waiting_[0]);
	show_text(64, 8, &for_[0]);
	show_text(64, 16, &midi_[0]);
	std::chrono::duration<double, std::milli> time_span = std::chrono::high_resolution_clock::now() - last_time_midi;
	if (time_span.count() > dot_animation_timer_ms){
		last_time_midi = std::chrono::high_resolution_clock::now();
		loop_midi++;
	}
	if (loop_midi == 5)
		loop_midi = 1;
	waiting_ = "";
	for (int i=1; i<(loop_midi+1); i++){
		waiting_ = waiting_ + ".";
	}
	waiting_ = waiting_ + "\n";
	show_text(64, 24, &waiting_[0]);
}

void waiting_for_guitar(void){
	std::string waiting = "waiting\nfor\nguitar\n";
	show_text(0, 0, &waiting[0]);
	std::chrono::duration<double, std::milli> time_span = std::chrono::high_resolution_clock::now() - last_time_guitar;
	if (time_span.count() > dot_animation_timer_ms){
		last_time_guitar = std::chrono::high_resolution_clock::now();
		loop_guitar++;
	}
	if (loop_guitar == 5)
		loop_guitar = 1;
	waiting = "";
	for (int i=1; i<(loop_guitar+1); i++){
		waiting = waiting + ".";
	}
	waiting = waiting + "\n";
	show_text(0, 24, &waiting[0]);
}

int get_device_number(std::string search_term){
	std::string::size_type sz;   // alias of size_t
	std::string search_string = "aconnect -l | grep \"" + search_term + "\" | grep \"client\" | awk '{print $2}' | sed -r 's/://g'";
	std::string resp = exec(&search_string[0]);
	std::cout << resp << "\n";
	int midi_port_number = 99999;
	try{
		midi_port_number = std::stoi(resp, &sz);
	}
	catch (const std::exception& e){
		        std::cout << " a standard exception was caught, with message '"
                  << e.what() << "'\n";
	}
	return midi_port_number;
}
void connect(int sender, int reciever){
	
	std::string cmd = std::string("aconnect ") + std::to_string(sender) + std::string(" ") + std::to_string(reciever) + "\n";
	std::cout << cmd;
	std::string output = exec(&cmd[0]);
	std::cout << output << "\n";
}

bool connection_timer(int timer_ms){
	std::chrono::duration<double, std::milli> time_span = std::chrono::high_resolution_clock::now() - connection_time;

	if (time_span.count() > timer_ms){
		connection_time = std::chrono::high_resolution_clock::now();
		return true;
	} else {
		return false;
	}
}

bool connection_timer_boss(int timer_ms){
	std::chrono::duration<double, std::milli> time_span = std::chrono::high_resolution_clock::now() - connection_time_boss;

	if (time_span.count() > timer_ms){
		connection_time_boss = std::chrono::high_resolution_clock::now();
		return true;
	} else {
		return false;
	}
}

