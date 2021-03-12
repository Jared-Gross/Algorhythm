#include <iostream>
#include <stdio.h>
#include <string>
#include <dirent.h>
#include <dirent.h>
#include <sstream>
#include <vector>
#include <time.h>
#include <iterator>
#include <algorithm>
#include <fstream>
#include <filesystem>
#include <experimental/filesystem>
// if were on windows
// void include_libs(){
#ifdef _WIN32 || _WIN64
#include "process.h"
#include <windows.h>
#include <limits.h>
#include <direct.h>
#elif __linux__
// if were on linux
#include <unistd.h>
#endif
// }

// include_libs();
namespace fs = std::experimental::filesystem;
using namespace std;
/*
LINUX
mkdir -p /usr/local/src
cd /usr/local/src
git clone https://github.com/tomclegg/mp3cat
cd mp3cat
make install



sudo apt install sox
sudo apt-get install libsox-fmt-mp3

WINDOWS
install sox
https://www.videohelp.com/software?d=sox-14.4.0-libmad-libmp3lame.zip
copy and replace the contents to where ever you install sox to.

*/

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
// template <size_t N>
// void splitString(string (&arr)[N], string str)
// {
//     int n = 0;
//     istringstream iss(str);
//     for (auto it = istream_iterator<string>(iss); it != istream_iterator<string>() && n < N; ++it, ++n)
//         arr[n] = *it;
// }

void deleteDirectoryContents(const string &dir_path)
{
    for (const auto &entry : experimental::filesystem::directory_iterator(dir_path))
        experimental::filesystem::remove_all(entry.path());
}
#ifdef _WIN32
string getCurrentDir()
{
    char buff[MAX_PATH];
    GetModuleFileName(NULL, buff, MAX_PATH);
    string::size_type position = string(buff).find_last_of("\\/");
    return string(buff).substr(0, position);
}
#endif
vector<string> list_dir(const char *path)
{
    struct dirent *entry;
    DIR *dir = opendir(path);

    vector<string> list_directory;
    vector<string> list_directory2;

    if (dir == NULL)
        return list_directory;
    while ((entry = readdir(dir)) != NULL)
        list_directory.push_back(entry->d_name);
    closedir(dir);

    for (string &file_name : list_directory)
    {
        if (file_name != "." && file_name != "..")
        {
            replace(CWD.begin(), CWD.end(), '\\', '/'); // replace all 'x' to 'y'
            list_directory2.push_back(CWD + "/Piano Samples/" + file_name);
        }
    }
    return list_directory2;
}

void combine_audio_files(vector<string> notes, vector<double> note_types, string output_filename)
{
#ifdef _WIN32 || _WIN64
    _mkdir((CWD + "/Process").c_str());
#elif __linux__
    system(("mkdir \"" + CWD + "/Process\"").c_str());
#endif
    string file_names_string = "";
    int index = 0;
    for (string &file_name : notes)
    {
        string s_index = to_string(index);
        string trim_ammount = to_string(note_types[index]);
        // system(("sox \"" + file_name + "\" \"" + CWD + "/Process/" + s_index + ".mp3\"
        // reverse trim " + trim_ammount + " reverse").c_str());
        system(("ffmpeg -t " + trim_ammount + " -i \"" + file_name + "\" -acodec copy \"" + CWD + "/Process/" + s_index + ".mp3\"").c_str());
        file_names_string.append(" \"" + CWD + "/Process/" + s_index + ".mp3\" ");
        index++;
    }
    // NEED LENGTH OF AUDIO FILE
    // NEED TO SHRING THE AUDIO FILE LENGTH BY 1,2,4,8,16,32
    // SAVE THOSE SHRUNKEN AUDIO FILES TO A TEMPERARY Directory
    // GET ALL PATHS TO THE NEW SHORTEND FILES
    // COMBINE ALL SHORTEND FILES INTO ONE
    // sox tracks\5_7.mp3 ntracks\05_7.mp3 reverse trim 0.195 reverse
    // ffmpeg -t 30 -i inputfile.mp3 -acodec copy outputfile.mp3

    string command_string = "cat" + file_names_string + "| mp3cat - - > \"" + output_filename + "\"";
    popen(command_string.c_str(), "r");
    deleteDirectoryContents((CWD + "/Process").c_str());
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
int main()
{
#if _WIN64
    CWD = getCurrentDir();
#elif _WIN32
    CWD = getCurrentDir();
#elif __linux__
    CWD = get_current_dir_name();
#endif // _OM_NO_IOSTREAM

    vector<string> list_directory = list_dir("./Piano Samples/");
    vector<string> files_to_compile = {
        list_directory[1],
        list_directory[15],
        list_directory[22],
        list_directory[3],
        list_directory[10],
        list_directory[40],
        list_directory[32],
        list_directory[1],
        list_directory[15],
    };
    vector<double> note_types_value = {
        8,
        16,
        32,
        4,
        2,
        1,
        4,
        16,
        32};
    vector<double> trim_note_audio_values;
    int index = 0;
    for (string &file_name : files_to_compile)
    {
        string length = get_audio_file_length("ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \"" + file_name + "\"");
        double audio_length = ::atof(length.c_str());
        trim_note_audio_values.push_back(audio_length / note_types_value[index]);
        index++;
    }
    for (double &new_trim : trim_note_audio_values)
        cout << new_trim << endl;
    combine_audio_files(files_to_compile, trim_note_audio_values, "Music/output.mp3");
    return 0;
}
