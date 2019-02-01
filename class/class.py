import getopt
import sys
from bean import ClassInfo, OpCode


data = ""


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "-h-f:", ['help', 'file='])
    except getopt.GetoptError:
        print("You can enter -h for help.")
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            help_method()
            sys.exit()
        elif opt in ("-f", "--file"):
            global data
            data = get_class_data(arg)
            class_info = gene_class_info()
            java_code = class_info.to_java_code()
            print(class_info)


# 帮助
def help_method():
    print("Usage:")
    print("python class.py -h|--help")
    print("python class.py -f|--file filename")


# 读取class文件并转换为16进制
def get_class_data(path):
    with open(path, 'rb') as f:
        return f.read().hex()


# 16进制转字符串
def hex_to_str(hex_str):
    return ''.join([chr(c) for c in [int((hex_str[i:i+2]), 16) for i in range(0, len(hex_str), 2)]])


# 截取字符串
def substring_str(len):
    global data
    str = data[0:len]
    data = data[len:]
    return str


# 从class文件中得到常量池
def get_constant_pool(count):
    constant_pool = {}
    for i in range(0, count):
        constant = {}
        tag = int(substring_str(1 * 2), 16)
        if tag == 1:
            constant["type"] = "CONSTANT_Utf8_info"
            constant["tag"] = tag
            length = int(substring_str(2 * 2), 16)
            constant["length"] = length
            constant["bytes"] = hex_to_str(substring_str(length * 1 * 2))
        elif tag == 3:
            constant["type"] = "CONSTANT_Integer_info"
            constant["tag"] = tag
            constant["bytes"] = hex_to_str(substring_str(4 * 2))
        elif tag == 4:
            constant["type"] = "CONSTANT_Float_info"
            constant["tag"] = tag
            constant["bytes"] = hex_to_str(substring_str(4 * 2))
        elif tag == 5:
            constant["type"] = "CONSTANT_Long_info"
            constant["tag"] = tag
            constant["bytes"] = hex_to_str(substring_str(8 * 2))
        elif tag == 6:
            constant["type"] = "CONSTANT_Double_info"
            constant["tag"] = tag
            constant["bytes"] = hex_to_str(substring_str(8 * 2))
        elif tag == 7:
            constant["type"] = "CONSTANT_Class_info"
            constant["tag"] = tag
            constant["index"] = int(substring_str(2 * 2), 16)
        elif tag == 8:
            constant["type"] = "CONSTANT_String_info"
            constant["tag"] = tag
            constant["index"] = int(substring_str(2 * 2), 16)
        elif tag == 9:
            constant["type"] = "CONSTANT_Fieldref_info"
            constant["tag"] = tag
            constant["index1"] = int(substring_str(2 * 2), 16)
            constant["index2"] = int(substring_str(2 * 2), 16)
        elif tag == 10:
            constant["type"] = "CONSTANT_Methodref_info"
            constant["tag"] = tag
            constant["index1"] = int(substring_str(2 * 2), 16)
            constant["index2"] = int(substring_str(2 * 2), 16)
        elif tag == 11:
            constant["type"] = "CONSTANT_InterfaceMethodref_info"
            constant["tag"] = tag
            constant["index1"] = int(substring_str(2 * 2), 16)
            constant["index2"] = int(substring_str(2 * 2), 16)
        elif tag == 12:
            constant["type"] = "CONSTANT_NameAndType_info"
            constant["tag"] = tag
            constant["index1"] = int(substring_str(2 * 2), 16)
            constant["index2"] = int(substring_str(2 * 2), 16)
        elif tag == 15:
            constant["type"] = "CONSTANT_MethodHandle_info"
            constant["tag"] = tag
            constant["reference_kind"] = int(substring_str(1 * 2), 16)
            constant["reference_index"] = int(substring_str(2 * 2), 16)
        elif tag == 16:
            constant["type"] = "CONSTANT_MethodType_info"
            constant["tag"] = tag
            constant["descriptor_index"] = int(substring_str(1 * 2), 16)
        elif tag == 18:
            constant["type"] = "CONSTANT_InvokeDynamic_info"
            constant["tag"] = tag
            constant["bootstrap_method_attr_index"] = int(substring_str(2 * 2), 16)
            constant["name_and_type_index"] = int(substring_str(2 * 2), 16)
        else:
            print("Not a Constant")
        constant_pool[i+1] = constant
    return constant_pool


