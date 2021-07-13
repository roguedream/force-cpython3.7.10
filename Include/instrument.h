#ifndef Py_INSTRUMENT_H
#define Py_INSTRUMENT_H
#include <windows.h>
#include "Python.h"
#include <direct.h> // _getcwd
#include <stdlib.h> // free, perror
#include <stdio.h>  // printf
#include <string.h> // strlen
#include <sys/stat.h>   // stat
#include "instrument_flag.h"
#include "frameobject.h"
#include "opcode.h"

int flag_main_file = 0;
int core_main_file_flag = 0;
int core_exec_flag = 0;
int flag_control_mode = 0;
int current_lineno = 0;
char current_file[MAX_PATH];
// char *current_filename ="";
char current_frame[512]="";
int last_line_main = 0;
char last_file_name_main[MAX_PATH];
int flag_config_loaded = 0;
int flag_call_function_from_main = 0;
int flag_call_function_from_main_error = 0;
char current_func[512]="";
char name_main_file[MAX_PATH];
char main_folder[MAX_PATH];
char outlog[MAX_PATH];
char forklog_path[MAX_PATH];
char python_folder[MAX_PATH];
char pip_folder[MAX_PATH];
char fork_record_folder[MAX_PATH];
int flag_pyinstaller = 0;
int flag_cut_branch = 1;
int flag_iter = 0;
char memory_folder[MAX_PATH];
int flag_func_memory;

int executed_lines[30000] = { 0 };
int max_lineno = 0;
int loop_limit = 50;
int flag_in_loop = 0;
int jump_count[4096] = { 0 } ;
int flag_call_uninvoked_function = 0;

char object_dump_folder[MAX_PATH] = { 0 } ;

int flag_begin_log = 0;
int fork_log_num = 0;

int last_record_lineno = 0;


int flag_last_record_used = 0;
int fork_record_length = 0;

char current_import_module[256] = "";
char tmp_fake_object[512] = "";
DWORD pid;

int fork_counter = 0;
struct fork_record
{
    char filename[1024];
    int linenumber;
    int opcode;
    int oparg;
    int cond;
    /* data */
};

struct force_func{
    char func_name[256];
    int index;
};
struct force_func func_list[1000];

// struct func_obj{
//     PyObject *func;
//     PyObject *args;
//     PyObject *ret_val;
// };

// struct func_obj func_record[1000] ={NULL};

struct fork_record forkRecords[1000];



int log_flag = 0;

int cond_instru = 0;

PyObject *FakeObject_dict = NULL;

// int config[1024] = {
//     0
// };

// int linenocount[1024] = {
//     0
// };
// int lineno_status[1024][1024] = {
//     0
// };
// int configlinenocount[1024] = {
//     0
// };
// int instrulinenocount[1024] = {
//     0
// };
char obj_name[512]="";




PyObject *new_FakeObject_str(char *name){
    if(strstr(name,"FakeObject")){
        sprintf(tmp_fake_object,"%s",name);
    }
    else{
        sprintf(tmp_fake_object,"FakeObject_%s",name);
    }
    PyObject *tmp_new_FakeObject = PyUnicode_FromString(tmp_fake_object);
    // PyObject *tmp_attr_dict = PyDict_New();
    // int dict_flag = PyDict_SetItem(FakeObject_dict,tmp_new_FakeObject,tmp_attr_dict);
    // Py_XDECREF(tmp_new_FakeObject);
    //Py_XDECREF(tmp_attr_dict);
    return tmp_new_FakeObject;
}
int FakeObject_setattr(PyObject * FakeObject, PyObject * key_object, PyObject *value_object){
    PyObject *attr_dict = PyDict_GetItem(FakeObject_dict,FakeObject);
    int dict_flag = PyDict_SetItem(attr_dict,key_object,value_object);
    return dict_flag;
}
PyObject *FakeObject_getattr(PyObject * FakeObject, PyObject * key_object){
    PyObject *attr_dict = PyDict_GetItem(FakeObject_dict,FakeObject);
    PyObject *value_object = PyDict_GetItem(attr_dict,key_object);
    return value_object;
}



char *get_object_name(PyObject *obj, char *output){
    PyObject *s = PyObject_Str(obj);
	if (s == NULL) {
		return "unknown name";
	}
    if (PyBytes_Check(s)) {
       strcpy(output,PyBytes_AS_STRING(s));
    }
    else if (PyUnicode_Check(s)) {
        PyObject *t;
        t = PyUnicode_AsEncodedString(s, "utf-8", "backslashreplace");
		strcpy(output,PyBytes_AS_STRING(t));
    }
    //Py_XDECREF(s);
    return output;
}

PyObject *new_FakeObject(PyObject *name){
    get_object_name(name,obj_name);
    if(strstr(obj_name,"FakeObject")){
        sprintf(tmp_fake_object,"%s",obj_name);
    }
    else{
        sprintf(tmp_fake_object,"FakeObject_%s",obj_name);
    }
    PyObject *tmp_new_FakeObject = PyUnicode_FromString(tmp_fake_object);
    // PyObject *tmp_attr_dict = PyDict_New();
    // int dict_flag = PyDict_SetItem(FakeObject_dict,tmp_new_FakeObject,tmp_attr_dict);
    obj_name[0] = '\0';
    //Py_XDECREF(tmp_attr_dict);
    return tmp_new_FakeObject;
}

int is_FakeObject(PyObject * Object){
    get_object_name(Object,obj_name);
    if(strstr(obj_name,"FakeObject")){
        obj_name[0] = '\0';
        return 1;
    }
    else{
        obj_name[0] = '\0';
        return 0;
    }
}

wchar_t wcstring[2048];
wchar_t * charToWString(char* orig)
{
    size_t origsize = strlen(orig) + 1;
    size_t convertedChars = 0;
    mbstowcs_s(&convertedChars, wcstring, origsize, orig, _TRUNCATE);
    return wcstring;
}

size_t getline(char **lineptr, size_t *n, FILE *stream) {
    char *bufptr = NULL;
    char *p = bufptr;
    size_t size;
    int c;

    if (lineptr == NULL) {
        return -1;
    }
    if (stream == NULL) {
        return -1;
    }
    if (n == NULL) {
        return -1;
    }
    bufptr = *lineptr;
    size = *n;

    c = fgetc(stream);
    if (c == EOF) {
        return -1;
    }
    if (bufptr == NULL) {
        bufptr = malloc(128);
        if (bufptr == NULL) {
            return -1;
        }
        size = 128;
    }
    p = bufptr;
    while(c != EOF) {
        if ((p - bufptr) > (size - 1)) {
            size = size + 128;
            bufptr = realloc(bufptr, size);
            if (bufptr == NULL) {
                return -1;
            }
        }
        *p++ = c;
        if (c == '\n') {
            break;
        }
        c = fgetc(stream);
    }

    *p++ = '\0';
    *lineptr = bufptr;
    *n = size;

    return p - bufptr - 1;
}

char frame_file_name[MAX_PATH]="";
// char * get_file_name(PyFrameObject * f) {
//     strcpy(frame_file_name,get_object_name(f->f_code->co_filename));
//     return frame_file_name;
// }

// int check_main_folder(PyFrameObject * f) {
//     char * filepath = get_file_name(f);
//     if (strstr(filepath, main_folder)) {
//         return 1;
//     } else {
//         return 0;
//     }
// }

int init_fork_record(){
    FILE *fork_file = fopen(forklog_path,"w");
    if(fork_file == NULL){
        printf("[debug log] something with fork_log file in %s\n",forklog_path);
        return 0;
    }
    fclose(fork_file);
    int i = 0;
    for(i = 0; i<1000; i++){
        strcpy(forkRecords[i].filename,"\0");
        forkRecords[i].linenumber = -1;
        forkRecords[i].opcode = -1;
        forkRecords[i].oparg = -1;
        forkRecords[i].cond = -1;
    }
    return 1;
}

