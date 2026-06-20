ENABLED = True
AVAILABLE_FUNCTIONS = ['file_bucket']

TOOLS = [
    {
        "type": "function",
        "is_local": True,
        "function": {
            "name": "file_bucket",
            "description": "Get file list, Seletc Directory, Read text file, Write text file in sapphire environment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_cmd": {
                        "type": "string",
                        "description": "If I need to get a file list, write: 'list'. If select directory, write: 'cd,foldername'. If step back directory, write: 'cd,go!back'. If read the entire text file, write: 'r,filename'. if read only one line in a text file, write: 'rl,filename,lineNumber'. The first line in the text file started with number '1'. If create or overwrite a text file, write: 'w,filename,AI write text here...'. If append text in file, write: 'a,filename,AI write text here...'. If I want to jump straight to the Directory I need in Directory Tree, write: 'rootDIR:/foldername/foldername/foldername' ... and so on... If I want to jump straight to the root Directory, write: 'rootDIR:/'. If I want to create a new directory, write: 'mk,foldername'."
                    }
                },
                "required": ["input_cmd"]
            }
        }
    }
]
import platform
from pathlib import Path

# Start conf:
userDIR = Path.home()
root_str = "Location = rootDIR:"

if platform.system() == "Windows":
   sapDIR = Path(str(userDIR) + "\\sapphire_filebox")
else:
   sapDIR = Path(str(userDIR) + "/sapphire_filebox")

sapDIR_root = sapDIR

if sapDIR.is_dir():
    pass
else:
    Path(str(sapDIR)).mkdir(parents=True, exist_ok=True)

if platform.system() == "Windows":
    pre_path = str(sapDIR) + '\\'
else:
    pre_path = str(sapDIR) + '/'

pre_path_root = pre_path

_FINAL_str = ""
# conf end.

def sr_DIR():
    global sapDIR_root, sapDIR, pre_path, _FINAL_str, root_str

    _FINAL_str = ""
    DIR_LIST = "Directories: "
    F_LIST = "Files: "
    d_ls = []
    f_ls = []
    d = 0
    f = 0
    ffex = "Objects counted: "

    for entry in sapDIR.iterdir():
        if entry.is_file():
            f_ls.append(entry)
        elif entry.is_dir():
            d_ls.append(entry)

    for entry in range(0, len(d_ls)):
        st = str(d_ls[entry])
        st = st.replace(pre_path, "")
        if entry == 0:
            DIR_LIST = DIR_LIST + st
        else:
            DIR_LIST = DIR_LIST + ", " + st
        d = d + 1

    for entry in range(0, len(f_ls)):
        st = str(f_ls[entry])
        st = st.replace(pre_path, "")
        if entry == 0:
            F_LIST = F_LIST + st
        else:
            F_LIST = F_LIST + ", " + st
        f = f + 1

    st = str(sapDIR).replace(str(sapDIR_root), "")
    st = root_str + st

    if (d > 0) and (f > 0):
        _FINAL_str = st + '\n' + ffex + str(d) + " Directories " + str(f) + " Files;" + '\n\n' + DIR_LIST + '\n' + F_LIST
    elif (d == 0) and (f > 0):
        _FINAL_str = st + '\n' + ffex + str(d) + " Directories " + str(f) + " Files;" + '\n\n' + F_LIST
    elif (d > 0) and (f == 0):
        _FINAL_str = st + '\n' + ffex + str(d) + " Directories " + str(f) + " Files;" + '\n\n' + DIR_LIST
    elif (d == 0) and (f == 0):
        _FINAL_str = st + '\n\n' + "Empty: (0 Directories, 0 Files)"

def CD_DIR(new_dir):
    global sapDIR, pre_path, _FINAL_str

    if platform.system() == "Windows":
        sapDIR = Path(str(sapDIR) + "\\" + new_dir)
    else:
        sapDIR = Path(str(sapDIR) + "/" + new_dir)

    if sapDIR.is_dir():
        if platform.system() == "Windows":
            pre_path = str(sapDIR) + '\\'
        else:
            pre_path = str(sapDIR) + '/'

        sr_DIR() # search dir...
    else:
        _FINAL_str = "This directory does not exist!"

