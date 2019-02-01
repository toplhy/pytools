

class ClassInfo(object):

    def __init__(self):
        self.magic = ""
        self.minor_version = ""
        self.major_version = ""
        self.constant_pool_count = 0
        self.constant_pool = {}
        self.access_flags = ""
        self.this_class_index = ""
        self.super_class_index = ""
        self.interfaces_count = 0
        self.interfaces_list = []
        self.fields_count = 0
        self.fields_list = []
        self.methods_count = 0
        self.methods_list = []
        self.attributes_count = 0
        self.attributes_list = []

    def to_java_code(self):
        # package
        full_class_name = self.constant_pool.get(self.constant_pool.get(self.this_class_index)["index"])["bytes"].replace('/', '.')
        package = 'package %s;\n\n' % full_class_name[:full_class_name.rindex(".")]
        # imports
        imports = ""

        return package + imports

    def __str__(self):
        classStr = "magic: %s\n" % self.magic
        classStr += "minor_version: %s\n" % self.minor_version
        classStr += "major_version: %s\n" % self.major_version
        classStr += "constant_pool_count: %s\n" % self.constant_pool_count
        classStr += "constant_pool: \n"
        for i in range(1, self.constant_pool_count):
            classStr += "\t#%s\t%s\n" % (i, self.constant_pool[i])
        classStr += "access_flags: %s\n" % self.access_flags
        classStr += "this_class_index: %s\n" % self.this_class_index
        classStr += "super_class_index: %s\n" % self.super_class_index
        classStr += "interfaces_count: %s\n" % self.interfaces_count
        for i in range(0, self.interfaces_count):
            classStr += "\t%s\n" % self.interfaces_list[i]
        classStr += "fields_count: %s\n" % self.fields_count
        classStr += "fields_list: \n"
        for i in range(0, self.fields_count):
            classStr += "\t%s\n" % self.fields_list[i]
        classStr += "methods_count: %s\n" % self.methods_count
        classStr += "methods_list: \n"
        for i in range(0, self.methods_count):
            classStr += "\t%s\n" % self.methods_list[i]
        classStr += "attributes_count: %s\n" % self.attributes_count
        classStr += "attributes_list: \n"
        for i in range(0, self.attributes_count):
            classStr += "\t%s\n" % self.attributes_list[i]
        return classStr


