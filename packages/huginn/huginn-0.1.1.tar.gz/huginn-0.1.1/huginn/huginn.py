import numpy as np

from .interest import get_interest
from .anomalies import constant_sd, rolling_std, ewm_std
from .visualize import plot_data_plotly, plot_data, plot_data_with_anomalies, plot_data_with_anomalies_plotly
from .articles import get_articles_title_text_images_all_dates
from ._lda import tokenize, get_lemma, prepare_text_for_lda, retrieve_tokens, set_dict, set_corpus, run_lda
from ._gpt2 import run_gpt2
from ._summarizer import run_summary

class Huginn:
    def __init__(self, key_word, mid=None):
        self.name = key_word
        self.mid = mid
        self.interest = get_interest(self.name, self.mid)

    def get_anomalies(self, method="ewm", **kwargs):
        """Get anomalies under method assumption (by default ewm)

        :argument method: ewm, rolling or constant
        :argument **kwargs: if ewm halflife_mean, halflife_std, k (set to 1, 10 and 1 by default)
                            if rolling lookback_mean, lookback_std, k (set to 1, 10 and 1 by default)
                            if constant k (set to 1 by default)

        :returns the anomalies as a DateIndex
        """
        if method == "ewm":
            self.anomalies = ewm_std(self.interest, **kwargs)
        if method == "rolling":
            self.anomalies = rolling_std(self.interest, **kwargs)
        if method == "constant":
            self.anomalies = constant_sd(self.interest, **kwargs)
        self.anomalies_formatted = np.array(self.anomalies, dtype='datetime64[D]')
        return self.anomalies

    def check_got_anomalies(self):
        """Method to check if get_anomalies has been called, used primarily as a check in later functions"""
        if not hasattr(self, 'anomalies'):
            raise AttributeError('Huginn has not gotten anomalies yet. Use \'get_anomalies\' before using '
                                 'Huginn')


    def check_got_articles(self):
        """Method to check if get_articles() has been called, used primarily as a check in later functions"""
        if not hasattr(self, 'articles'):
            raise AttributeError('Huginn has not gotten article texts yet. Use \'get_articles\' before using '
                                 'Huginn')

    def check_got_ldamodel(self):
        """Method to check if model_lda() has been called, used primarily as a check in later functions"""
        if not hasattr(self, 'ldamodel'):
            raise AttributeError('Huginn has not gotten article texts yet. Use \'model_lda\' before using '
                                 'Huginn')


    def plot_interest(self, plotly=False):
        """Plot only the interestt the month of the entity or person under study"""
        if not plotly:
            plot_data(self.interest)
        else:
            return plot_data_plotly(self.interest)

    def plot_interest_with_anomalies(self, plotly=False, as_var=False):
        """
        Plot interest by month and the anomalies (as vertical lines)
        """
        self.check_got_anomalies()
        if not plotly:
            self.anomaly_plot = plot_data_with_anomalies(self.interest, self.anomalies, as_var)
        else:
            self.anomaly_plot = plot_data_with_anomalies_plotly(self.interest, self.anomalies, as_var)
            return self.anomaly_plot
    
    def get_info(self, num_links):
        self.check_got_anomalies()
        tmp = get_articles_title_text_images_all_dates(self.name, self.anomalies, num_links)
        self.urls = tmp['urls']
        self.titles = tmp['titles']
        self.articles = tmp['texts']
        self.images = tmp['images']

    def model_lda(self, viz=True):
        """Must have run get_anomalies() and get_title_text() to have requisite articles in session
           prior to running LDA on the object
        """

        self.check_got_anomalies()
        self.check_got_articles()
        article_list = [item for sublist in list(self.articles.values()) for item in sublist if len(item) > 10]
        self.text_data = retrieve_tokens(article_list)
        self.dictionary = set_dict(self.text_data)
        self.corpus = set_corpus(self.text_data, self.dictionary)
        self.ldamodel, self.dom_topic, self.gpt2_input = run_lda(self.corpus, self.dictionary, article_list)

    def gpt2(self):
        self.check_got_anomalies()
        self.check_got_articles()
        self.check_got_ldamodel()
        self.gpt2_output = run_gpt2(self.gpt2_input)

    def get_summary(self):
        self.check_got_anomalies()
        self.check_got_articles()
        self.check_got_ldamodel()
        self.summary = run_summary(self.gpt2_input)