# 从class文件中得到属性表
def get_attributes_list(count, constant_pool):
    attributes_list = []
    for i in range(0, count):
        attribute = {}
        attribute["attribute_name_index"] = int(substring_str(2 * 2), 16)
        attribute["attribute_length"] = int(substring_str(4 * 2), 16)
        attribute["attribute_name"] = constant_pool[attribute["attribute_name_index"]]["bytes"]
        if attribute["attribute_name"] == "Code":
            attribute["max_statck"] = int(substring_str(2 * 2), 16)
            attribute["max_locals"] = int(substring_str(2 * 2), 16)
            attribute["code_length"] = int(substring_str(4 * 2), 16)
            code_map = {}
            k = 0
            for j in range(0, attribute["code_length"]):
                if k == 0:
                    op_code = OpCode()
                    op_code.hex = substring_str(1 * 2)
                    op_code.code = op_code.code_convert()
                    op_code.num = op_code.operand_num()
                    if op_code.num != 0:
                        k = op_code.num
                    code_map[j] = op_code.code
                else:
                    substring_str(1 * 2)
                    k -= 1
            attribute["code_map"] = code_map
            attribute["exception_table_length"] = int(substring_str(2 * 2), 16)
            exception_list = []
            for j in range(0, attribute["exception_table_length"]):
                exception = {}
                exception["start_pc"] = int(substring_str(2 * 2), 16)
                exception["end_pc"] = int(substring_str(2 * 2), 16)
                exception["handler_pc"] = int(substring_str(2 * 2), 16)
                exception["catch_type"] = int(substring_str(2 * 2), 16)
                exception_list.append(exception)
            attribute["exception_table_list"] = exception_list
            attribute["code_attributes_count"] = int(substring_str(2 * 2), 16)
            attribute["code_attributes_list"] = get_attributes_list(attribute["code_attributes_count"], constant_pool)
        elif attribute["attribute_name"] == "Exceptions":
            attribute["number_of_exceptions"] = int(substring_str(2 * 2), 16)
            exception_index_table = []
            for j in range(0, attribute["number_of_exceptions"]):
                exception_index_table.append(int(substring_str(2 * 2), 16))
            attribute["exception_index_table"] = exception_index_table
        elif attribute["attribute_name"] == "LineNumberTable":
            attribute["line_number_table_length"] = int(substring_str(2 * 2), 16)
            line_number_table_list = []
            for j in range(0, attribute["line_number_table_length"]):
                line_number_table = {}
                line_number_table["start_pc"] = int(substring_str(2 * 2), 16)
                line_number_table["line_number"] = int(substring_str(2 * 2), 16)
                line_number_table_list.append(line_number_table)
            attribute["line_number_table_list"] = line_number_table_list
        elif attribute["attribute_name"] == "SourceFile":
            attribute["sourcefile_index"] = int(substring_str(2 * 2), 16)
        elif attribute["attribute_name"] == "LocalVariableTable":
            attribute["local_variable_table_length"] = int(substring_str(2 * 2), 16)
            local_variable_table = []
            for j in range(0, attribute["local_variable_table_length"]):
                local_variable_info = {}
                local_variable_info["start_pc"] = int(substring_str(2 * 2), 16)
                local_variable_info["length"] = int(substring_str(2 * 2), 16)
                local_variable_info["name_index"] = int(substring_str(2 * 2), 16)
                local_variable_info["descriptor_index"] = int(substring_str(2 * 2), 16)
                local_variable_info["index"] = int(substring_str(2 * 2), 16)
                local_variable_table.append(local_variable_info)
            attribute["local_variable_table"] = local_variable_table
        elif attribute["attribute_name"] == "ConstantValue":
            attribute["constantvalue_index"] = int(substring_str(2 * 2), 16)
        elif attribute["attribute_name"] == "InnerClasses":
            attribute["number_of_classes"] = int(substring_str(2 * 2), 16)
            inner_classes_list = []
            for j in range(0, attribute["number_of_classes"]):
                inner_classes = {}
                inner_classes["inner_class_info_index"] = int(substring_str(2 * 2), 16)
                inner_classes["outer_class_info_index"] = int(substring_str(2 * 2), 16)
                inner_classes["inner_name_index"] = int(substring_str(2 * 2), 16)
                inner_classes["inner_class_access_flags"] = substring_str(2 * 2)
                inner_classes_list.append(inner_classes)
            attribute["inner_classes_list"] = inner_classes_list
        elif attribute["attribute_name"] == "Signature":
            attribute["signature_index"] = int(substring_str(2 * 2), 16)
        else:
            attribute["info"] = substring_str(attribute["attribute_length"] * 1 * 2)
        attributes_list.append(attribute)
    return attributes_list


