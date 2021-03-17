#include <iostream>
#include <stdio.h>
#include <string>
#include <dirent.h>
#include <dirent.h>
#include <sstream>
#include <vector>
#include "nlohmann/json.hpp"
#include <time.h>
#include <iterator>
#include <algorithm>
#include <fstream>
#include <filesystem>
#ifdef _WIN32
#include <filesystem>
#include "process.h"
#include <windows.h>
#include <limits.h>
#include <direct.h>
#elif _WIN64
#include <filesystem>
#include "process.h"
#include <windows.h>
#include <limits.h>
#include <direct.h>
#elif __linux__
#include <unistd.h>
#endif
using namespace std;
using json = nlohmann::json;
const string MUSIC_DIRECTORY = "./Piano Samples/";

string CWD = "";

string platform()
{
#ifdef _WIN32
    return "Windows";
#elif _WIN64
    return "Windows";
#elif __APPLE__ || __MACH__
    return "Mac";
#elif __linux__
    return "Linux";
#elif __FreeBSD__
    return "FreeBSD";
#elif __unix || __unix__
    return "Unix";
#else
    return "Other";
#endif
}
#ifdef _WIN32
string getCurrentDir()
{
    char buff[MAX_PATH];
    GetModuleFileName(NULL, buff, MAX_PATH);
    string::size_type position = string(buff).find_last_of("\\/");
    return string(buff).substr(0, position);
}
#elif _WIN64
string getCurrentDir()
{
    char buff[MAX_PATH];
    GetModuleFileName(NULL, buff, MAX_PATH);
    string::size_type position = string(buff).find_last_of("\\/");
    return string(buff).substr(0, position);
}
#endif

void combine_audio_files(vector<string> notes, vector<double> note_types, string output_filename)
{
    system(("mkdir \"" + CWD + "/Process\"").c_str());
    int index = 0;
    ofstream list_file;
    list_file.open("Process/list.txt");
    for (string &file_name : notes)
    {
        string s_index = to_string(index);
        string trim_ammount = to_string(note_types[index]);
        list_file << "file '" << s_index + ".mp3'\n";
        system(("ffmpeg -t " + trim_ammount + " -i \"" + file_name + "\" -acodec copy \"" + CWD + "/Process/" + s_index + ".mp3\"").c_str());
        index++;
    }
    list_file.close();
    string command_string = "ffmpeg -f concat -i \"" + CWD + "/Process/list.txt\" -c copy \"" + CWD + "/Music/" + output_filename + "\"";
    system(command_string.c_str());
    if (platform() == "Windows")
        system(("rd /s /q \"" + CWD + "/Process/\"").c_str());
    else if (platform() == "Linux")
        system(("rm -rf \"" + CWD + "/Process/\"").c_str());
}
string get_audio_file_length(string command)
{
    char buffer[128];
    string result = "";
    // Open pipe to file
    FILE *pipe = popen(command.c_str(), "r");
    if (!pipe)
        return "popen failed!";

    // read till end of process:
    while (!feof(pipe))
    {
        // use buffer to read and add to result
        if (fgets(buffer, 128, pipe) != NULL)
            result += buffer;
    }

    pclose(pipe);
    return result;
}
bool compareFunction(string a, string b) { return a < b; }

int main(int argc, const char *argv[])
{
    vector<string> list_directory;
    vector<string> files_to_compile;
    vector<int> note_indexes;
    vector<int> note_types_values;
    vector<double> trim_note_audio_values;
    vector<string> note_audio_values;
    int index = 0;
#if _WIN64
    CWD = getCurrentDir();
#elif _WIN32
    CWD = getCurrentDir();
#elif __linux__
    CWD = get_current_dir_name();
#endif

    replace(CWD.begin(), CWD.end(), '\\', '/'); // replace all '\\' to '/'
//     GET ALL KEYS
    ifstream file1(CWD + "/keys.json");
    json KEYS_JSON;
    file1 >> KEYS_JSON;
    for (json &key : KEYS_JSON[0]["keys"])
        list_directory.push_back((CWD + "/Piano Samples/" + key.get<string>() + ".mp3").c_str());
//     GET ALL KEY DURATIONS
    ifstream file2(CWD + "/Key_Durations.json");
    json KEYS_DURATION_JSON;
    file2 >> KEYS_DURATION_JSON;
    for (json &key : KEYS_DURATION_JSON[0]["Key_Durations"])
        note_audio_values.push_back(key.get<string>().c_str());
    
    
    stringstream ss_notes(argv[1]);
    for (int i; ss_notes >> i;)
    {
        note_indexes.push_back(i);
        if (ss_notes.peek() == ',')
            ss_notes.ignore();
    }
    stringstream ss_types_value(argv[2]);
    for (int i; ss_types_value >> i;)
    {
        note_types_values.push_back(i);
        if (ss_types_value.peek() == ',')
            ss_types_value.ignore();
    }
    for (int i = 0; i < note_indexes.size(); i++)
        files_to_compile.push_back(list_directory[note_indexes[i]]);
    for (string &duration : note_audio_values)
    {
//         string length = get_audio_file_length("ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \"" + file_name + "\"");
        double audio_length = ::atof(duration.c_str());
        trim_note_audio_values.push_back(audio_length / note_types_values[index]);
        index++;
    }
    combine_audio_files(files_to_compile, trim_note_audio_values, argv[3]);
    return 0;
}
