# catd
A Chinese co-word analysis with topic discovery package.

# Overview
The catd co-word analysis with topic discovery package is intend for Chinese corpus analysis.

## Use case
For better experience, you can run this script (with your corpus which have list of documents separated by `'\n'`.)

Corpus('$ProjectRoot/data/original_data/tianya_posts_test_set_10.txt):
```text
documents1
documents2
...
```

Program: 
```python
import catd
import os

corpus = []
with open(os.path.join('data', 'original_data', 'tianya_posts_test_set_10.txt'), encoding='utf-8') as f:
    for line in f:
        corpus.append(line)

stop_words_set = catd.util.collect_all_words_to_set_from_dir(os.path.join('data', 'stop_words'))

cut_corpus = catd.util.word_cut(corpus, stop_words_set)

word_net = catd.WordNet()
coded_corpus = word_net.generate_nodes_hash_and_edge(cut_corpus)
word_net.add_cut_corpus(coded_corpus)
```
## Note

Now I am working on the efficient visualization for big graph (hundreds of millions of edges).

If you have any question or suggestion, feel free to contact [the Author](mailto:danielqin7@outlook.com) in English or Chinese. But for the benefit of all users, please make communicate in English when it is public.  


## Data Structure
 
```
* WordNet
    * nodes   list[WordNode1, WordNode2, ...])
    * edges   dict[word][neighbors] -> weight)
    * docs    list[Doc1, Doc2, ...]
    * get_node_by_str dict[word] -> WordNode

* WordNode
    * id
    * name
    * doc_count
    * word_count
    * inverse_document_frequency

* Doc
    * id
    * word_count_in_doc
    * word_tf_in_doc
    * word_tf_idf
    * num_of_words
```

## log

### 0.3.0

Add support for lda model and topic information aggregation from words. 

## License

MIT License