int fork(int merge_line){
    printf("[%lu debug log] fork() is called\n",pid);
    HANDLE process_handle;
    process_handle = GetCurrentProcess();
    // Sleep(1000);
    // srand((unsigned int)time(NULL));
    // int set1 = rand() % 90000 + 10000;
    // char buffer[20]="";
    // itoa(set1,buffer,10);
    // printf("[%lu debug log] rand value = %s\n", pid, buffer);
    //generate unique filename
    char filename_suffix[1024];
    sprintf(filename_suffix,"%lu",pid);
    char s[1024] ="";
    char *filename_prefix = "forcedExecutionConfig";
    char merge_prefix[1024]="";
    sprintf(merge_prefix,"MergeLine%d",merge_line);
    // char *filename_suffix = buffer;
    strcat(s,merge_prefix);
    strcat(s,filename_prefix);
    strcat(s,filename_suffix);
    char full_path[1024]="";
    strcat(full_path,fork_record_folder);
    strcat(full_path,s);
    printf("[%lu debug log] generated full path is %s\n",pid,full_path);


    FILE *fork_record_file = fopen(full_path,"w");
    int i = 0;

    printf("[%lu debug log] fork() filename is %s\n",pid,forkRecords[i].filename);
    struct fork_record reverse_forkRecords[1000];
    for(i = 0; i<1000; i++){
        strcpy(reverse_forkRecords[i].filename,"\0");
        reverse_forkRecords[i].linenumber = -1;
        reverse_forkRecords[i].opcode = -1;
        reverse_forkRecords[i].oparg = -1;
        reverse_forkRecords[i].cond = -1;
    }
    int flag = 0;
    i = 0;
    while(forkRecords[i].linenumber!=-1){
        // printf("[%lu debug log] in loop\n",pid);
        char original_filename[1024]="";
        char *ret = strstr(forkRecords[i].filename,"forcedExecutionConfig");
        if(ret){
            strncpy(original_filename, forkRecords[i].filename, strlen(forkRecords[i].filename) - strlen(ret));
        }
        else{
            strcpy(original_filename,forkRecords[i].filename);
        }
        strcpy(reverse_forkRecords[i].filename,original_filename);
        reverse_forkRecords[i].linenumber = forkRecords[i].linenumber;
        reverse_forkRecords[i].opcode = forkRecords[i].opcode;
        reverse_forkRecords[i].oparg = forkRecords[i].oparg;
        reverse_forkRecords[i].cond = forkRecords[i].cond;
        flag = i;
        i = i + 1;
    }
    if(reverse_forkRecords[flag].cond == 1){
        reverse_forkRecords[flag].cond = 0;
    }
    else{
        reverse_forkRecords[flag].cond = 1;
    }
    i = 0;
    printf("---------------------------------write to record file--------------------------------------------\n");
    while(reverse_forkRecords[i].linenumber!=-1){
        fprintf(stdout,"%s %d %d %d %d\n",reverse_forkRecords[i].filename,reverse_forkRecords[i].linenumber,reverse_forkRecords[i].opcode,reverse_forkRecords[i].oparg,reverse_forkRecords[i].cond);
        fprintf(fork_record_file,"%s %d %d %d %d\n",reverse_forkRecords[i].filename,reverse_forkRecords[i].linenumber,reverse_forkRecords[i].opcode,reverse_forkRecords[i].oparg,reverse_forkRecords[i].cond);
        i = i + 1;
    }
    printf("---------------------------------write to record file--------------------------------------------\n");
    // printf("[%lu debug log] before close file\n",pid);
    fclose(fork_record_file);



    PROCESS_INFORMATION ProcessInfo; //This is what we get as an [out] parameter
    STARTUPINFO StartupInfo; //This is an [in] parameter
    char cmdArgs[2048]="";
    strcat(cmdArgs," ");
    
    // printf("[%lu debug log] original target file is %s\n",pid,targetFile);

    // strcpy(targetFile,"D:\\cpython-3.9.2\\mal.py");//need to be removed later on !!!!!!!!!!!!!!!!!!!!!!!!!!

    strcat(cmdArgs,targetFile);
    strcat(cmdArgs,s);
    // printf("[%lu debug log] cmdArgs: %s\n",pid,cmdArgs);
    ZeroMemory(&StartupInfo, sizeof(StartupInfo));
    StartupInfo.cb = sizeof StartupInfo ; //Only compulsory field
    TCHAR szFileName[MAX_PATH];
    GetModuleFileName(NULL, szFileName, MAX_PATH);    
    if(CreateProcess(szFileName, cmdArgs, 
        NULL,NULL,FALSE,0,NULL,
        NULL,&StartupInfo,&ProcessInfo))
    {
        FILE * pFile2 = fopen(outlog, "a");
        fprintf(pFile2,"[%5lu]: fork() %lu in line:%d and merge line is %d\n",pid,ProcessInfo.dwProcessId,current_lineno,merge_line);
        fclose(pFile2);
        printf("[%lu debug log] we get a new process:  %lu\n",pid,ProcessInfo.dwProcessId);
        WaitForSingleObject( ProcessInfo.hProcess, INFINITE );
        // WaitForSingleObject( ProcessInfo.hProcess, 0 );
        CloseHandle(ProcessInfo.hThread);
        CloseHandle(ProcessInfo.hProcess);
        
        return 1;
    }  
    else
    {
        printf("[debug log] The process could not be started...\n");
        return -1;
    }
    
}
//if the record does not exist, we add and return -1 means we need to fork here
//else we return the cond for the corresponding record

int write_one_fork_record_mem(char *filename,int linenumber, int opcode, int oparg, int cond){
    int i = 0;
    // printf("[debug log] the input file name is %s\n",filename);
    char original_filename[1024]="";
    char *ret = strstr(filename,"forcedExecutionConfig");

    if(ret){
        strncpy(original_filename, filename, strlen(filename) - strlen(ret));
    }
    else{
        strcpy(original_filename,filename);
    }
    filename = original_filename;
    // printf("[debug log] filtered file name is %s\n",filename);
    // printf("[%lu debug log] the input record is: %s %d %d %d %d\n",pid,filename,linenumber,opcode,oparg,cond);
    while(forkRecords[i].linenumber!=-1){
        // printf("[debug log] current record is: %s %d %d %d\n",forkRecords[i].filename,forkRecords[i].linenumber,forkRecords[i].opcode,forkRecords[i].oparg);
        if( forkRecords[i].linenumber == linenumber && forkRecords[i].opcode == opcode && forkRecords[i].oparg == oparg ){
        // if(forkRecords[i].filename == filename && forkRecords[i].linenumber == linenumber && forkRecords[i].opcode == opcode && forkRecords[i].oparg == oparg ){
            // printf("[%lu debug log] we find the matched record\n",pid);
            fork_log_num = fork_log_num - 1;
            if(fork_log_num == 0){
                flag_begin_log = 1;
            }
            if(i == (fork_record_length - 1)){
                printf("last record is used\n");
                flag_last_record_used = 1;
            }
            return forkRecords[i].cond;
        }
        i = i + 1;
    }
    strcpy(forkRecords[i].filename,filename);
    forkRecords[i].linenumber = linenumber;
    forkRecords[i].opcode = opcode;
    forkRecords[i].oparg = oparg;
    forkRecords[i].cond = cond;
    return -1;
}
int read_fork_record(){
    if(strstr(forcedExcutionConfig,"no config")){
        printf("[%lu debug log]  first round execution: no config detected\n",pid);
        flag_begin_log = 1;
        return 0;
    }
    else{
        char fullpath[1024]="";
        strcat(fullpath,fork_record_folder);
        //to add
        char line[100]="";
        sprintf(line,"MergeLine%d",mergeline);
        // return 1;
        //
        strcat(fullpath,line);
        strcat(fullpath,forcedExcutionConfig);
        printf("[%lu debug log] we will read the config in %s\n",pid, fullpath);
        FILE *fork_record_file = fopen(fullpath,"r");
        if(fork_record_file == NULL){
            printf("[debug log] we cannot open fork record file in %s\n",fullpath);
            return -1;
        }
        else{
            char * line = NULL;
            size_t len = 0;
            ssize_t read;
            int i = 0;
            // printf("---------------------------------read from fork record-----------------------------------------\n");
            while ((read = getline( & line, & len, fork_record_file)) != -1) {
        // printf("[debug log] Retrieved line of length %zu:\n", read);
                // printf("[%lu debug log] the record we get is: %s", pid,line);
                char * pch;
                pch = strtok(line, " ");
                int offset = 0;
                char *tmp_filename;
                int tmp_linenumber;
                int tmp_opcode;
                int tmp_oparg;
                int tmp_cond;
                // i = 0;
                while (pch != NULL) {
                    if (offset == 0) {
                        tmp_filename = pch;
                    }
                    if (offset == 1) {
                        tmp_linenumber = atoi(pch);
                        last_record_lineno = tmp_linenumber;
                    }
                    if (offset == 2) {
                        tmp_opcode = atoi(pch);
                    }
                    if (offset == 3) {
                        tmp_oparg = atoi(pch);
                    }
                    if (offset == 4) {
                        tmp_cond = atoi(pch);
                    }
                    pch = strtok(NULL, " ");
                    offset = offset + 1;
                }
                write_one_fork_record_mem(tmp_filename,tmp_linenumber,tmp_opcode,tmp_oparg,tmp_cond);
                i = i + 1;
            }
            // printf("---------------------------------read from fork record-----------------------------------------\n");
            fork_log_num = i;
            fork_record_length = i;
            fclose(fork_record_file);
            return 1;
        }
    }
}

