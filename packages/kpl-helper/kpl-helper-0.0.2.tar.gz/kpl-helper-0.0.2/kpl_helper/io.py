from kpl_helper.base import get_config
import json
import os
import logging
logger = logging.getLogger("kpl-helper")


def get_input_path(key, default=""):
    inner = get_config().get_inner()
    if not inner:
        return default
    in_keys = get_config().get_input_keys()
    index = in_keys.index(key)
    if index < 0:
        raise Exception("get_input_dir(). key not exists")
    root = get_config().get_input_root()
    path = os.path.join(root, str(index))
    if not os.path.exists(path):
        raise Exception("input direction not exists: {}".format(path))
    return path


def get_output_path(key, default=""):
    inner = get_config().get_inner()
    if not inner:
        return default
    in_keys = get_config().get_output_keys()
    index = in_keys.index(key)
    if index < 0:
        raise Exception("get_input_dir(). key not exists")
    root = get_config().get_output_root()
    path = os.path.join(root, str(index))
    if not os.path.exists(path):
        os.makedirs(path)
    return path


# def send_data_attribute(output_index=1, class_num=None, class_name_dict=None, sample_num=None):
#     """
#     将数据的属性信息发送给服务器
#     :param output_index:    第index个输出，如划分训练集和测试集会有多个输出. 从1开始
#     :param class_num:   类别数量.
#     :param class_name_dict:  id与类名对应字典. 如: {0: "airplane", 1: "sofa", ...}
#     :param sample_num:  数据集包含样本总数. 注意: 样本总数并非文件总数，如检测数据集，样本总数=图片文件总数=XML标注文件总数
#     :return:
#     """
#     if not KPL_INNER:
#         return
#     dataset_api = get_dataset_api()
#     for k, v in {"class_name": class_num, "class_name_dict": class_name_dict, "sample_num": sample_num}.items():
#         try:
#             resp = session.post('{}/updateDatasetAttribute'.format(dataset_api),
#                                 json={
#                                     "token": get_dataset_token(),
#                                     "output": str(output_index),
#                                     "name": k,
#                                     "value": json.dumps(v)
#                                 },
#                                 timeout=5)
#             logger.info("send data attribute, {} = {}".format(k, v))
#             if resp.status_code != 200:
#                 logger.error("send data attribute http code: {}. content: {}".format(resp.status_code, resp.content))
#         except requests.RequestException as e:
#             logger.error('Could not reach dataset api. detail: {}'.format(e))
