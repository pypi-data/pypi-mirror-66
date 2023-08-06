# -*- coding: utf-8 -*-
import re
import math
import json
from gensim.models import LdaModel
import jieba
from jieba import posseg
from .WordNode import WordNode
from .Doc import Doc
from .util import *
from .Topic import Topic


class WordNet:
    def __init__(self):
        self.docs = []
        self.nodes = []
        self.edges = {}
        self.topics = []

        self.get_node_by_str = {}

        self.stop_words_set = set()
        self.selected_words = set()

        self.lda_model = None

    def add_selected_word_ids_to_set(self, words, intersection_mode=False):
        if intersection_mode and len(self.selected_words) != 0:
            self.selected_words = self.selected_words.intersection(words)
        else:
            for word in words:
                self.selected_words.add(word)

    def add_stop_words_set(self, stop_words_set):
        self.stop_words_set = stop_words_set

    def get_stop_words_set(self):
        return self.stop_words_set

    def word_cut(self, corpus_with_time, stop_words_set, user_selected_words_mode=False,
                 selected_part_of_speech=None, if_output_tokens=False):
        """
        :param user_selected_words_mode:
        :param stop_words_set:
        :param if_output_tokens:
        :param selected_part_of_speech:
        :param corpus_with_time:
        :return: a list of cleaned documents contain only Chinese characters
        """
        if selected_part_of_speech is None:
            # set default selection
            selected_part_of_speech = {'an', 'n', 'nr', 'ns', 'nt', 'nz', 'vn'}

        self.add_stop_words_set(stop_words_set)
        corpus_after_cut = []
        keep_chinese_chars = re.compile(r'[^\u4e00-\u9fa5]')
        num_of_docs = len(corpus_with_time)
        index = 0

        for doc, time in corpus_with_time:
            list_of_cut_words = []
            # keep only Chinese characters
            doc = keep_chinese_chars.sub(' ', str(doc))
            for word_with_part_of_speech in jieba.posseg.dt.cut(doc):
                word, part_of_speech = str(word_with_part_of_speech).split('/')
                if user_selected_words_mode is False:
                    if word not in stop_words_set and part_of_speech in selected_part_of_speech and len(word) > 1:
                        list_of_cut_words.append(word)
                else:
                    if word not in stop_words_set and part_of_speech in selected_part_of_speech and len(word) > 1 \
                            and word in self.selected_words:
                        list_of_cut_words.append(word)
            corpus_after_cut.append((list_of_cut_words, time))

            index += 1
            display_progress('word cut', index, num_of_docs)

        if if_output_tokens:
            save_obj(corpus_after_cut, 'corpus_with_time')

        return corpus_after_cut

    def output_d3_force_graph_json(self, filepath=''):
        # add nodes
        # https://bl.ocks.org/heybignick/3faf257bbbbc7743bb72310d03b86ee8
        # {
        #     "nodes": [
        #         {"id": "Myriel", "group": 1},
        #         {"id": "Tholomyes", "group": 2},
        #         {"id": "Listolier", "group": 3},
        #         {"id": "Fantine", "group": 3}
        #     ],
        #     "links": [
        #         {"source": "Gervais", "target": "Myriel", "value": 1},
        #         {"source": "Mlle.Baptistine", "target": "Myriel", "value": 8},
        #         {"source": "Mme.Magloire", "target": "Myriel", "value": 10}
        #     ]
        # }

        # d3_force_graph_json['people'].append({
        #     'name': 'Larry',
        #     'website': 'google.com',
        #     'from': 'Michigan'
        # })

        d3_force_graph_json = {'nodes': [], 'links': []}

        for node in self.nodes:
            d3_force_graph_json['nodes'].append({
                'id': node.word,
                'group': node.group
            })
        for node_id in self.edges.keys():
            for neighbor_id in self.edges[node_id].keys():
                d3_force_graph_json['links'].append({
                    'source': self.nodes[node_id].word,
                    'target': self.nodes[neighbor_id].word,
                    'value': self.edges[node_id][neighbor_id]
                })

        with open(os.path.join(filepath, 'd3_force_graph.json'), 'w', encoding='utf-8') as json_outfile:
            json.dump(d3_force_graph_json, json_outfile)

    def description(self):
        """
        output numbers of valid word, edges, and docs
        :return: void
        """
        num_of_edges = 0
        for word_id in self.edges.keys():
            num_of_edges += len(self.edges[word_id])
        return '[word_net info]\n' \
               '\tnumber of word_net.docs: {}\n\tnumber of word_net.nodes: {}\n\tnumber of word_net.edges: {}'\
            .format(len(self.docs), len(self.nodes), num_of_edges)

    def docs_description(self):
        docs_info = '[docs info]'
        for doc in self.docs:
            docs_info += doc.description(self)
        return docs_info

    def nodes_description(self):
        nodes_info = '[nodes info]\n'
        for node in self.nodes:
            nodes_info += str(node) + '\n'
        return nodes_info

    def edges_description(self):
        edge_info = '[edge info]'
        for word_id in self.edges.keys():
            for neighbor_id in self.edges[word_id]:
                edge_info += '\t{:8}'.format(self.word_id_to_word(word_id)) \
                               + '-> {:8}'.format(self.word_id_to_word(neighbor_id)) \
                               + '  {}'.format(self.edges[word_id][neighbor_id]) + '\n'
        return edge_info

    def add_cut_corpus(self, coded_corpus):
        """
        :param coded_corpus: list of lists of cut word
        :return: void
        """

        num_of_docs = len(coded_corpus)
        index = 0

        # generate doc
        for doc, time in coded_corpus:
            word_id_counter = count_word_in_doc(doc)

            for node_id in word_id_counter.keys():
                # update doc_count and word_count
                self.nodes[node_id].doc_count += 1
                self.nodes[node_id].word_count += word_id_counter[node_id]

                for neighbor_id in word_id_counter:
                    if neighbor_id not in self.edges[node_id].keys():
                        self.edges[node_id][neighbor_id] = 1
                    else:
                        self.edges[node_id][neighbor_id] += 1

                if time in self.nodes[node_id].time_statistics.keys():
                    self.nodes[node_id].time_statistics[time] += 1
                else:
                    self.nodes[node_id].time_statistics[time] = 1

            self.docs.append(
                Doc(doc_id=index, word_id_count_in_doc=word_id_counter, number_of_words=len(doc), time=time))

            index += 1
            display_progress('add cut corpus_with_time', index, num_of_docs)

        for node in self.nodes:
            node.inverse_document_frequency = math.log(num_of_docs / node.doc_count + 1)

        for doc in self.docs:
            for word_id in doc.word_id_count_in_doc.keys():
                doc.word_id_tf[word_id] = doc.word_id_count_in_doc[word_id] / doc.number_of_words
                doc.word_id_tf_idf[word_id] = doc.word_id_tf[word_id] * self.nodes[word_id].inverse_document_frequency

    def get_cut_corpus(self):
        """
        :return: list of lists of word
        """
        corpus = []
        for doc in self.docs:
            word_list = []
            for word_id in doc.word_id_count_in_doc.keys():
                for i in range(doc.word_id_count_in_doc[word_id]):
                    word_list.append(self.word_id_to_word(word_id))
            corpus.append(word_list)
        return corpus

    def generate_id_to_word(self):
        """
        :return: dict[id] = word
        """
        id2word = {}
        for node in self.nodes:
            id2word[node.node_id] = node.word
        return id2word

    def generate_word_to_id(self):
        """
        :return: dict[word] = id
        """
        word2id = {}
        for node in self.nodes:
            word2id[node.word] = node.node_id
        return word2id

    def generate_docs_to_bag_of_words(self):
        """
        Convert each doc into the bag-of-word format
        :return: list of `(token_id, token_count)` tuples
        """
        bow = []
        for doc in self.docs:
            doc_bow = []
            for word_id in doc.word_id_count_in_doc.keys():
                doc_bow.append((word_id, doc.word_id_count_in_doc[word_id]))
            bow.append(doc_bow)
        return bow

    def generate_lda_model(self, num_topics=5, chunksize=100000, passes=20, iterations=400, eval_every=1):
        id2word = self.generate_id_to_word()
        corpus = self.generate_docs_to_bag_of_words()

        print('[generate_lda_model] generating model')
        self.lda_model = LdaModel(
            corpus=corpus,
            id2word=id2word,
            chunksize=chunksize,
            alpha='auto',
            eta='auto',
            iterations=iterations,
            num_topics=num_topics,
            passes=passes,
            eval_every=eval_every
        )

        topics = get_topic_with_words(gensim_lda_model=self.lda_model)

        for topic in topics:
            doc_count_weighted = 0
            word_count_weighted = 0
            inverse_document_frequency_weighted = 0
            time_statistics_aggregated = {}

            for word, contribution in topic[1]:
                node = self.get_node_by_str[word]

                # update group for nodes
                if node.group:
                    if contribution > node.group[1]:
                        node.group = (topic[0], contribution)
                else:
                    node.group = (topic[0], contribution)

                doc_count_weighted += node.doc_count * contribution
                word_count_weighted += node.word_count * contribution
                inverse_document_frequency_weighted += node.inverse_document_frequency * contribution

                for date in node.time_statistics:
                    if time_statistics_aggregated.get(date):
                        time_statistics_aggregated[date] += node.time_statistics[date]
                    else:
                        time_statistics_aggregated[date] = node.time_statistics[date]

            sorted_time_statistics_aggregated = []
            date_list = time_statistics_aggregated.keys()
            for key in sorted(date_list):
                sorted_time_statistics_aggregated.append((key, time_statistics_aggregated[key]))

            new_topic = Topic(topic[0],
                              topic[1],
                              doc_count_weighted,
                              word_count_weighted,
                              inverse_document_frequency_weighted,
                              sorted_time_statistics_aggregated)
            self.topics.append(new_topic)
            display_progress('creat topic obj', topic[0], num_topics)

    def get_topics(self):
        if self.topics:
            return self.topics
        else:
            print('[get_topics] lda model not created.')

    def get_top_percent_words_by_tf_idf_in_each_doc(self, percent):
        extracted_words_id_set = set()
        for doc in self.docs:
            sorted_list = sorted(doc.word_id_tf_idf, key=lambda j: doc.word_id_tf_idf[j], reverse=True)
            extracted_sorted_list = sorted_list[0:int(len(sorted_list) * percent)]
            extracted_words_id_set.update(set(extracted_sorted_list))

        extracted_words_set = set()
        for word_id in extracted_words_id_set:
            extracted_words_set.add(self.nodes[word_id].word)

        return extracted_words_set

    def get_words_above_doc_count_percent(self, percent):
        extracted_words_set = set()
        threshold = int(len(self.docs) * percent)
        for node in self.nodes:
            if node.doc_count > threshold:
                extracted_words_set.add(node.word)

        return extracted_words_set

    def get_top_words_in_each_topics(self, topK=None):
        if self.topics:
            if topK:
                lda_selected_words_set = set()
                word_counter = 0
                for topic in self.topics:
                    for word_with_contribution in topic[1]:
                        word = word_with_contribution[0]
                        lda_selected_words_set.add(word)
                        word_counter += 1
                        if word_counter >= topK:
                            break
                return lda_selected_words_set
            else:
                lda_selected_words_set = set()
                for topic in self.topics:
                    for word_with_contribution in topic[1]:
                        word = word_with_contribution[0]
                        lda_selected_words_set.add(word)
                return lda_selected_words_set
        else:
            print('[get_topics] lda model not created.')

    def word_to_id(self, word):
        return self.get_node_by_str[word].node_id

    def word_id_to_word(self, node_id):
        return self.nodes[node_id].word

    def generate_nodes_hash_and_edge(self, cut_corpus_with_time):
        """
        setup all the nodes, edges, and a dict to get nodes by word
        :param cut_corpus_with_time: list of lists of cut word
        :return: void
        """
        word_set = set()
        for cut_doc, time in cut_corpus_with_time:
            for word in cut_doc:
                word_set.add(word)

        num_of_nodes = len(word_set)
        index = 0

        for unique_word in word_set:
            new_node = WordNode(node_id=index, word=unique_word)
            self.nodes.append(new_node)
            self.get_node_by_str[unique_word] = new_node

            self.edges[index] = {}

            index += 1
            display_progress('generate_nodes_hash', index, num_of_nodes)

        coded_corpus = []
        for cut_doc, time in cut_corpus_with_time:
            id_doc = []
            for word_to_be_coverted in cut_doc:
                id_doc.append(self.word_to_id(word_to_be_coverted))
            coded_corpus.append((id_doc, time))
        return coded_corpus

    def export_for_gephi(self):
        with open(os.path.join('output', 'gephi_nodes.csv'), 'w+', encoding='utf-8') as nodes_file:
            nodes_file.write('Id, Label' + '\n')
            for node in self.nodes:
                nodes_file.write(str(node.node_id) + ', ' + str(node.word) + '\n')

        with open(os.path.join('output', 'gephi_edges.csv'), 'w+', encoding='utf-8') as edges_file:
            edges_file.write('Source, Target, Weight\n')
            for source in self.edges.keys():
                for target in self.edges[source].keys():
                    edges_file.write(str(source) + ', ' + str(target) + ', ' + str(self.edges[source][target]) + '\n')

    def export(self, dest_dir=os.path.join('../output', 'exported'), optional_postfix=''):
        if len(optional_postfix) != 0:
            optional_postfix = '_' + optional_postfix
        with open(os.path.join(dest_dir, 'data_structure', optional_postfix, '.txt'),
                  'w+', encoding='utf-8') as output_file:
            output_file.write('# word_net.docs')
            for doc in self.docs:
                pass