int dump_pair_disk(PyObject *name, PyObject *value){
    //printf("dump_pair_disk in\n");
    if(name == NULL || value == NULL){
        return 0;
    }
    char filename[MAX_PATH] = "";
    sprintf(filename,"%s%s-%lu-%d.txt",object_dump_folder,"var",pid,mergeline);
    FILE *tmpfile_dump_obj = fopen(filename,"a");
    fprintf(tmpfile_dump_obj,"-----------------------------------\n");
    PyObject_Print(name,tmpfile_dump_obj,0);
    fprintf(tmpfile_dump_obj,"\n");
    PyObject_Print(value,tmpfile_dump_obj,0);
    fprintf(tmpfile_dump_obj,"\n-----------------------------------\n");
    fclose(tmpfile_dump_obj);
    return 1;
}

// int dump_object_disk(PyObject *obj,char *name){
//     if(obj ==NULL){
//         return 0;
//     }
//     PyObject *key, *value;
//     Py_ssize_t pos = 0;
//     char filename[4096] = "";
//     sprintf(filename,"%s%s-%lu-%d.txt",object_dump_folder,name,pid,mergeline);

//     if(PyDict_Check(obj)){
//         PyDictObject *dict_obj = obj;
//         FILE *tmpfile_dump_obj = fopen(filename,"a");
//         while (PyDict_Next(dict_obj, &pos, &key, &value)) {
//             fprintf(tmpfile_dump_obj,"%s  :  %s\n",get_object_name(key),get_object_name(value)); 
//         }
//         fclose(tmpfile_dump_obj);
//     }
//     return 1;
// }

int load_configuration_file(char *path){
    pid = GetCurrentProcessId();
    FILE *fork_record_file = fopen(path,"r");
    if(fork_record_file == NULL){
        printf("[debug log] we cannot open config file in %s\n",path);
        return -1;
    }
    else{
        char * line = NULL;
        size_t len = 0;
        ssize_t read;
        int i = 0;
        int current_config_line = 0;
        while ((read = getline( & line, & len, fork_record_file)) != -1) {
            char * pch;
            pch = strtok(line, " ");
            int offset = 0;
            i = 0;
            while (pch != NULL) {
                if (offset == 1 && current_config_line == 0) {
                    int size = strlen(pch); //Total size of string
                    pch[size-1] = '\0';
                    strcpy(name_main_file,pch);
                    printf("name_main_file:%s\n",name_main_file);
                }
                if (offset == 1 && current_config_line == 1) {
                    int size = strlen(pch); //Total size of string
                    pch[size-1] = '\0';
                    strcpy(main_folder,pch);
                    printf("main_folder:%s\n",main_folder);
                }
                if (offset == 1 && current_config_line == 2) {
                    int size = strlen(pch); //Total size of string
                    pch[size-1] = '\0';
                    strcpy(outlog,pch);
                    printf("outlog:%s\n",outlog);
                }
                if (offset == 1 && current_config_line == 3) {
                    int size = strlen(pch); //Total size of string
                    pch[size-1] = '\0';
                    strcpy(forklog_path,pch);
                    printf("forklog_path:%s\n",forklog_path);
                }
                if (offset == 1 && current_config_line == 4) {
                    int size = strlen(pch); //Total size of string
                    pch[size-1] = '\0';
                    strcpy(python_folder,pch);
                    printf("python_folder:%s\n",python_folder);
                }
                if (offset == 1 && current_config_line == 5) {
                    int size = strlen(pch); //Total size of string
                    pch[size-1] = '\0';
                    strcpy(pip_folder,pch);
                    printf("pip_folder:%s\n",pip_folder);
                }
                if (offset == 1 && current_config_line == 6) {
                    int size = strlen(pch); //Total size of string
                    pch[size-1] = '\0';
                    strcpy(fork_record_folder,pch);
                    printf("fork_record_folder:%s\n",fork_record_folder);
                }
                if (offset == 1 && current_config_line == 7) {
                    flag_pyinstaller = atoi(pch);
                    printf("flag_pyinstaller:%d\n",flag_pyinstaller);
                }
                if (offset == 1 && current_config_line == 8) {
                    loop_limit = atoi(pch);
                    printf("loop_limit:%d\n",loop_limit);
                }
                if (offset == 1 && current_config_line == 9) {
                    flag_call_uninvoked_function = atoi(pch);
                    printf("flag_call_uninvoked_function:%d\n",flag_call_uninvoked_function);
                }
                if (offset == 1 && current_config_line == 10) {
                    flag_func_memory = atoi(pch);
                    printf("flag_func_memory:%d\n",flag_func_memory);
                }
                if (offset == 1 && current_config_line == 11) {
                    int size = strlen(pch); //Total size of string
                    pch[size-1] = '\0';
                    strcpy(memory_folder,pch);
                    printf("memory_folder:%s\n",memory_folder);
                }
                if (offset == 1 && current_config_line == 12) {
                    flag_cut_branch = atoi(pch);
                    printf("flag_cut_branch:%d\n",flag_cut_branch);
                }

                if (offset == 1 && current_config_line == 13) {
                    int size = strlen(pch); //Total size of string
                    pch[size-1] = '\0';
                    strcpy(object_dump_folder,pch);
                    printf("object_dump_folder:%s\n",object_dump_folder);
                }
                pch = strtok(NULL, " ");
                offset = offset + 1;
            }
            current_config_line = current_config_line + 1;
            i = i + 1;
        }
        // printf("---------------------------------read from fork record-----------------------------------------\n");
        fclose(fork_record_file);
        return 1;
    }
}

