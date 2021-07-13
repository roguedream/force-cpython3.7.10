#ifndef Py_INSTRUMENT_FLAG_H
#define Py_INSTRUMENT_FLAG_H
#include "Python.h"
extern int core_main_file_flag;
extern int core_exec_flag;
extern int current_lineno;
extern char current_file[MAX_PATH];
// extern char *current_filename;
extern char current_frame[512];
extern int last_line;
extern char last_file_name[MAX_PATH];
extern char outlog[MAX_PATH];
extern int flag_main_file;
extern int last_line_main;
extern char last_file_name_main[MAX_PATH];
extern int loop_limit;
extern int flag_in_loop;
extern int jump_count[4096];
extern int flag_call_uninvoked_function;
extern int flag_call_function_from_main;
extern int flag_call_function_from_main_error;
extern int flag_iter;
extern char current_func[512];

extern int flag_last_record_used;
extern int fork_record_length;

extern int executed_lines[30000];
extern int max_lineno;

extern int flag_cut_branch;

extern char object_dump_folder[MAX_PATH];

extern char current_import_module[256];

extern char tmp_fake_object[512];
extern char obj_name[512];
// static inline char* get_object_name(PyObject *object);
#endif