def CD_DIRECT(full_path):
    global sapDIR, sapDIR_root, pre_path, pre_path_root, _FINAL_str

    if full_path == "/" or full_path == "\\":
        sapDIR = sapDIR_root
        pre_path = pre_path_root
        sr_DIR() # search dir...
    else:

        if platform.system() == "Windows":
            sapDIR = Path(str(sapDIR_root) + "\\" + full_path)
        else:
            sapDIR = Path(str(sapDIR_root) + "/" + full_path)

        if sapDIR.is_dir():
            if platform.system() == "Windows":
                pre_path = str(sapDIR) + '\\'
            else:
                pre_path = str(sapDIR) + '/'

            sr_DIR() # search dir...
        else:
            _FINAL_str = "This directory does not exist!"

def Back_DIR():
    global sapDIR, sapDIR_root, pre_path, _FINAL_str
    loc_list = []
    s = ""

    if not sapDIR_root == sapDIR:
        if platform.system() == "Windows":
            loc_list = str(sapDIR).split('\\')
        else:
            loc_list = str(sapDIR).split('/')

        for entry in range(0, len(loc_list)-1):
            if platform.system() == "Windows":
                if entry == 0:
                    s = loc_list[0]
                else:
                    s = s + "\\" + loc_list[entry]
            else:
                if entry == 0:
                    pass
                else:
                    s = s + "/" + loc_list[entry]

        sapDIR = Path(s)

        loc_list.clear
        s = ""

        if platform.system() == "Windows":
            loc_list = pre_path.split('\\')
        else:
            loc_list = pre_path.split('/')

        for entry in range(0, len(loc_list)-2):
            if platform.system() == "Windows":
                if entry == 0:
                    s = loc_list[0]
                else:
                    s = s + "\\" + loc_list[entry]
            else:
                if entry == 0:
                    pass
                else:
                    s = s + "/" + loc_list[entry]

        pre_path = s + "/"

        sr_DIR() # search dir...
    else:
        _FINAL_str = "You are already in the root directory."

oLINE = False
ordered_line = 0
wordPAD = ""

def read_TextFile(_txtfile_):
    global _FINAL_str, oLINE, ordered_line

    if oLINE == False:
        if _txtfile_.exists():
            with open(_txtfile_) as _TextFile:
                _FINAL_str = _TextFile.read()
        else:
            _FINAL_str = "This file does not exist here!"
    else:
        if _txtfile_.exists():
            with open(_txtfile_) as _TextFile:
                notepad = _TextFile.readlines()
                _FINAL_str = notepad[ordered_line]
        else:
            _FINAL_str = "This file does not exist here!"

    if oLINE == True:
        oLINE = False
        ordered_line = 0

def write_TextFile(afile):
    global _FINAL_str, wordPAD, oLINE

    if oLINE == False:
        if afile.exists():
            with open(afile, "w", encoding="utf-8") as _file_:
                _file_.write(wordPAD + "\n")
        else:
            with open(afile, "x", encoding="utf-8") as _file_:
                _file_.write(wordPAD + "\n")
        _FINAL_str = "Saving is done."
    else:
        with open(afile, "a", encoding="utf-8") as _file_:
            _file_.write(wordPAD + "\n")
        _FINAL_str = "Content successfully added to file."

    if not wordPAD == "":
        wordPAD = ""

    if oLINE == True:
        oLINE = False

def CreateDIR(_DIRname_):
    global sapDIR, pre_path, _FINAL_str

    if platform.system() == "Windows":
        Path(str(sapDIR) + '\\' + _DIRname_).mkdir(parents=True, exist_ok=True)
    else:
        Path(str(sapDIR) + '/' + _DIRname_).mkdir(parents=True, exist_ok=True)

    
    _FINAL_str = 'Directory created.'