#include <stdbool.h>    // bool type
int is_target(char *filename){
    if(strstr(filename,python_folder)){
        //printf("this is in python folder\n");
        return 0;
    }
    else if (strstr(filename,pip_folder))
    {
        //printf("this is in pip folder\n");
        return 0;
    }
    else if (strstr(filename,"frozen importlib._bootstrap"))
    {
        //printf("this is in frozen importlib._bootstrap\n");
        return 0;
    }
    else if (strstr(filename,name_main_file))
    {
        //printf("%s - %s\n",filename,name_main_file);
        return 1;
    }
    else{
        return 0;
    }
    return 0;
}
int file_exists (char *filename) {
  struct stat   buffer;
  //printf("file exist of %s is to be checked\n",filename);
  if(stat (filename, &buffer) == 0){
    return 1;
  }
  else{
      return 0;
  }
}
void add_pip(){
    printf("[%lu debug log] we will add pip to our dependencies\n",pid);
    // PyObject *syspath = PySys_GetObject("path");
    // PyObject_Print(syspath,stdout,0);
    char py_sys_path[9999] = "";
    
    char* buffer;
    if ( (buffer = _getcwd( NULL, 0 )) == NULL ){
        perror( "_getcwd error" );
    }
    else{
        printf( "[%lu debug log] current working directory is: %s \n",pid, buffer);
    }
    strcat(py_sys_path,buffer);
    strcat(py_sys_path,";");

    strcat(py_sys_path,"C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python37\\python37.zip;");
    strcat(py_sys_path,"C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python37\\DLLs;");
    strcat(py_sys_path,"C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python37\\lib;");
    strcat(py_sys_path,"C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python37;");
    strcat(py_sys_path,"C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python37\\lib\\site-packages;");
    strcat(py_sys_path,"C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python37\\lib\\site-packages\\fastecdsa-2.1.6-py3.7-win-amd64.egg;");
    strcat(py_sys_path,"C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python37\\lib\\site-packages\\win32;");
    strcat(py_sys_path,"C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python37\\lib\\site-packages\\win32\\lib;");
    strcat(py_sys_path,"C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python37\\lib\\site-packages\\Pythonwin;");
    
    strcat(py_sys_path,python_folder);
    strcat(py_sys_path,";");

    strcat(py_sys_path,python_folder);
    strcat(py_sys_path,"DLLs");
    strcat(py_sys_path,";");

    strcat(py_sys_path,python_folder);
    strcat(py_sys_path,"PCbuild\\amd64\\python37.zip");
    strcat(py_sys_path,";");

    strcat(py_sys_path,python_folder);
    strcat(py_sys_path,"lib");
    strcat(py_sys_path,";");

    strcat(py_sys_path,python_folder);
    strcat(py_sys_path,"PCbuild\\amd64");
    strcat(py_sys_path,";");

    strcat(py_sys_path,python_folder);
    strcat(py_sys_path,"lib\\site-packages");
    strcat(py_sys_path,";");

    wchar_t *w_pypath = charToWString(py_sys_path);
    PySys_SetPath(w_pypath);
    printf("[%lu debug log]we have redirected path to %s\n",pid,py_sys_path);


}

void load_configuration(){
        pid = GetCurrentProcessId();
        printf(">>>>>> %5lu start() %d\n",pid,current_lineno);
        char cwd[MAX_PATH];
        if (getcwd(cwd, sizeof(cwd)) != NULL) {
            char log_full_path[8096]="";
            sprintf(log_full_path,"%s\\forceConfig.txt",cwd);
            printf("----------------------------------\n");
            printf("We are using configuration file from %s\n", log_full_path);
            int tmp_flag = load_configuration_file(log_full_path);
            add_pip();
            if(tmp_flag){
                printf("configuration succefully loaded\n");
            }
            else{
                printf("configuration loading failure\n");
            }
            printf("----------------------------------\n");
        } else {
            perror("getcwd() error");
        }
        flag_config_loaded = 1;
    
}
void branch_cut(){
    if(last_line_main > mergeline){
        char merge_filename[1024];
        sprintf(merge_filename,"%sMergeFile%d",fork_record_folder,mergeline);
        int file_exist = file_exists(merge_filename);
        if(flag_cut_branch == 1){
            printf("[%5lu debug log] we need to exit()\n",pid);
            FILE * pFile2 = fopen(outlog, "a");
            // if(pFile2 == NULL){
            //     printf("[%")
            // }
            fprintf(pFile2,"[%5lu] exit() in %d   mergeline is: %d\n",pid,last_line_main,mergeline);
            int lineno = 0;
            int search_lineno = 0;
            fprintf(pFile2,"[%5lu]: Coverage: ",pid);
            //char full_coverage[4096];
            while (lineno < 30000){
                if(executed_lines[lineno]){
                    search_lineno = lineno + 1;
                    while (executed_lines[search_lineno] && search_lineno < 30000){
                        search_lineno = search_lineno + 1;
                    }
                    if(lineno == (search_lineno - 1)){
                        fprintf(pFile2,"%d, ",lineno);
                    }
                    else{
                        fprintf(pFile2,"%d - %d, ",lineno,search_lineno-1);
                    }
                    lineno = search_lineno;
                }
                else{
                    lineno = lineno + 1;
                }
            }
            fprintf(pFile2,"\n");
            fclose(pFile2);
            exit(0);
        }
    }
}

void add_pyinstaller(){
    wchar_t cwd[1024];
    wchar_t *tmp_dir;
    tmp_dir = _Py_wgetcwd(cwd,1024);
    char *tmp_1;
    char *tmp_2;
    tmp_1 = Py_EncodeLocale(cwd,NULL);
    tmp_2 = Py_EncodeLocale(tmp_dir,NULL);
    // printf("%s %s\n",tmp_1,tmp_2);
    // printf("---------------------\n");
    char c_library_path[4096];
    memset(c_library_path, 0, 4096);
    // printf("aaaaaaaaaaaaaaaaaaaaaaaa\n");
    strcat(c_library_path,tmp_2);
    strcat(c_library_path,"\\base_library.zip;");
    strcat(c_library_path,tmp_2);
    strcat(c_library_path,"\\PYZ-00.pyz_extracted\\;");
    strcat(c_library_path,tmp_2);
    strcat(c_library_path,"\\");
    // printf("aaaaaaaaaaaaaaaaaaaaaaaa\n");
    printf("c_library_path: %s\n",c_library_path);
    const wchar_t *w_library_path = Py_DecodeLocale(c_library_path,NULL);
    PySys_SetPath(w_library_path);
    printf("[%lu debug log] pyinstaller extracted package detected, we use redirect path\n",pid);
}

