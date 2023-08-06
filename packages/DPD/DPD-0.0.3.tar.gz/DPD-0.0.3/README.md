# Dendrogram Prototypical Discourse Analysis
According to [Harris, 1954] and [Rubenstein and Goodenough, 1965], words in natural languages are structured within linguistic environments (e.g.,sentences, paragraphs), and in this context, words having similar meanings,  tend  to  share  similar  contexts.   This  assumption,  known  as  the Distributional  Hypothesis, suggests that a corpus is often constituted bys everal  discursive  contexts;  each  one  being  a  set  of  extended  linguistic environments,  conveying  similar/related  concepts  and  topics.   Although this  theory  emerged  in  linguistics  in  1954,  it  received  recently  an  in-creasing attention in many other fields such as in cognitive sciences (e.g.,[McDonald and Ramscar, 2001]),  and  natural  language  processing  (e.g.,[Mikolov et al., 2013a]).  This hypothesis is the founding principle of our approach. Our method aims at modeling a large corpus, as a set of so-called DP-discourses, and then studying them as prototypical speeches.  To do so, the core step,  consists in building clusters of words sharing similar dis-cursive contexts.  This was achieved using word-embedding and subspace clustering, but other data-mining techniques could be used.  Then, intra-cluster  words  were  represented  asDendrogram  Prototypical  Discourses(DP-discourses), using a hierarchical clustering algorithm.  Finally, DP-discourses revealed to be comprehensible enough, to be studied using Charaudeau’s methodology, and they could possibly be analyzed using other discourse analysis approaches.

## Installation

The easiest way to install the generator is using `pip` the package installer for Python.
Typing the command:

`pip install DPD`

## Tutorial

Check the jupyter notebook tutorial `tutorials/tutorial1.ipynb` for a basic usage illustration

## License

This project is under the GNU GENERAL PUBLIC LICENSE (Version 3, 29 June 2007)
