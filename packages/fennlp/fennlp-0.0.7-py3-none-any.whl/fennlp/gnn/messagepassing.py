#! usr/bin/env python3
# -*- coding:utf-8 -*-
"""
reference:
https://github.com/microsoft/tf2-gnn/blob/master/tf2_gnn/layers/message_passing/message_passing.py
"""
import tensorflow as tf

class MessagePassing(tf.keras.layers.Layer):
    def __init__(self, aggr="add", **kwargs):
        super(MessagePassing, self).__init__(**kwargs)
        self.aggr = aggr

    def message_function(self, edge_source_states,
                             edge_target_states,
                             num_incoming_to_node_per_message,
                             num_outing_to_node_per_message,
                             edge_type_idx):  # 也就是公式中的M_t
        """
        :param edge_source_states: A tensor of shape [E, D] giving the node states at the source node
                of each edge.
        :param edge_target_states:A tensor of shape [E, D] giving the node states at the target node
                of each edge.
        :param num_incoming_to_node_per_message:A tensor of shape [E] giving the number of messages
                entering the target node of each edge. For example, if
                num_incoming_to_node_per_message[i] = 4, then there are 4 messages whose target
                node is the target node of message i.
        :param num_outing_to_node_per_message:A tensor of shape [E] giving the number of messages
                outing the source node of each edge. For example, if
                num_outing_to_node_per_message[i] = 4, then there are 4 messages whose source
                node is the source node of message i.
        :param edge_type_idx: The edge type that that these messages correspond to.
        :param training:
        :return:
        """
        raise NotImplementedError

    def propagate(self, inputs):
        """
        :param node_embeddings: [N,D]
        :param adjacency_lists: [E,2]
        :param training:
        :return:
        """
        node_embeddings = inputs.node_embeddings
        adjacency_lists = inputs.adjacency_lists
        nodes_num = tf.shape(node_embeddings)[0]
        # [E*type_num,H]
        # 所有类别中每一个节点收到的信息大小
        messages_all_type = self._calculate_messages_all_type(node_embeddings, adjacency_lists)
        # [E,]
        # 所有关系类别中信息流动的目标节点
        edge_type_to_message_targets = [adjacency_type_list[:, 1] for adjacency_type_list in adjacency_lists]

        # 就当前节点聚合所有收到的信息，并获得新的节点状态
        new_nodes_states = self._aggregate_function(messages_all_type,
                                                    edge_type_to_message_targets,
                                                    nodes_num)
        return new_nodes_states

    def _calculate_messages_all_type(self, node_embeddings, adjacency_lists):
        messages_all_type = []
        type_incoming_edges_num, type_outing_edges_num = self._calculate_type_to_incoming_edges_num(node_embeddings, adjacency_lists)
        for edge_type_idx, adjanceny_list_edge_type in enumerate(adjacency_lists):  # M表示当前类的edge类型中包含的edge个数
            edge_sources = adjanceny_list_edge_type[:, 0]  # [M]
            edge_targets = adjanceny_list_edge_type[:, 1]  # [M]
            edge_source_states = tf.gather(node_embeddings, edge_sources)  # [M,H]
            edge_targets_states = tf.gather(node_embeddings, edge_targets)  # [M,H]
            num_incoming_to_node_per_message = tf.gather(
                type_incoming_edges_num[edge_type_idx, :], edge_targets)  # message num [M], 目标每一个节点的message输入
            num_outing_to_node_per_message = tf.gather(
                type_outing_edges_num[edge_type_idx, :], edge_sources)

            messages = self.message_function(edge_source_states,
                                             edge_targets_states,
                                             num_incoming_to_node_per_message,
                                             num_outing_to_node_per_message,
                                             edge_type_idx)
            messages_all_type.append(messages)
        return messages_all_type

    def _calculate_type_to_incoming_edges_num(self, node_embeddings, adjacency_lists):
        """计算某种类型的边指向各节点的次数
        Calculate the type_to_num_incoming_edges tensor.
        Returns:
            float32 tensor of shape [L, V] representing the number of incoming edges of
            a given type. Concretely, type_to_num_incoming_edges[l, v] is the number of
            edge of type l connecting to node v.
        """
        type_to_incoming_edges_num = []
        type_to_outing_edges_num = []
        for edge_type_adjacency_list in adjacency_lists:
            source = edge_type_adjacency_list[:, 0]
            targes = edge_type_adjacency_list[:, 1]
            indices_source = tf.expand_dims(source, -1)
            indices_targets = tf.expand_dims(targes, -1)
            incoming_edges_num = tf.scatter_nd(
                indices=indices_targets,
                updates=tf.ones_like(targes,dtype=tf.float32),
                shape=(tf.shape(node_embeddings)[0],)
            )
            outing_edges_num = tf.scatter_nd(
                indices=indices_source,
                updates=tf.ones_like(source,dtype=tf.float32),
                shape=(tf.shape(node_embeddings)[0],)
            )
            type_to_incoming_edges_num.append(incoming_edges_num)
            type_to_outing_edges_num.append(outing_edges_num)
        return tf.stack(type_to_incoming_edges_num), tf.stack(type_to_outing_edges_num)

    def _aggregate_function(self,
                            message_per_type,
                            edge_type_to_message_targets,
                            num_nodes):
        if self.aggr == "sum":
            aggregation_fn = tf.math.unsorted_segment_sum
        elif self.aggr == "max":
            aggregation_fn = tf.math.unsorted_segment_max
        elif self.aggr == "mean":
            aggregation_fn = tf.math.unsorted_segment_mean
        elif self.aggr == "sqrt":
            aggregation_fn = tf.math.unsorted_segment_sqrt_n
        # data = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        # unsorted_segment_sum(data,[2,0,1],3)
        # output[0]：i = 0，对应segment_ids中值为0的索引为1，则output[0] = data[1] = [3, 4, 5]。
        # output[1]：i = 1，对应segment_ids中值为1的索引为2，则output[1] = data[2] = [6, 7, 8]。
        # output[2]：i = 2，对应segment_ids中值为2的索引为0，则output[2] = data[0] = [0, 1, 2]。
        message_targets = tf.concat(edge_type_to_message_targets, axis=0)
        messages = tf.concat(message_per_type, axis=0)
        aggregated_messages = aggregation_fn(
            data=messages, segment_ids=message_targets, num_segments=num_nodes
        )  # 按节点从message_targets中跳出所有类别中传向当前节点的的信息值并求和后获得当前节点在所有类别之下的总的信息输入值。
        return aggregated_messages
