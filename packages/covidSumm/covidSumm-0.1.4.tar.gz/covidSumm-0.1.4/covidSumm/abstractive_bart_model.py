import torch
import json
from .abstractive_utils import get_ir_result, result_to_json, get_qa_result
from fairseq.models.bart import BARTModel


import nltk.data
import re



class Bart_model(object):
    def __init__(self, model_path):
        # self.model = torch.hub.load('pytorch/fairseq', 'bart.large.cnn')
        self.model = BARTModel.from_pretrained(model_path, checkpoint_file='model.pt')
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(device)
        self.model.eval()
        self.model.half()
        self.count = 1
        self.bsz = 3
        self.summary_list = []
        self.slines = []
    
    def process_hypothesis(self, hypothesis):
        # replace some incomplete sentences
        hypothesis_final = ""
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        hypo_sentence_list = sent_detector.tokenize(hypothesis.strip())
        for each in hypo_sentence_list:
            if re.match('.*[?.!]$', each):
                hypothesis_final += each
                hypothesis_final += " "
        
        return hypothesis_final

        
    def bart_generate_summary(self, paragraphs_list):
        self.summary_list = []
        self.slines = []
        for i in range(len(paragraphs_list)):
            self.sline = paragraphs_list[i]['src'].strip()
            self.slines.append(self.sline.strip())
            if self.count % self.bsz == 0:
                with torch.no_grad():
                    hypotheses_batch = self.model.sample(self.slines, beam=4, lenpen=1.0, max_len_b=64, min_len=8, no_repeat_ngram_size=3)

                for hypothesis in hypotheses_batch:
                    hypothesis_final = self.process_hypothesis(hypothesis)
                    self.summary_list.append(hypothesis_final)
                self.slines = []
            self.count += 1

        if self.slines != []:
            hypotheses_batch = self.model.sample(self.slines, beam=4, lenpen=1.0, max_len_b=64, min_len=8, no_repeat_ngram_size=3)
            for hypothesis in hypotheses_batch:
                hypothesis_final = self.process_hypothesis(hypothesis)
                self.summary_list.append(hypothesis_final)
        return self.summary_list


def bart_generate_summary_list(list_of_paragraphs_list, bart_model):
    count = bart_model.count
    bsz = bart_model.bsz

    list_of_summary_list = []

    for paragraphs_list in list_of_paragraphs_list:
        summary_list = bart_model.bart_generate_summary(paragraphs_list)
        summary_result = ""
        for item in summary_list:
            summary_result += item.replace("\n", ' ')

        list_of_summary_list.append(summary_result)
    
    return list_of_summary_list



def get_bart_answer_summary(query, bart_model):
    paragraphs_list = get_qa_result(query, topk = 3)
    answer_summary_list = bart_model.bart_generate_summary(paragraphs_list)
    answer_summary_result = ""
    for item in answer_summary_list:
        answer_summary_result += item.replace('\n', ' ')
    
    answer_summary_json = {}
    answer_summary_json['summary'] = answer_summary_result
    answer_summary_json['question'] = query
    return answer_summary_json


def get_bart_article_summary(query, bart_model, topk = 3):
    article_list, meta_info_list = get_ir_result(query, topk)
    summary_list = bart_generate_summary_list(article_list, bart_model) 
    summary_list_json = []    
    with open('summary_bart.output', 'w') as fout:
        for i in range(len(summary_list)):
            json_summary = {}
            json_summary = result_to_json(meta_info_list[i], summary_list[i])
            summary_list_json.append(json_summary)
            json.dump(json_summary, fout)
            fout.write('\n')

    return summary_list_json

