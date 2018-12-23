def cal_mux_num(src_num):
    """每多一个端口，就需要在原有基础上增加一个MUX
    """
    return max(0, src_num-1)