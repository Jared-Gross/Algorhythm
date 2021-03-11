#include <iostream>
#include <stdio.h>
#include <string>
#include <dirent.h>
#include <dirent.h>
#include <sstream>
#include <vector>
#include <time.h>

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
*/
const string MUSIC_DIRECTORY = "./Piano Samples/";
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
            list_directory2.push_back(path + file_name);
        }
    }
    return list_directory2;
}

void combine_audio_files(vector<string> files, string output_filename)
{
    string file_names_string = "";
    for (string &file_name : files)
        file_names_string.append(" \"" + file_name + "\" ");
    // NEED LENGTH OF AUDIO FILE
    // NEED TO SHRING THE AUDIO FILE LENGTH BY 1,2,4,8,16,32
    // SAVE THOSE SHRUNKEN AUDIO FILES TO A TEMPERARY Directory
    // GET ALL PATHS TO THE NEW SHORTEND FILES
    // COMBINE ALL SHORTEND FILES INTO ONE
    // sox tracks\5_7.mp3 ntracks\05_7.mp3 reverse trim 0.195 reverse

    string command_string = "cat" + file_names_string + "| mp3cat - - > \"" + output_filename + "\"";
    // char *command = &(command_string[0]);
    popen(command_string.c_str(), "r");
    // popen(command, "r");
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
    vector<string> list_directory = list_dir("./Piano Samples/");
    for (string &path : list_directory)
        cout << path << endl;
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
    int index = 0;
    // combine_audio_files(files_to_compile, "yteaa.mp3");
    string ls = get_audio_file_length("sox \"./Piano Samples/A1.mp3\" -n stat");
    cout << ls;
    return 0;
}