class OpCode(object):

    def __init__(self):
        self.hex = ""
        self.code = ""
        self.num = ""

    def code_convert(self):
        switcher = {
            "00": "nop", "01": "aconst_null", "02": "iconst_m1", "03": "iconst_0", "04": "iconst_1",
            "05": "iconst_2", "06": "iconst_3", "07": "iconst_4", "08": "iconst_5", "09": "lconst_0",
            "0a": "lconst_1", "0b": "fconst_0", "0c": "fconst_1", "0d": "fconst_2", "0e": "dconst_0",
            "0f": "dconst_1", "10": "bipush", "11": "sipush", "12": "ldc", "13": "ldc_w",
            "14": "ldc2_w", "15": "iload", "16": "lload", "17": "fload", "18": "dload",
            "19": "aload", "1a": "iload_0", "1b": "iload_1", "1c": "iload_2", "1d": "iload_3",
            "1e": "lload_0", "1f": "lload_1", "20": "lload_2", "21": "lload_3", "22": "fload_0",
            "23": "fload_1", "24": "fload_2", "25": "fload_3", "26": "dload_0", "27": "dload_1",
            "28": "dload_2", "29": "dload_3", "2a": "aload_0", "2b": "aload_1", "2c": "aload_2",
            "2d": "aload_3", "2e": "iaload", "2f": "laload", "30": "faload", "31": "daload",
            "32": "aaload", "33": "baload", "34": "caload", "35": "saload", "36": "istore",
            "37": "lstore", "38": "fstore", "39": "dstore", "3a": "astore", "3b": "istore_0",
            "3c": "istore_1", "3d": "istore_2", "3e": "istore_3", "3f": "lstore_0", "40": "lstore_1",
            "41": "lstore_2", "42": "lstore_3", "43": "fstore_0", "44": "fstore_1", "45": "fstore_2",
            "46": "fstore_3", "47": "dstore_0", "48": "dstore_1", "49": "dstore_2", "4a": "dstore_3",
            "4b": "astore_0", "4c": "astore_1", "4d": "astore_2", "4e": "astore_3", "4f": "iastore",
            "50": "lastore", "51": "fastore", "52": "dastore", "53": "aastore", "54": "bastore",
            "55": "castore", "56": "sastore", "57": "pop", "58": "pop2", "59": "dup",
            "5a": "dup_x1", "5b": "dup_x2", "5c": "dup2", "5d": "dup2_x1", "5e": "dup2_x2",
            "5f": "swap", "60": "iadd", "61": "ladd", "62": "fadd", "63": "dadd",
            "64": "is", "65": "ls", "66": "fs", "67": "ds", "68": "imul",
            "69": "lmul", "6a": "fmul", "6b": "dmul", "6c": "idiv", "6d": "ldiv",
            "6e": "fdiv", "6f": "ddiv", "70": "irem", "71": "lrem", "72": "frem",
            "73": "drem", "74": "ineg", "75": "lneg", "76": "fneg", "77": "dneg",
            "78": "ishl", "79": "lshl", "7a": "ishr", "7b": "lshr", "7c": "iushr",
            "7d": "lushr", "7e": "iand", "7f": "land", "80": "ior", "81": "lor",
            "82": "ixor", "83": "lxor", "84": "iinc", "85": "i2l", "86": "i2f",
            "87": "i2d", "88": "l2i", "89": "l2f", "8a": "l2d", "8b": "f2i",
            "8c": "f2l", "8d": "f2d", "8e": "d2i", "8f": "d2l", "90": "d2f",
            "91": "i2b", "92": "i2c", "93": "i2s", "94": "lcmp", "95": "fcmpl",
            "96": "fcmpg", "97": "dcmpl", "98": "dcmpg", "99": "ifeq", "9a": "ifne",
            "9b": "iflt", "9c": "ifge", "9d": "ifgt", "9e": "ifle", "9f": "if_icmpeq",
            "a0": "if_icmpne", "a1": "if_icmplt", "a2": "if_icmpge", "a3": "if_icmpgt", "a4": "if_icmple",
            "a5": "if_acmpeq", "a6": "if_acmpne", "a7": "goto", "a8": "jsr", "a9": "ret",
            "aa": "tableswitch", "ab": "lookupswitch", "ac": "ireturn", "ad": "lreturn", "ae": "freturn",
            "af": "dreturn", "b0": "areturn", "b1": "return", "b2": "getstatic", "b3": "putstatic",
            "b4": "getfield", "b5": "putfield", "b6": "invokevirtual", "b7": "invokespecial", "b8": "invokestatic",
            "b9": "invokeinterface", "ba": "–", "bb": "new", "bc": "newarray", "bd": "anewarray",
            "be": "arraylength", "bf": "athrow", "c0": "checkcast", "c1": "instanceof", "c2": "monitorenter",
            "c3": "monitorexit", "c4": "wide", "c5": "multianewarray", "c6": "ifnull", "c7": "ifnonnull",
            "c8": "goto_w", "c9": "jsr_w"
        }
        return switcher.get(self.hex, "")

    def operand_num(self):
        switcher = {
            "aload": 1, "anewarray": 2, "astore": 1, "bipush": 1, "checkcast": 2,
            "dload": 1, "dstore": 1, "fload": 1, "fstore": 1, "getfield": 2,
            "getstatic": 2, "goto": 2, "goto_w": 4, "if_acmp<cond>": 2, "if_icmp<cond>": 2,
            "if<cond>": 2, "ifnonnull": 2, "ifnull": 2, "iinc": 1, "iload": 1,
            "instanceof": 2, "invokedynamic": 2, "invokeinterface": 4, "invokespecial": 2, "invokestatic": 2,
            "invokevirtual": 2, "istore": 1, "jsr": 2, "jsr_wbranch": 4, "ldc": 1,
            "ldc_w": 2, "ldc2_w": 2, "lload": 1, "lstore": 1, "multianewarray": 3,
            "new": 2, "putfield": 2, "putstatic": 2, "ret": 1, "sipush": 2
        }
        return switcher.get(self.code, 0)