char *get_opcode_name(int opcode){
    switch (opcode)
    {
    case POP_TOP:
        return "POP_TOP";
        break;
    case ROT_TWO:
        return "ROT_TWO";
        break;
    case ROT_THREE:
        return "ROT_THREE";
        break;
    case DUP_TOP:
        return "DUP_TOP";
        break;
    case DUP_TOP_TWO:
        return "DUP_TOP_TWO";
        break;
    case NOP:
        return "NOP";
        break;
    case UNARY_POSITIVE:
        return "UNARY_POSITIVE";
        break;
    case UNARY_NEGATIVE:
        return "UNARY_NEGATIVE";
        break;
    case UNARY_NOT:
        return "UNARY_NOT";
        break;
    case UNARY_INVERT:
        return "UNARY_INVERT";
        break;
    case BINARY_MATRIX_MULTIPLY:
        return "BINARY_MATRIX_MULTIPLY";
        break;
    case INPLACE_MATRIX_MULTIPLY:
        return "INPLACE_MATRIX_MULTIPLY";
        break;
    case BINARY_POWER:
        return "BINARY_POWER";
        break;
    case BINARY_MULTIPLY:
        return "BINARY_MULTIPLY";
        break;
    case BINARY_MODULO:
        return "BINARY_MODULO";
        break;
    case BINARY_ADD:
        return "BINARY_ADD";
        break;
    case BINARY_SUBTRACT:
        return "BINARY_SUBTRACT";
        break;
    case BINARY_SUBSCR:
        return "BINARY_SUBSCR";
        break;
    case BINARY_FLOOR_DIVIDE:
        return "BINARY_FLOOR_DIVIDE";
        break;
    case BINARY_TRUE_DIVIDE:
        return "BINARY_TRUE_DIVIDE";
        break;
    case INPLACE_FLOOR_DIVIDE:
        return "INPLACE_FLOOR_DIVIDE";
        break;
    case INPLACE_TRUE_DIVIDE:
        return "INPLACE_TRUE_DIVIDE";
        break;
    case GET_AITER:
        return "GET_AITER";
        break;
    case GET_ANEXT:
        return "GET_ANEXT";
        break;
    case BEFORE_ASYNC_WITH:
        return "BEFORE_ASYNC_WITH";
        break;
    case INPLACE_ADD:
        return "INPLACE_ADD";
        break;
    case INPLACE_SUBTRACT:
        return "INPLACE_SUBTRACT";
        break;
    case INPLACE_MULTIPLY:
        return "INPLACE_MULTIPLY";
        break;
    case INPLACE_MODULO:
        return "INPLACE_MODULO";
        break;
    case STORE_SUBSCR:
        return "STORE_SUBSCR";
        break;
    case DELETE_SUBSCR:
        return "DELETE_SUBSCR";
        break;
    case BINARY_LSHIFT:
        return "BINARY_LSHIFT";
        break;
    case BINARY_RSHIFT:
        return "BINARY_RSHIFT";
        break;
    case BINARY_AND:
        return "BINARY_AND";
        break;
    case BINARY_XOR:
        return "BINARY_XOR";
        break;
    case BINARY_OR:
        return "BINARY_OR";
        break;
    case INPLACE_POWER:
        return "INPLACE_POWER";
        break;
    case GET_ITER:
        return "GET_ITER";
        break;
    case GET_YIELD_FROM_ITER:
        return "GET_YIELD_FROM_ITER";
        break;
    case PRINT_EXPR:
        return "PRINT_EXPR";
        break;
    case LOAD_BUILD_CLASS:
        return "LOAD_BUILD_CLASS";
        break;
    case YIELD_FROM:
        return "YIELD_FROM";
        break;
    case GET_AWAITABLE:
        return "GET_AWAITABLE";
        break;
    case INPLACE_LSHIFT:
        return "INPLACE_LSHIFT";
        break;
    case INPLACE_RSHIFT:
        return "INPLACE_RSHIFT";
        break;
    case INPLACE_AND:
        return "INPLACE_AND";
        break;
    case INPLACE_XOR:
        return "INPLACE_XOR";
        break;
    case INPLACE_OR:
        return "INPLACE_OR";
        break;
    case BREAK_LOOP:
        return "BREAK_LOOP";
        break;
    case WITH_CLEANUP_START:
        return "WITH_CLEANUP_START";
        break;
    case WITH_CLEANUP_FINISH:
        return "WITH_CLEANUP_FINISH";
        break;
    case RETURN_VALUE:
        return "RETURN_VALUE";
        break;
    case IMPORT_STAR:
        return "IMPORT_STAR";
        break;
    case SETUP_ANNOTATIONS:
        return "SETUP_ANNOTATIONS";
        break;
    case YIELD_VALUE:
        return "YIELD_VALUE";
        break;
    case POP_BLOCK:
        return "POP_BLOCK";
        break;
    case END_FINALLY:
        return "END_FINALLY";
        break;
    case POP_EXCEPT:
        return "POP_EXCEPT";
        break;
    case STORE_NAME:
        return "STORE_NAME";
        break;
    case DELETE_NAME:
        return "DELETE_NAME";
        break;
    case UNPACK_SEQUENCE:
        return "UNPACK_SEQUENCE";
        break;
    case FOR_ITER:
        return "FOR_ITER";
        break;
    case UNPACK_EX:
        return "UNPACK_EX";
        break;
    case STORE_ATTR:
        return "STORE_ATTR";
        break;
    case DELETE_ATTR:
        return "DELETE_ATTR";
        break;
    case STORE_GLOBAL:
        return "STORE_GLOBAL";
        break;
    case DELETE_GLOBAL:
        return "DELETE_GLOBAL";
        break;
    case LOAD_CONST:
        return "LOAD_CONST";
        break;
    case LOAD_NAME:
        return "LOAD_NAME";
        break;
    case BUILD_TUPLE:
        return "BUILD_TUPLE";
        break;
    case BUILD_LIST:
        return "BUILD_LIST";
        break;
    case BUILD_SET:
        return "BUILD_SET";
        break;
    case BUILD_MAP:
        return "BUILD_MAP";
        break;
    case LOAD_ATTR:
        return "LOAD_ATTR";
        break;
    case COMPARE_OP:
        return "COMPARE_OP";
        break;
    case IMPORT_NAME:
        return "IMPORT_NAME";
        break;
    case IMPORT_FROM:
        return "IMPORT_FROM";
        break;
    case JUMP_FORWARD:
        return "JUMP_FORWARD";
        break;
    case JUMP_IF_FALSE_OR_POP:
        return "JUMP_IF_FALSE_OR_POP";
        break;
    case JUMP_IF_TRUE_OR_POP:
        return "JUMP_IF_TRUE_OR_POP";
        break;
    case JUMP_ABSOLUTE:
        return "JUMP_ABSOLUTE";
        break;
    case POP_JUMP_IF_FALSE:
        return "POP_JUMP_IF_FALSE";
        break;
    case POP_JUMP_IF_TRUE:
        return "POP_JUMP_IF_TRUE";
        break;
    case LOAD_GLOBAL:
        return "LOAD_GLOBAL";
        break;
    case CONTINUE_LOOP:
        return "CONTINUE_LOOP";
        break;
    case SETUP_LOOP:
        return "SETUP_LOOP";
        break;
    case SETUP_EXCEPT:
        return "SETUP_EXCEPT";
        break;
    case SETUP_FINALLY:
        return "SETUP_FINALLY";
        break;
    case LOAD_FAST:
        return "LOAD_FAST";
        break;
    case STORE_FAST:
        return "STORE_FAST";
        break;
    case DELETE_FAST:
        return "DELETE_FAST";
        break;
    case RAISE_VARARGS:
        return "RAISE_VARARGS";
        break;
    case CALL_FUNCTION:
        return "CALL_FUNCTION";
        break;
    case MAKE_FUNCTION:
        return "MAKE_FUNCTION";
        break;
    case BUILD_SLICE:
        return "BUILD_SLICE";
        break;
    case LOAD_CLOSURE:
        return "LOAD_CLOSURE";
        break;
    case LOAD_DEREF:
        return "LOAD_DEREF";
        break;
    case STORE_DEREF:
        return "STORE_DEREF";
        break;
    case DELETE_DEREF:
        return "DELETE_DEREF";
        break;
    case CALL_FUNCTION_KW:
        return "CALL_FUNCTION_KW";
        break;
    case CALL_FUNCTION_EX:
        return "CALL_FUNCTION_EX";
        break;
    case SETUP_WITH:
        return "SETUP_WITH";
        break;
    case EXTENDED_ARG:
        return "EXTENDED_ARG";
        break;
    case LIST_APPEND:
        return "LIST_APPEND";
        break;
    case SET_ADD:
        return "SET_ADD";
        break;
    case MAP_ADD:
        return "MAP_ADD";
        break;
    case LOAD_CLASSDEREF:
        return "LOAD_CLASSDEREF";
        break;
    case BUILD_LIST_UNPACK:
        return "BUILD_LIST_UNPACK";
        break;
    case BUILD_MAP_UNPACK:
        return "BUILD_MAP_UNPACK";
        break;
    case BUILD_MAP_UNPACK_WITH_CALL:
        return "BUILD_MAP_UNPACK_WITH_CALL";
        break;
    case BUILD_TUPLE_UNPACK:
        return "BUILD_TUPLE_UNPACK";
        break;
    case BUILD_SET_UNPACK:
        return "BUILD_SET_UNPACK";
        break;
    case SETUP_ASYNC_WITH:
        return "SETUP_ASYNC_WITH";
        break;
    case FORMAT_VALUE:
        return "FORMAT_VALUE";
        break;
    case BUILD_CONST_KEY_MAP:
        return "BUILD_CONST_KEY_MAP";
        break;
    case BUILD_STRING:
        return "BUILD_STRING";
        break;
    case BUILD_TUPLE_UNPACK_WITH_CALL:
        return "BUILD_TUPLE_UNPACK_WITH_CALL";
        break;
    case LOAD_METHOD:
        return "LOAD_METHOD";
        break;
    case CALL_METHOD:
        return "CALL_METHOD";
        break;
    
    default:
        return "UNKNOWN";
        break;
    }


}