def gene_class_info():
    # 魔数magic
    magic = substring_str(4 * 2).lower()
    if magic != "cafebabe":
        print("This file is not a class file.")
    else:
        class_info = ClassInfo()
        class_info.magic = magic
        # 次版本号minor_version
        class_info.minor_version = substring_str(2 * 2)
        # 主版本号major_version
        class_info.major_version = substring_str(2 * 2)
        # 常量池个数constant_pool_count
        class_info.constant_pool_count = int(substring_str(2 * 2), 16) - 1
        # 常量池
        class_info.constant_pool = get_constant_pool(class_info.constant_pool_count)
        # 访问标志
        class_info.access_flags = substring_str(2 * 2)
        # 类索引
        class_info.this_class_index = int(substring_str(2 * 2), 16)
        # 父类索引
        class_info.super_class_index = int(substring_str(2 * 2), 16)
        # 接口索引集合大小
        class_info.interfaces_count = int(substring_str(2 * 2), 16)
        # 接口索引集合
        interface_list = []
        for i in range(0, class_info.interfaces_count):
            interface_list.append(int(substring_str(2 * 2), 16))
        class_info.interfaces_list = interface_list
        # 字段表集合大小
        class_info.fields_count = int(substring_str(2 * 2), 16)
        # 字段表集合
        fields_list = []
        for i in range(0, class_info.fields_count):
            filed = {}
            filed["access_flag"] = substring_str(2 * 2)
            filed["name_index"] = int(substring_str(2 * 2), 16)
            filed["descriptor_index"] = int(substring_str(2 * 2), 16)
            filed["attributes_count"] = int(substring_str(2 * 2), 16)
            filed["attributes_list"] = get_attributes_list(filed["attributes_count"], class_info.constant_pool)
            fields_list.append(filed)
        class_info.fields_list = fields_list
        # 方法表集合大小
        class_info.methods_count = int(substring_str(2 * 2), 16)
        # 方法表集合
        methods_list = []
        for i in range(0, class_info.methods_count):
            method = {}
            method["access_flag"] = substring_str(2 * 2)
            method["name_index"] = int(substring_str(2 * 2), 16)
            method["descriptor_index"] = int(substring_str(2 * 2), 16)
            method["attributes_count"] = int(substring_str(2 * 2), 16)
            method["attributes_list"] = get_attributes_list(method["attributes_count"], class_info.constant_pool)
            methods_list.append(method)
        class_info.methods_list = methods_list
        # 其他属性表集合大小
        class_info.attributes_count = int(substring_str(2 * 2), 16)
        class_info.attributes_list = get_attributes_list(class_info.attributes_count, class_info.constant_pool)
        return class_info


if __name__ == "__main__":
    main(sys.argv[1:])
