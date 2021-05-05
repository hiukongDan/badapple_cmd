# file: compressTxt.py
# description: a quick solution for compress txt generated by compress in badapply.py
#   with format - (character + frequency)* + [newline]
# author: Hiukong Dan
# version: 1.0    6/May/2021

def compress(fil_name):
    """
    Compress file using character + frequency
    a newline attached to each line
    """
    filin_name = fil_name
    filout_name = fil_name + ".out"
    filin = open(filin_name, 'r')
    filout = open(filout_name, 'w')
    
    lines = filin.readlines()
    
    # compress line one by one
    for line in lines:
        lineout = ""
        ch = line[0]
        count = 0
        for x in range(1, len(line)):
            if line[x] != ch:
                if line[x] == '\n':
                    lineout += ch + "%s"%count
                    filout.write(lineout + '\n')
                else:
                    lineout += ch + "%s"%count
                    ch = line[x]
                    count = 1
            else:
                count += 1
                
    filin.close()
    filout.close()

def decompress_file(fil_name):
    """
    Decompress file from character + frequency
    """
    fil = open(fil_name)
    lines = fil.readlines()
    fil.close()
    
    filout = open(fil_name+".dec", 'w')
    
    for line in lines:
        filout.write(decompress(line))
    
    filout.close()
    
def decompress(compressed_str):
    """
    decompress one string of compressed text
    TODO:
    using module re
    """
    
    ret = ""
    last_char = ''
    count = 0
    
    for x in range(len(compressed_str)):
        next_ch = compressed_str[x]
        if next_ch == '\n':
            if count > 0:
                ret += last_char * count
            ret += '\n'
            count = 0
            last_char = ''
        elif str.isdigit(next_ch):
            count = count * 10 + int(next_ch)
        else:
            if count > 0:
                ret += last_char * count
                count = 0
            else:
                count = 0
            last_char = next_ch
    
    return ret

if __name__ == "__main__":
    #filin_name = "badapple.txt"
    #filout_name = "badapple_compressed.txt"
    filin_name = "badapple.txt"
    compress(filin_name)
    # decompress_file(filin_name+".out")