void check_scope(PyFrameObject *frame, int opcode){
	//printf("in check scope\n");
    get_object_name(frame->f_code->co_filename,current_file);
    get_object_name(frame->f_code->co_name,current_frame);
    current_lineno = PyFrame_GetLineNumber(frame);
	if (!flag_config_loaded) {
		load_configuration();
	}

    if(is_target(current_file)){
        core_main_file_flag = 1;
        last_line_main = current_lineno;
        executed_lines[current_lineno] = 1;
        if(current_lineno > max_lineno){
            max_lineno = current_lineno;
        }
        printf("[%5u execution log] Execute %s:%3d  %s \n",pid,current_file,current_lineno,get_opcode_name(opcode));
    }
    else{
        core_main_file_flag = 0;
    }

    if (!flag_main_file) {
        if(FakeObject_dict == NULL){
            FakeObject_dict = PyDict_New();
            printf("[%5u debug log] FakeObject_dict has been created\n",pid);
        }
        int tmp_flag = 0;
        char tmp_file_name[MAX_PATH];
        strcpy(tmp_file_name,current_file);
        if (strstr(tmp_file_name, name_main_file)) {
            tmp_flag = 1;
            int i = 0;
            flag_main_file = 1;
            //initialize func_list
            int index = 0;
            while(index < 1000){
                func_list[index].index = 0;
                func_list[index].func_name[0] = '\0';
                index = index + 1;
            }
            //
            // printf("flag_main_file is set to 1\n");
            // int config_read = read_instru_config();
            FILE * pFile2 = fopen(outlog, "a");
            if(strstr(forcedExcutionConfig,"no config")){
                fprintf(pFile2, "\n[%5lu]: %s \n",pid,tmp_file_name);
            }
            else{
                fprintf(pFile2, "\n[%5lu]: forked from %s: %s \n",pid,forcedExcutionConfig,tmp_file_name);
            }
            int tmp_init_fork = init_fork_record();
            // printf("[debug log] before read fork record\n");
            int fork_record_flag = read_fork_record();
            // printf("[debug log] after read fork record\n");
            fclose(pFile2);
            if(flag_pyinstaller){
                add_pyinstaller();
            }
            else{
                add_pip();
            }

        }
    }
    if (flag_cut_branch &&  flag_config_loaded && core_main_file_flag && (mergeline != 0)) {
    	branch_cut();
    }
}

void check_main_file(char *filename) {
    pid = GetCurrentProcessId();
    load_configuration();
    if(is_target(current_file)){    
        core_main_file_flag = 1;
        executed_lines[current_lineno] = 1;
        if(current_lineno > max_lineno){
            max_lineno = current_lineno;
        }
        last_line_main = current_lineno;
        strcpy(last_file_name_main,current_file);
        printf("[%5lu debug log] we are execute %s:%d\n",pid,current_file,current_lineno);
    }
    else{
        core_main_file_flag = 0;
    }

    branch_cut();

    
}

void log_opcode_oparg(PyFrameObject * f, int opcode, int oparg) {
    if (log_flag) {
        fprintf(stdout, "[instrument log]: ");
        PyObject_Print(f -> f_code -> co_filename, stdout, 0);
        fprintf(stdout, "lineno: %d, opcode: %d, ", PyFrame_GetLineNumber(f), opcode);
        fprintf(stdout, "oparg: %d\n", oparg);
    }

}

int is_target_file(char * filename) {
    if (!strstr(filename, "/home")) {
        return 0;
    } else if (!strstr(filename, ".py")) {
        return 0;
    } else{
        return 1;
    }
}

void log_opcode(PyFrameObject * f, int opcode) {
    if (log_flag) {
        fprintf(stdout, "[instrument log]: ");
        PyObject_Print(f -> f_code -> co_filename, stdout, 0);
        fprintf(stdout, "lineno: %d, opcode: %d, ", PyFrame_GetLineNumber(f), opcode);
        fprintf(stdout, "oparg: none\n");
    }

}


// int instru_function(PyFrameObject * f, PyObject ** sp, int opcode, int oparg, PyObject * kwnames) {
//     if(!flag_begin_log){
//         //printf("returned because of flag_begin_log\n");
//         return 0;
//     }
//     // printf("we get into instru function\n");
//     char * filename = get_file_name(f);
//     FILE * logfile = fopen(outlog,"a");
//     // printf("[debug log] filename:%s core_exec_flag is %d\n",filename,core_exec_flag);
//     // fprintf(stdout,"lineno: %d, opcode: %d\n",PyFrame_GetLineNumber(f),opcode);
//     if(core_main_file_flag||strstr(filename,name_main_file)||core_exec_flag) {
//         // PyObject_Print((PyObject *)f,stdout,0);
//         // printf("\n");
//         // PyObject_Print((PyObject *)(f->f_code->co_name),stdout,0);
//         // printf("\n");

//         char *last_frame_name;
//         PyObject *s_frame = PyObject_Str((PyObject *)(f->f_code->co_name));
//         if (PyBytes_Check(s_frame)) {
//         last_frame_name = PyBytes_AS_STRING(s_frame);
//         }
//         else if (PyUnicode_Check(s_frame)) {
//             PyObject *t;
//             t = PyUnicode_AsEncodedString(s_frame, "utf-8", "backslashreplace");
//             last_frame_name = PyBytes_AS_STRING(t);
//         }



//         char *func_name = "tmp";
//         if(opcode == CALL_FUNCTION){
//                 PyObject **pfunc = (*&sp) - oparg - 1;
//                 PyObject *func = *pfunc;
//                 PyObject *s = PyObject_Str(func);
//                 if (PyBytes_Check(s)) {
//                         func_name = PyBytes_AS_STRING(s);
//                 }
//                 else if (PyUnicode_Check(s)) {
//                         PyObject *t;
//                         t = PyUnicode_AsEncodedString(s, "utf-8", "backslashreplace");
//                         func_name = PyBytes_AS_STRING(t);
//                 }
                        
//                 //strcpy(current_func,func_name);
//                 Py_ssize_t nkwargs = 0;
//                 Py_ssize_t nargs = oparg - nkwargs;
//                 PyObject **stack = (*&sp) - nargs - nkwargs;
//                 Py_ssize_t arg_num = nargs;
//                 // Py_ssize_t arg_num = PyVectorcall_NARGS(nargs);
                
