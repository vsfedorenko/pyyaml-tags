# coding: utf-8
from __future__ import absolute_import, division, print_function, \
    unicode_literals

import ast
import re
from abc import abstractmethod as abstract_method

import yaml
from path import Path
from yaml import Dumper, Loader


# noinspection PyMethodMayBeStatic
class BaseTag(object):
    yaml_loader = Loader
    yaml_dumper = Dumper

    tag_name = None
    registered = False

    _left_placeholder = '<%'
    _right_placeholder = '%>'

    def __init__(self):
        super(BaseTag, self).__init__()

    def __new__(cls):
        return super(BaseTag, cls).__new__(cls)

    def yaml_tag(self):
        if not self.tag_name:
            raise ValueError("Tag name can't be null")
        return r'!' + self.tag_name

    def yaml_pattern(self):
        if not self.tag_name:
            raise ValueError("Tag name can't be null")

        pattern = r'^' \
                  + r'(.*)' \
                  + self._left_placeholder \
                  + r'[\s]*' \
                  + '(' + self.tag_name + ')' \
                  + r'[\s]*' \
                  + r'(?:(\((.*)\))|)' \
                  + r'[\s]*' \
                  + self._right_placeholder \
                  + r'(.*)' \
                  + r'$'

        return re.compile(pattern)

    def from_yaml(self, loader, yaml_node, *args, **kwargs):
        work_dir = self.__get_work_dir(yaml_node)

        prefix = None
        suffix = None

        if isinstance(yaml_node, yaml.nodes.ScalarNode):
            yaml_node_value = loader.construct_scalar(yaml_node)
            match = self.yaml_pattern().match(yaml_node_value)

            if match:
                prefix_val, suffix_val, args_val, kwargs_val = \
                    self.__parse_implicit_tag_match(match)

                prefix = prefix_val
                suffix = suffix_val

                if args_val:
                    args += tuple(args_val)
                if kwargs_val:
                    kwargs.update(kwargs_val)
            else:
                args = [yaml_node_value]

        elif isinstance(yaml_node, yaml.nodes.SequenceNode):
            args = loader.construct_sequence(yaml_node)
        elif isinstance(yaml_node, yaml.nodes.MappingNode):
            kwargs = loader.construct_mapping(yaml_node)

        try:
            return self._from_yaml(
                loader, work_dir, prefix, suffix, *args, **kwargs
            )
        except Exception as e:
            raise e

    def to_yaml(self, dumper, data):
        return dumper \
            .represent_yaml_object(self.yaml_tag, data, self.__class__)

    @abstract_method
    def _from_yaml(self, _loader, _work_dir, _prefix, _suffix,
                   *args, **kwargs):

        raise NotImplementedError()

    def __get_work_dir(self, yaml_node):
        try:
            work_dir = Path(yaml_node.start_mark.name).dirname()
        except Exception as e:
            work_dir = Path(yaml_node.end_mark.name).dirname()

        work_dir = work_dir.abspath()

        return work_dir

    def __parse_implicit_tag_match(self, tag_match):
        prefix, tag_name, params_w_brackets, params_wo_brackets, suffix = \
            tag_match.groups()

        args = []
        kwargs = {}

        if not params_w_brackets and not params_wo_brackets:
            return prefix, suffix, args, kwargs

        ast_tree = ast.parse(tag_name + params_w_brackets)
        for ast_node in ast.walk(ast_tree):
            if not isinstance(ast_node, ast.Expr):
                continue

            ast_node_args = ast_node.value.args
            ast_node_keywords = ast_node.value.keywords
            for ast_node_arg in ast_node_args:
                try:
                    self.__convert_node_bool_value(ast_node_arg)

                    if hasattr(ast_node_arg, 'id'):
                        arg_value = ast.literal_eval(ast_node_arg.id)
                    else:
                        arg_value = ast.literal_eval(ast_node_arg)
                except Exception as e:
                    arg_value = ast.literal_eval(
                        '"' + params_wo_brackets + '"'
                    )

                args.append(arg_value)

            for ast_node_keyword in ast_node_keywords:
                kwargs[ast_node_keyword.arg] = \
                    ast.literal_eval(ast_node_keyword.value)

        return prefix, suffix, args, kwargs

    def __convert_node_bool_value(self, ast_node_arg):
        if not hasattr(ast_node_arg, 'id'):
            return

        arg_id = ast_node_arg.id
        if not arg_id:
            return

        for bool_val in [True, False]:
            arg_id = str(arg_id).lower()
            bool_var_str = str(bool_val)
            bool_val_str_lower = bool_var_str.lower()

            if arg_id == bool_val_str_lower:
                ast_node_arg.col_offset = 0
                ast_node_arg.id = bool_var_str


__all__ = (BaseTag,)
