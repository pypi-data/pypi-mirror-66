#coding=utf-8

'''
easypwd-0.3
'''

def __password(password_type, password_length):
    if not password_length > 0:
        return False
    number_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    lowercase_list = ['a', 'b', 'c', 'd', 'e', 'f', 'j', 'h', 'i', 'g', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    uppercase_list = ['A', 'B', 'C', 'D', 'E', 'F', 'J', 'H', 'I', 'G', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    symbol_list = ['~', '!', '@', '#', '$', '%', '^', '&', '*']
    if password_type == 'md5':
        if not password_length <= 32:
            return False
        return __import__('hashlib').md5(str(__import__('time').time()) + __password("strong", 256)).hexdigest()[:password_length]
    elif password_type == 'weak':
        block_length = password_length / 1
        base_number_list =      []
        for x in [number_list[__import__('random').randint(0, len(number_list)-1)] for y in xrange(block_length)]:
            base_number_list.append(x)
        base_list = base_number_list
    elif password_type == 'normal':
        if not password_length >= 2:
            return False
        block_length = password_length / 2
        base_number_list =      []
        base_lowercase_list =   []
        for x in [number_list[__import__('random').randint(0, len(number_list)-1)] for y in xrange(block_length)]:
            base_number_list.append(x)
        for x in [lowercase_list[__import__('random').randint(0, len(lowercase_list)-1)] for y in xrange(password_length - block_length)]:
            base_lowercase_list.append(x)
        base_list = base_number_list + base_lowercase_list
    elif password_type == 'strong':
        if not password_length >= 3:
            return False
        block_length = password_length / 3
        base_number_list =      []
        base_lowercase_list =   []
        base_uppercase_list =   []
        for x in [number_list[__import__('random').randint(0, len(number_list)-1)] for y in xrange(block_length)]:
            base_number_list.append(x)
        for x in [lowercase_list[__import__('random').randint(0, len(lowercase_list)-1)] for y in xrange(block_length)]:
            base_lowercase_list.append(x)
        for x in [uppercase_list[__import__('random').randint(0, len(uppercase_list)-1)] for y in xrange(password_length - block_length)]:
            base_uppercase_list.append(x)
        base_list = base_number_list + base_lowercase_list + base_uppercase_list
    elif password_type == 'very_strong':
        if not password_length >= 4:
            return False
        block_length = password_length / 4
        base_number_list =      []
        base_lowercase_list =   []
        base_uppercase_list =   []
        base_symbol_list =      []
        for x in [number_list[__import__('random').randint(0, len(number_list)-1)] for y in xrange(block_length)]:
            base_number_list.append(x)
        for x in [lowercase_list[__import__('random').randint(0, len(lowercase_list)-1)] for y in xrange(block_length)]:
            base_lowercase_list.append(x)
        for x in [uppercase_list[__import__('random').randint(0, len(uppercase_list)-1)] for y in xrange(block_length)]:
            base_uppercase_list.append(x)
        for x in [symbol_list[__import__('random').randint(0, len(symbol_list)-1)] for y in xrange(password_length - block_length)]:
            base_uppercase_list.append(x)
        base_list = base_number_list + base_lowercase_list + base_uppercase_list + base_symbol_list
    else:
        pass
    password = ''
    for x in xrange(password_length):
        y = base_list[__import__('random').randint(0, len(base_list)-1)]
        password += y
        base_list.remove(y)
    return password

def md5(password_length):
    return __password('md5', password_length)

def weak(password_length):
    return __password('weak', password_length)

def normal(password_length):
    return __password('normal', password_length)

def strong(password_length):
    return __password('strong', password_length)
    
def very_strong(password_length):
    return __password('very_strong', password_length)

def cmd_interact():
    while True:
        while  True:
            password_type = raw_input('[*] PasswordType: [0]md5(m) [1]weak(w) [2]normal(n) [3]strong(s) [4]very_strong(vs).\n[*] type>> ')
            if password_type.strip() in ('0', 'md5', 'm'):
                _password_type = 'md5'
                break
            elif password_type.strip() in ('1', 'weak', 'w'):
                _password_type = 'weak'
                break
            elif password_type.strip() in ('2', 'normal', 'n'):
                _password_type = 'normal'
                break
            elif password_type.strip() in ('3', 'strong', 's'):
                _password_type = 'strong'
                break
            elif password_type.strip() in ('4', 'very_strong', 'vs'):
                _password_type = 'very_strong'
                break
            elif password_type.strip() == 'exit':
                exit()
            else:
                print '[!] PasswordType Error. Try Again.'
                continue
        while True:
            password_length = raw_input('[*] PasswordLength: 1<=md5<=32 weak>=1 normal>=2 strong>=3 very_strong>=4.\n[*] length>> ')
            if password_length.strip() == 'exit':
                exit()
            try:
                if int(password_length) > 0:
                    _password_length = int(password_length)
                    break
                else:
                    print "[!] PasswordLength Must be more than 0. Try Again."
                    continue
            except:
                    print "[!] PasswordLength Must be NUMBER. Try Again."
        res = __password(_password_type, _password_length)
        if res is not False:
            print ">> %s <<" %res
        else:
            print ">> ERROR!!! <<"
            
def cmd_argv():
    
    argv_list = __import__('sys').argv
    password_type   = argv_list[1]
    password_length = argv_list[2]
    
    if password_type.strip() in ('0', 'md5', 'm'):
        _password_type = 'md5'
    elif password_type.strip() in ('1', 'weak', 'w'):
        _password_type = 'weak'
    elif password_type.strip() in ('2', 'normal', 'n'):
        _password_type = 'normal'
    elif password_type.strip() in ('3', 'strong', 's'):
        _password_type = 'strong'
    elif password_type.strip() in ('4', 'very_strong', 'vs'):
        _password_type = 'very_strong'
    else:
        help()
        return

    try:
        _password_length = int(password_length)
    except:
        help()
        return

    res = __password(_password_type, _password_length)
    if res is not False:
        print ">> %s <<" %res
    else:
        print ">> ERROR!!! <<"
            
def help():
    print "[*] Usage: easypwd <PasswordType> <PasswordLength>"
    print "[*] PasswordType: [0]md5(m) [1]weak(w) [2]normal(n) [3]strong(s) [4]very_strong(vs)."
    print "[*] PasswordLength: 1<=md5<=32 weak>=1 normal>=2 strong>=3 very_strong>=4."
    print "[*] Example: easypwd md5 6"
    print "[*] Example: easypwd weak 7"
    print "[*] Example: easypwd normal 8"
    print "[*] Example: easypwd strong 9"
    print "[*] Example: easypwd very_strong 10"
    print "[*] Example: easypwd 0 11"
    print "[*] Example: easypwd 1 12"
    print "[*] Example: easypwd 2 13"
    print "[*] Example: easypwd 3 14"
    print "[*] Example: easypwd 4 15"
    print "[*] Example: easypwd m 16"
    print "[*] Example: easypwd w 17"
    print "[*] Example: easypwd n 18"
    print "[*] Example: easypwd s 19"
    print "[*] Example: easypwd vs 20"
    
if __name__ == '__main__':
    argv_list = __import__('sys').argv
    if len(argv_list) is not 3:
        help()
        cmd_interact()
    else:
        cmd_argv()