//                 //fprintf(logfile,"[%5lu]: %10s:%4d  %-10s %-20s  : ",pid,current_file,current_lineno,last_frame_name,func_name);
//                 char arg_full[409600]="";
//                 if(arg_num > 0){
//                     Py_ssize_t tmp_count = (Py_ssize_t)0;
//                     while(tmp_count < arg_num){
//                         //printf("[debug log] we are trying to print function %s arg %d/%d\n",func_name,(int)tmp_count,(int)arg_num-1);
//                         // fprintf(logfile,"[%lu instrument log] original arg[%d]: ",pid,(int)tmp_count);
//                         char *arg = get_object_name(stack[tmp_count]);
//                         strcat(arg_full,arg);
//                         strcat(arg_full," ");
//                         // PyObject_Print(stack[tmp_count],logfile,0);
//                         // fprintf(logfile,"   ");
//                         tmp_count = tmp_count + (Py_ssize_t)1; 
//                     }
//                     // fprintf(logfile,"[%lu instrument log] original arg[0]: ",pid);
//                     // PyObject_Print(stack[0],logfile,0);
//                     // fprintf(logfile,"\n");                 
//                 }
//                 fprintf(logfile,"[%5lu]: %10s:%4d  %-10s %-20s  : %s\n",pid,current_file,current_lineno,last_frame_name,func_name,arg_full);
//                 //fprintf(logfile,"\n");
//                 // if(strstr(filename,name_main_file) && strstr(func_name,"sleep")){
//                 //         printf("[debug log] --------------\n");
//                 //         printf("[debug log] original arg0: ");
//                 //         PyObject_Print(stack[0],stdout,0);
//                 //         long new_arg = 1;
//                 //         PyObject *tmp = PyLong_FromLong(new_arg);
//                 //         stack[0]= tmp;
//                 //         printf("[debug log] \n");
//                 //         // printf("[debug log] arg0 has been changed to 150\n");
//                 //         // printf("[debug log] --------------\n");
//                 // }
//         }
//         else if(opcode == CALL_FUNCTION_KW){
//                 PyObject **pfunc = (*&sp) - oparg - 1;
//                 PyObject *func = *pfunc;
//                 PyObject *s = PyObject_Str(func);
//                 if (PyBytes_Check(s)) {
//                         func_name = PyBytes_AS_STRING(s);
//                 }
//                 else if (PyUnicode_Check(s)) {
//                         PyObject *t;
//                         t = PyUnicode_AsEncodedString(s, "utf-8", "backslashreplace");
//                         func_name = PyBytes_AS_STRING(t);
//                 }
//                 //strcpy(current_func,func_name);
//                 Py_ssize_t nkwargs = (kwnames == NULL) ? 0 : PyTuple_GET_SIZE(kwnames);
//                 Py_ssize_t nargs = oparg - nkwargs;
//                 PyObject **stack = (*&sp) - nargs - nkwargs;
//                 Py_ssize_t arg_num = nargs;
//                 //fprintf(logfile,"[%5lu]: %10s:%4d  %-10s %-20s  : ",pid,current_file,current_lineno,last_frame_name,func_name);
//                 char arg_full[409600]="";
//                 if(arg_num > 0){
//                     Py_ssize_t tmp_count = (Py_ssize_t)0;
//                     while(tmp_count < arg_num){
//                         //printf("[debug log] we are trying to print function %s arg %d/%d\n",func_name,(int)tmp_count,(int)arg_num-1);
//                         // fprintf(logfile,"[%lu instrument log] original arg[%d]: ",pid,(int)tmp_count);
//                         char *arg = get_object_name(stack[tmp_count]);
//                         strcat(arg_full,arg);
//                         strcat(arg_full," ");
//                         // PyObject_Print(stack[tmp_count],logfile,0);
//                         // fprintf(logfile,"   ");
//                         tmp_count = tmp_count + (Py_ssize_t)1; 
//                     }
//                     // fprintf(logfile,"[%lu instrument log] original arg[0]: ",pid);
//                     // PyObject_Print(stack[0],logfile,0);
//                     // fprintf(logfile,"\n");                 
//                 }
//                 fprintf(logfile,"[%5lu]: %10s:%4d  %-10s %-20s  : %s\n",pid,current_file,current_lineno,last_frame_name,func_name,arg_full);
//                 //fprintf(logfile,"\n");
//         }
//         fclose(logfile);
//         return 1;
//     } else {
//         fclose(logfile);
//         return 0;
//     }

// }

// int instru_call_function_ex(PyFrameObject * f, PyObject * func, PyObject * callargs, PyObject * kwdict) {
//     if(!flag_begin_log){
//         return 0;
//     }
//     char * filename = get_file_name(f);
//     FILE * logfile = fopen(outlog,"a");
//     // printf("[debug log] filename:%s\n",filename);
//     // fprintf(stdout,"lineno: %d, opcode: %d\n",PyFrame_GetLineNumber(f),CALL_FUNCTION_EX);
//     //if(core_main_file_flag||strstr(filename,name_main_file)||(core_exec_flag&&strstr(filename,"<module>"))||(core_exec_flag&&strstr(filename,"<string>"))) {
//     if(core_main_file_flag||strstr(filename,name_main_file)||core_exec_flag) {
//         char *last_frame_name;
//         PyObject *s_frame = PyObject_Str((PyObject *)(f->f_code->co_name));
//         if (PyBytes_Check(s_frame)) {
//         last_frame_name = PyBytes_AS_STRING(s_frame);
//         }
//         else if (PyUnicode_Check(s_frame)) {
//             PyObject *t;
//             t = PyUnicode_AsEncodedString(s_frame, "utf-8", "backslashreplace");
//             last_frame_name = PyBytes_AS_STRING(t);
//         }
//         char *func_name = "tmp";
//         PyObject *s = PyObject_Str(func);
//         if (PyBytes_Check(s)) {
//                 func_name = PyBytes_AS_STRING(s);
//         }
//         else if (PyUnicode_Check(s)) {
//                 PyObject *t;
//                 t = PyUnicode_AsEncodedString(s, "utf-8", "backslashreplace");
//                 func_name = PyBytes_AS_STRING(t);
//         }
//         Py_ssize_t arg_num = PyTuple_GET_SIZE(callargs);
//         fprintf(logfile,"[%5lu]: %10s:%4d  %-10s %-20s  : ",pid,current_file,current_lineno,last_frame_name,func_name);
//         // if(arg_num > 0){
//         //     fprintf(logfile,"[%lu instrument log] original arg[0]: ",pid);
//         //     PyObject_Print(stack[0],logfile,0);
//         //     printf("\n");                 
//         // }
//         fclose(logfile);
//         return 1;
//     } else {
//         fclose(logfile);
//         return 0;
//     }

// }
int execute_statement(char * statement, PyObject * globals, PyObject * locals) {
    int start = Py_eval_input; //Py_file_input, and Py_single_input
    PyObject * tmp_ref = PyRun_String(statement, start, globals, locals);
    if(tmp_ref == NULL){
        return 0;
    }
    else{
        return 1;
    }

}




// belows are for the customized objects
// #include "structmember.h"

// typedef struct {
//     PyObject_HEAD
//     PyObject *first; /* first name */
//     PyObject *last;  /* last name */
//     int number;
// } CustomObject;

// static int
// Custom_traverse(CustomObject *self, visitproc visit, void *arg)
// {
//     Py_VISIT(self->first);
//     Py_VISIT(self->last);
//     return 0;
// }

// static int
// Custom_clear(CustomObject *self)
// {
//     Py_CLEAR(self->first);
//     Py_CLEAR(self->last);
//     return 0;
// }

// static void
// Custom_dealloc(CustomObject *self)
// {
//     PyObject_GC_UnTrack(self);
//     Custom_clear(self);
//     Py_TYPE(self)->tp_free((PyObject *) self);
// }