def execute(function_name, arguments, config, plugin_settings=None):
    global sapDIR, _FINAL_str, oLINE, ordered_line, wordPAD
    command = ""
    target = ""
    root_sig = "nop."
    full_dir = ""
    line_num_str = ""

    if function_name == 'file_bucket':
        input_cmd = arguments.get('input_cmd', '')

        if input_cmd == "list":            
            sr_DIR()
            return f"{_FINAL_str}", True

        # Check for "cd" command
        elif input_cmd.startswith("cd,"): # Check if it starts with "cd,"
            parts = input_cmd.split(",", 1)
            if len(parts) == 2:
                command = parts[0] # "cd"
                target = parts[1]  # This will be "new_dir" or "go!back"
                if target == "go!back":
                    Back_DIR()
                else:
                    CD_DIR(target)
                return f"{_FINAL_str}", True
            else:
                return "Error: Invalid 'cd' command format. Expected 'cd,foldername' or 'cd,go!back'.", False

        # Check for "r" (read) command
        elif input_cmd.startswith("r,"): # Check if it starts with "r,"
            parts = input_cmd.split(",", 1)
            if len(parts) == 2:
                command = parts[0] # "r"
                target = parts[1]  # This will be "some_text.txt"
                if platform.system() == "Windows":
                    fAddress = Path(str(sapDIR) + "\\" + target)
                else:
                    fAddress = Path(str(sapDIR) + "/" + target)
                read_TextFile(fAddress)
                return f"{_FINAL_str}", True
            else:
                return "Error: Invalid 'r' command format. Expected 'r,filename'.", False

        elif input_cmd.startswith("rl,"): # Check if it starts with "rl,"
            parts = input_cmd.split(",", 2)
            if len(parts) == 3:
                oLINE = True
                command = parts[0] # "rl"
                target = parts[1]  # This will be "some_text.txt"
                try:
                    line_num_str = parts[2]
                    ordered_line = int(line_num_str) - 1 # Convert to integer
                    if ordered_line < 0:
                        ordered_line = 0

                    if platform.system() == "Windows":
                        fAddress = Path(str(sapDIR) + "\\" + target)
                    else:
                        fAddress = Path(str(sapDIR) + "/" + target)
                    read_TextFile(fAddress)
                    return f"{_FINAL_str}", True
                except ValueError:
                    return "Error: Invalid 'rl' command format. lineNumber must be a valid integer!", False                
            else:
                return "Error: Invalid 'rl' command format. Expected 'rl,filename,lineNumber'.", False


        # Check for "w" (write) command
        elif input_cmd.startswith("w,"): # Check if it starts with "w,"
            parts = input_cmd.split(",", 2)
            if len(parts) == 3:
                command = parts[0] # "w"
                target = parts[1]  # This will be "some_text.txt"
                wordPAD = parts[2] # AI text...

                if platform.system() == "Windows":
                    fAddress = Path(str(sapDIR) + "\\" + target)
                else:
                    fAddress = Path(str(sapDIR) + "/" + target)
                write_TextFile(fAddress)
                return f"{_FINAL_str}", True
            else:
                return "Error: Invalid 'w' command format. Expected 'w,filename,AI written text'.", False
        # Check for "a" (write) command
        elif input_cmd.startswith("a,"): # Check if it starts with "a,"
            parts = input_cmd.split(",", 2)
            if len(parts) == 3:
                oLINE = True
                command = parts[0] # "a"
                target = parts[1]  # This will be "some_text.txt"
                wordPAD = parts[2] # AI text...

                if platform.system() == "Windows":
                    fAddress = Path(str(sapDIR) + "\\" + target)
                else:
                    fAddress = Path(str(sapDIR) + "/" + target)
                write_TextFile(fAddress)
                return f"{_FINAL_str}", True
            else:
                return "Error: Invalid 'a' command format. Expected 'a,filename,AI written text'.", False

        # Check for "rootDIR" command
        elif input_cmd.startswith("rootDIR:"): # Check if it starts with "rootDIR:"
            parts = input_cmd.split(":", 1)
            if len(parts) == 2:
                root_sig = parts[0] # "rootDIR"
                full_dir = parts[1] # This will be the path
                CD_DIRECT(full_dir)
                return f"{_FINAL_str}", True
            else:
                return "Error: Invalid 'rootDIR' command format. Expected 'rootDIR:/path'.", False

        # Check for "mk" command
        elif input_cmd.startswith("mk,"): # Check if it starts with "mk,"
            parts = input_cmd.split(",", 1)
            if len(parts) == 2:
                command = parts[0] # "mk"
                target = parts[1]  # This will be created "new_dir"
                CreateDIR(target)
                return f"{_FINAL_str}", True
            else:
                return "Error: Invalid 'mk' command format. Expected 'mk,foldername'.", False

        else:
            return f"invalid command", False