// static PyObject *
// Custom_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
// {
//     CustomObject *self;
//     self = (CustomObject *) type->tp_alloc(type, 0);
//     if (self != NULL) {
//         self->first = PyUnicode_FromString("");
//         if (self->first == NULL) {
//             Py_DECREF(self);
//             return NULL;
//         }
//         self->last = PyUnicode_FromString("");
//         if (self->last == NULL) {
//             Py_DECREF(self);
//             return NULL;
//         }
//         self->number = 0;
//     }
//     return (PyObject *) self;
// }

// static int
// Custom_init(CustomObject *self, PyObject *args, PyObject *kwds)
// {
//     static char *kwlist[] = {"first", "last", "number", NULL};
//     PyObject *first = NULL, *last = NULL, *tmp;

//     if (!PyArg_ParseTupleAndKeywords(args, kwds, "|UUi", kwlist,
//                                      &first, &last,
//                                      &self->number))
//         return -1;

//     if (first) {
//         tmp = self->first;
//         Py_INCREF(first);
//         self->first = first;
//         Py_DECREF(tmp);
//     }
//     if (last) {
//         tmp = self->last;
//         Py_INCREF(last);
//         self->last = last;
//         Py_DECREF(tmp);
//     }
//     return 0;
// }

// static PyMemberDef Custom_members[] = {
//     {"number", T_INT, offsetof(CustomObject, number), 0,
//      "custom number"},
//     {NULL}  /* Sentinel */
// };

// static PyObject *
// Custom_getfirst(CustomObject *self, void *closure)
// {
//     Py_INCREF(self->first);
//     return self->first;
// }

// static int
// Custom_setfirst(CustomObject *self, PyObject *value, void *closure)
// {
//     if (value == NULL) {
//         PyErr_SetString(PyExc_TypeError, "Cannot delete the first attribute");
//         return -1;
//     }
//     if (!PyUnicode_Check(value)) {
//         PyErr_SetString(PyExc_TypeError,
//                         "The first attribute value must be a string");
//         return -1;
//     }
//     Py_INCREF(value);
//     Py_CLEAR(self->first);
//     self->first = value;
//     return 0;
// }

// static PyObject *
// Custom_getlast(CustomObject *self, void *closure)
// {
//     Py_INCREF(self->last);
//     return self->last;
// }

// static int
// Custom_setlast(CustomObject *self, PyObject *value, void *closure)
// {
//     if (value == NULL) {
//         PyErr_SetString(PyExc_TypeError, "Cannot delete the last attribute");
//         return -1;
//     }
//     if (!PyUnicode_Check(value)) {
//         PyErr_SetString(PyExc_TypeError,
//                         "The last attribute value must be a string");
//         return -1;
//     }
//     Py_INCREF(value);
//     Py_CLEAR(self->last);
//     self->last = value;
//     return 0;
// }

// static PyGetSetDef Custom_getsetters[] = {
//     {"first", (getter) Custom_getfirst, (setter) Custom_setfirst,
//      "first name", NULL},
//     {"last", (getter) Custom_getlast, (setter) Custom_setlast,
//      "last name", NULL},
//     {NULL}  /* Sentinel */
// };

// static PyObject *
// Custom_name(CustomObject *self, PyObject *Py_UNUSED(ignored))
// {
//     return PyUnicode_FromFormat("%S %S", self->first, self->last);
// }

// static PyMethodDef Custom_methods[] = {
//     {"name", (PyCFunction) Custom_name, METH_NOARGS,
//      "Return the name, combining the first and last name"
//     },
//     {NULL}  /* Sentinel */
// };

// static PyTypeObject CustomType = {
//     PyVarObject_HEAD_INIT(NULL, 0)
//     .tp_name = "custom.Custom",
//     .tp_doc = "Custom objects",
//     .tp_basicsize = sizeof(CustomObject),
//     .tp_itemsize = 0,
//     .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
//     .tp_new = Custom_new,
//     .tp_init = (initproc) Custom_init,
//     .tp_dealloc = (destructor) Custom_dealloc,
//     .tp_traverse = (traverseproc) Custom_traverse,
//     .tp_clear = (inquiry) Custom_clear,
//     .tp_members = Custom_members,
//     .tp_methods = Custom_methods,
//     .tp_getset = Custom_getsetters,
// };

// static PyModuleDef custommodule = {
//     PyModuleDef_HEAD_INIT,
//     .m_name = "custom",
//     .m_doc = "Example module that creates an extension type.",
//     .m_size = -1,
// };

// PyMODINIT_FUNC
// PyInit_custom(void)
// {
//     PyObject *m;
//     if (PyType_Ready(&CustomType) < 0)
//         return NULL;

//     m = PyModule_Create(&custommodule);
//     if (m == NULL)
//         return NULL;

//     Py_INCREF(&CustomType);
//     PyModule_AddObject(m, "Custom", (PyObject *) &CustomType);
//     return m;
// }



//below are for new fake object
// typedef struct {
//     PyUnicodeObject unicode_obj;
//     PyUnicodeObject *content;
//     int state;
// } FakeObject;

// static PyObject *
// FakeObject_increment(FakeObject *self, PyObject *unused)
// {
//     self->state++;
//     return PyLong_FromLong(self->state);
// }

// static PyMethodDef FakeObject_methods[] = {
//     {"increment", (PyCFunction) FakeObject_increment, METH_NOARGS,
//      PyDoc_STR("increment state counter")},
//     {NULL},
// };

// static int
// FakeObject_init(FakeObject *self, PyObject *args, PyObject *kwds)
// {
//     if (PyUnicode_Type.tp_init((PyObject *) self, args, kwds) < 0){
//         return -1;
//     }
//     self->state = 0;
//     return 0;
// }
// static PyGetSetDef FakeObject_getsetlist[] = {
//     {"__dict__", PyObject_GenericGetDict, PyObject_GenericSetDict},
//     {NULL} /* Sentinel */
// };
// static PyObject *
// FakeObject_descr_get(PyObject *func, PyObject *obj, PyObject *type)
// {
//     if (obj == Py_None || obj == NULL) {
//         Py_INCREF(func);
//         return func;
//     }
//     return PyMethod_New(func, obj);
// }
// static PyTypeObject FakeObjectType = {
//     PyVarObject_HEAD_INIT(NULL, 0)
//     .tp_name = "FakeObject.FakeObject",
//     .tp_doc = "FakeObject for force execution",
//     .tp_basicsize = sizeof(FakeObject),
//     .tp_itemsize = 0,
//     .tp_flags = Py_TPFLAGS_HEAPTYPE,
//     .tp_init = (initproc) FakeObject_init,
//     .tp_methods = FakeObject_methods,
//     .tp_getset = FakeObject_getsetlist,
//     .tp_descr_get = FakeObject_descr_get,
// };
// //|Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE
// static PyModuleDef FakeObjectmodule = {
//     PyModuleDef_HEAD_INIT,
//     .m_name = "FakeObject Module",
//     .m_doc = "Example module that creates FakeObject.",
//     .m_size = -1,
// };

// PyMODINIT_FUNC
// PyInit_FakeObject(void)
// {
//     PyObject *m;
//     FakeObjectType.tp_base = &PyUnicode_Type;
//     if (PyType_Ready(&PyUnicode_Type) < 0)
//         return NULL;

//     printf("FakeObject module is called\n");

//     m = PyModule_Create(&FakeObjectmodule);
//     if (m == NULL)
//         return NULL;

//     Py_INCREF(&FakeObjectType);
//     if (PyModule_AddObject(m, "FakeObject", (PyObject *) &FakeObjectType) < 0) {
//         Py_DECREF(&FakeObjectType);
//         Py_DECREF(m);
//         return NULL;
//     }

//     return m;
// }
#endif /* !Py_PYTHON_H */












